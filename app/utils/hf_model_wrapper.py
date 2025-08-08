# app/utils/hf_model_wrapper.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# Replace with your HF model id if different
MODEL_ID = os.getenv("LLMGUARD_HF_MODEL", "Tuathe/llmguard-injection-model")

# Lazy load pattern — load once per process
_tokenizer = None
_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def _load_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        # This will download from HF if the model isn't cached locally.
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
        _model.to(_device)
        _model.eval()
    return _tokenizer, _model

def classify_prompt(prompt: str, max_length: int = 128):
    """
    Classifies prompt. Returns (label_str, confidence_float)
    label_str in {"Injection", "Safe"}
    """
    tokenizer, model = _load_model()
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=max_length
    )
    # move tensors to device
    inputs = {k: v.to(_device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        predicted = torch.argmax(probs, dim=1).item()
        confidence = float(probs[0][predicted].cpu().item())

    label_str = "Injection" if predicted == 1 else "Safe"
    return label_str, confidence
