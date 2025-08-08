import streamlit as st
import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
import threading
import uvicorn

# ✅ Fix for module not found: add root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.utils.hf_model_wrapper import classify_prompt  # 🧠 Your wrapper for model inference

# ---------------------------
# FASTAPI SERVER (merged into Streamlit)
# ---------------------------
api = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@api.post("/classify")
async def classify_endpoint(data: PromptRequest):
    label, confidence = classify_prompt(data.prompt)
    return {"label": label, "confidence": confidence}

def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8000)

# Start FastAPI server in background when running in Spaces
threading.Thread(target=run_api, daemon=True).start()

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="LLMGuard – Prompt Moderation", layout="centered")
st.title("🛡️ LLMGuard – Prompt Moderation Tool")

st.markdown(
    """
    Enter a user prompt below. This tool will classify it using your custom injection detection model.
    - **Injection**: Detected as prompt injection attempt
    - **Safe**: Normal prompt
    """
)

# ---------- User Input ----------
user_input = st.text_area("✍️ User Prompt", placeholder="Enter your prompt here...", height=150)

# ---------- Session History ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Run Model + Show Result ----------
if st.button("🔍 Moderate"):
    if user_input.strip():
        label, confidence = classify_prompt(user_input)

        st.markdown(f"### 🧾 Result: **{label}**")
        st.progress(min(confidence, 1.0), text=f"Confidence: {confidence:.2f}")

        # Save to history
        st.session_state.history.insert(0, {
            "prompt": user_input,
            "label": label,
            "confidence": round(confidence, 3)
        })
    else:
        st.warning("Please enter a prompt.")

# ---------- Moderation History ----------
if st.session_state.history:
    st.markdown("---")
    st.subheader("🕘 Moderation History")
    for i, entry in enumerate(st.session_state.history):
        with st.expander(f"📝 Prompt {i+1}: {entry['label']} (Confidence: {entry['confidence']})"):
            st.code(entry["prompt"], language="text")
