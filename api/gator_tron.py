from transformers import  AutoTokenizer, AutoModelForCausalLM, AutoModel

# Load the model and tokenizer
# Load model directly
model_name = "UFNLP/gatortron-base"
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_report(patient_data):
    # Prepare the input prompt
    prompt = f"Generate a medical report for patient with the following data: {patient_data}"
    
    # Tokenize the input
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate the report
    outputs = model.generate(**inputs, max_length=500)
    
    # Decode the output
    report = tokenizer.decode(outputs[0])
    
    return report

# Similar function for treatment plan generation