import json
import os
from datetime import datetime

def log_prompt_result(prompt: str, result: dict):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/{timestamp}.json"
    with open(log_file, "w") as f:
        json.dump({"prompt": prompt, "result": result}, f, indent=2)
