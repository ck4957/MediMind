from fastapi import FastAPI
from flask_cors import CORS
from transformers import  pipeline, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from flask import Flask, request, jsonify
from peft import get_peft_model
import torch
import json


# Load the model and tokenizer
# Load model directly
model_name = "UFNLP/gatortron-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

app = FastAPI()
CORS(app)
@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

def generate_text(prompt, max_length=500):
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=max_length)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

@app.post('/generate_report')
def generate_report():
    data = request.json
    patient = data['patient']
    prompt = f"Generate a detailed medical report for the following patient:\n\nName: {patient['name']}\nDate of Birth: {patient['birthDate']}\nGender: {patient['gender']}\nConditions: {', '.join(patient['conditions'])}\nMedications: {', '.join(patient['medications'])}\n\nMedical Report:"
    report = generate_text(prompt)
    return jsonify({"report": report})

@app.post('/suggest_treatment')
def suggest_treatment():
    data = request.json
    patient = data['patient']
    prompt = f"Suggest a detailed treatment plan for the following patient:\n\nName: {patient['name']}\nDate of Birth: {patient['birthDate']}\nGender: {patient['gender']}\nConditions: {', '.join(patient['conditions'])}\nMedications: {', '.join(patient['medications'])}\n\nTreatment Plan:"
    plan = generate_text(prompt)
    return jsonify({"plan": plan})


# Load the model and tokenizer (this should be done at startup)
def load_model():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    base_model_name = "meta-llama/Llama-2-13b-chat-hf"
    model_name = "healthsageai/note-to-fhir-13b-adapter"

    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        trust_remote_code=True,
        quantization_config=bnb_config,
        device_map='auto'
    )

    model.config.use_cache = False
    model.load_adapter(model_name)

    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True, return_tensor="pt", padding=True)
    tokenizer.pad_token = tokenizer.bos_token
    tokenizer.padding_side = 'left'

    for name, module in model.named_modules():
        if "norm" in name:
            module = module.to(torch.float32)

    return model, tokenizer

model, tokenizer = load_model()

generator = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    do_sample=False,
    eos_token_id=model.config.eos_token_id,
    max_length=4096
)

@app.route('/convert', methods=['POST'])
def convert_note_to_fhir():
    data = request.json
    clinical_note = data.get('note', '')

    prompt = f"""[INST] <<SYS>>
INSTRUCTION
Translate the following clinical note into HL7 FHIR R4 Format.
- Do not insert any values that are not in the note.
- Do not infer or impute any values
- Only include information that is essential:
    - information that is in the clinical note
    - information that is mandatory for a valid FHIR resource.

OUTPUT FORMAT
Return the HL7 FHIR structured information as a json string. denote the start and end of the json with a markdown codeblock:
```json
[RESOURCE HERE]
```
<</SYS>>

CLINICAL NOTE
{clinical_note}

[/INST]
"""

    with torch.autocast("cuda"):
        fhir_pred = generator(prompt)

    fhir_pred = fhir_pred[0]['generated_text']
    result = json.loads(fhir_pred.split("```")[3][4:].strip(" \t\n\r"))

    for resource in result['entry']:
        key_values = [(k, v) for k, v in resource['resource'].items()]
        for k, v in key_values:
            if v is None:
                del resource['resource'][k]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)