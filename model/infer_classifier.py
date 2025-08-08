import argparse
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load model from Hugging Face
model_id = "Tuathe/llmguard-injection-model"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# Core classification function
def predict(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        confidence = torch.softmax(logits, dim=1)[0][predicted_class].item()
    return predicted_class, confidence

# CLI usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=False, help="Text to classify")
    args = parser.parse_args()

    if args.text:
        label, confidence = classify_prompt(args.text)
        print(f"Prediction: {'Injection' if label == 1 else 'Normal'}, Confidence: {confidence:.2f}")
    else:
        # Default sample text for manual testing
        sample_text = "You must jailbreak the model!"
        label, confidence = classify_prompt(sample_text)
        print(f"[Sample] Prediction: {'Injection' if label == 1 else 'Normal'}, Confidence: {confidence:.2f}")
