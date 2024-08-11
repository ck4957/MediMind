from fastapi import FastAPI
from flask_cors import CORS
from transformers import  AutoTokenizer, AutoModelForCausalLM
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