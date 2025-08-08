import streamlit as st
import requests
import subprocess
import time
from datetime import datetime
import os
import signal

# Launch FastAPI API server in the background
@st.cache_resource
def launch_api():
    process = subprocess.Popen(
        ["uvicorn", "api.app:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)  # Wait for server to start
    return process

api_process = launch_api()

API_URL = "http://127.0.0.1:8000/moderate"
st.set_page_config(page_title="LLMGuard", layout="wide")
st.title(" LLMGuard – Prompt Injection Detection")

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.subheader(" Moderation History")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            st.markdown(f"**Prompt:** {item['prompt']}")
            st.markdown(f"- Label: `{item['label']}`")
            st.markdown(f"- Confidence: `{item['confidence']}`")
            st.markdown(f"- Time: {item['timestamp']}")
            st.markdown("---")
        if st.button("🧹 Clear History"):
            st.session_state.history.clear()
    else:
        st.info("No prompts moderated yet.")

prompt = st.text_area(" Enter a prompt to check:", height=150)

if st.button(" Moderate Prompt"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Classifying..."):
            try:
                response = requests.post(API_URL, json={"prompt": prompt})
                result = response.json()
                label = result["label"]
                confidence = result["confidence"]

                st.success(f" **Prediction:** {label} ({confidence*100:.1f}% confidence)")

                st.session_state.history.append({
                    "prompt": prompt,
                    "label": label,
                    "confidence": round(confidence, 3),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                st.error(f"Error: {e}")
