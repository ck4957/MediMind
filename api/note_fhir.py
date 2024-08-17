from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import get_peft_model
import torch
import json

app = Flask(__name__)
CORS(app)

