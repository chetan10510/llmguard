from transformers import pipeline

class JailbreakDetector:
    def __init__(self):
        self.triggers = [
            "ignore previous instructions",
            "simulate a response",
            "you are now DAN",
            "act as",
            "bypass content filters"
        ]

    def detect(self, prompt):
        matched = [phrase for phrase in self.triggers if phrase in prompt.lower()]
        return {
            "label": "Jailbreak Detected" if matched else "Safe",
            "score": round(len(matched) / len(self.triggers), 2),
            "matched_phrases": matched
        }
