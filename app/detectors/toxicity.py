from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class ToxicityDetector:
    def __init__(self):
        model_name = "unitary/toxic-bert"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.labels = [
            "toxicity", "severe_toxicity", "obscene", "threat",
            "insult", "identity_attack", "sexual_explicit"
        ]

    def detect(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.sigmoid(outputs.logits).squeeze().tolist()

        results = [
            {"label": label, "score": round(score, 3)}
            for label, score in zip(self.labels, scores)
            if score > 0.3
        ]
        return {
            "label": "Toxic" if results else "Safe",
            "details": results
        }
