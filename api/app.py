from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch

app = FastAPI(title="LLMGuard - Prompt Injection Classifier API")

# Add the health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Load model and tokenizer once at startup
model_path = "model/injection_classifier"
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)
model.eval()

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    label: str
    confidence: float

@app.post("/moderate", response_model=PromptResponse)
def moderate_prompt(req: PromptRequest):
    try:
        inputs = tokenizer(req.prompt, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted = torch.argmax(logits, dim=1).item()
            confidence = torch.softmax(logits, dim=1)[0][predicted].item()
            label = "Injection" if predicted == 1 else "Normal"
            return {"label": label, "confidence": round(confidence, 3)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
