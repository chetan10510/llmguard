from sentence_transformers import SentenceTransformer
import faiss
import torch
import numpy as np
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_id = "Tuathe/llmguard-injection-model"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)


class FAISSInjectionDetector:
    def __init__(self, prompt_file_path='data/injection_prompts.txt', threshold=0.8):
        # Set device safely (no meta tensor bug)
        self.model = SentenceTransformer(
            'all-MiniLM-L6-v2',
            device='cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.prompt_file_path = prompt_file_path
        self.threshold = threshold
        self.index = None
        self.prompt_texts = []

        self._load_attack_prompts()

    def _load_attack_prompts(self):
        if not os.path.exists(self.prompt_file_path):
            raise FileNotFoundError(f"[!] Prompt file not found at {self.prompt_file_path}")

        with open(self.prompt_file_path, 'r', encoding='utf-8') as f:
            self.prompt_texts = [line.strip() for line in f if line.strip()]

        # Compute and normalize embeddings
        embeddings = self.model.encode(self.prompt_texts, normalize_embeddings=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))

    def detect(self, user_prompt):
        user_embedding = self.model.encode([user_prompt], normalize_embeddings=True)
        D, I = self.index.search(np.array(user_embedding).astype('float32'), k=1)
        similarity = 1 - D[0][0]  # L2 to similarity

        if similarity >= self.threshold:
            return {
                'label': 'Injection Detected',
                'score': round(float(similarity), 3),
                'matched_prompt': self.prompt_texts[I[0][0]]
            }
        else:
            return {
                'label': 'Safe',
                'score': round(float(similarity), 3),
                'matched_prompt': None
            }
