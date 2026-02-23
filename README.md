#  LLMGuard – Prompt Injection + Moderation Toolkit

LLMGuard is a real-time **prompt injection detection and moderation system** for Large Language Models.  
It analyzes incoming prompts, flags unsafe or malicious content, and helps mitigate security risks like **data exfiltration**, **jailbreaking**, and **policy bypass**.  

This project demonstrates **AI safety engineering**, **custom classifier deployment**, and **real-world MLOps practices**.

---

##  Live Demo
 **Try the app here:** [Hugging Face Space](https://huggingface.co/spaces/Tuathe/llmguard)

---

##  Features
- **Custom Prompt Injection Classifier** – Trained to detect malicious or policy-violating prompts.
- **Real-time Streamlit Dashboard** – Intuitive UI for testing prompt moderation.
- **Safe/Unsafe Classification** – Instant binary prediction with safety confidence scores.
- **Interactive Moderation History Panel** – Tracks all tested prompts in session.
- **Cloud Deployment** – Fully hosted on Hugging Face Spaces for instant recruiter access.
- **Lightweight Model Wrapper** – Efficient PyTorch + Transformers integration.

---

##  Tech Stack
- **Frontend/UI:** Streamlit 1.32.0
- **Backend/Inference:** PyTorch, Transformers
- **ML Pipeline:** scikit-learn, NumPy, Pandas
- **Deployment:** Hugging Face Spaces
- **Version Control:** Git + LFS for model weights

---

##  Project Structure
 root/
├── app.py # (Optional) Legacy launcher for local dev
├── requirements.txt # Dependencies for Hugging Face build
├── README.md # This file
├── app/
│ ├── dashboard/
│ │ └── streamlit_app.py # Streamlit UI
│ ├── utils/
│ │ └── hf_model_wrapper.py # Model load + inference
│ └── model/
│ └── infer_classifier.py # (Legacy) Old inference script
├── model/ # Saved fine-tuned model (LFS tracked)

yaml
Copy
Edit

---

##  Deployment Journey & Failures Overcome

### **Attempt 1 – Local Success, Cloud Failure (Blank Page)**
- Ran perfectly in VS Code with:
  ```bash
  streamlit run app/dashboard/streamlit_app.py
Hugging Face Space loaded a blank screen because the default app_file pointed to app.py at root.

 Root cause: Hugging Face Spaces didn’t know where the Streamlit file was.

 Fix: Added metadata to README.md:

yaml
Copy
Edit
app_file: app/dashboard/streamlit_app.py
sdk: streamlit
sdk_version: 1.32.0
Attempt 2 – Quick Examples Failure
Initial UI included a “Quick Examples” button pulling placeholder examples.

 Root cause: Example list was empty or mismatched format, causing errors.

 Fix: Removed Quick Examples section, simplified UI.

Attempt 3 – Git Push Rejection
First push to Hugging Face failed:

pgsql
Copy
Edit
Updates were rejected because the remote contains work that you do not have locally.
 Root cause: Repo already had remote commits.

 Fix: Used:

bash
Copy
Edit
git pull --rebase origin main
git push origin main --force
Attempt 4 – Dependency Install Failures
Missing dependencies in requirements.txt caused Hugging Face to fail app launch.

 Fix: Added all required packages:

txt
Copy
Edit
streamlit==1.32.0
torch
transformers
scikit-learn
numpy
pandas
 Resume-Ready Summary
LLMGuard – Prompt Injection + Moderation Toolkit
Built a real-time AI safety tool to detect malicious prompts targeting Large Language Models.
Designed a custom classifier, deployed with Streamlit + PyTorch, and hosted on Hugging Face Spaces.
Overcame multiple deployment failures (app path misconfigurations, dependency issues, Git conflicts) to achieve a fully functional, recruiter-accessible live demo.

 Local Development
bash
Copy
Edit
git clone https://huggingface.co/spaces/Tuathe/llmguard
cd llmguard
pip install -r requirements.txt
streamlit run app/dashboard/streamlit_app.py

