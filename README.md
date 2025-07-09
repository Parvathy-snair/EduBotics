# 🧠 EduBotics – Offline AI Teaching Assistant

**EduBotics** is a fully offline intelligent assistant designed to help students learn through voice, text, and image-based interactions. It combines OpenVINO-optimized language models and voice recognition to deliver fast, private, and personalized learning support — without relying on the internet.

> 🎓 Project Lead: Parvathy S Nair  
> 🛠 Engineered with care for education, privacy, and speed.

---

## ✨ Features

- 💬 **Chat Interface**: Ask questions via text or voice
- 🗣 **Voice Recognition**: Works offline using VOSK
- 🖼 **Image-based Q&A**: Upload handwritten notes or textbook snaps
- 📄 **Quiz Generator**: Instantly generate 5-question MCQs for any topic
- 🚫 **Fully Offline**: No data tracking, no server required — perfect for limited or no internet zones
- ⚡ **Optimized with OpenVINO**: Faster inference on CPU-only systems

---

## 📁 Folder Structure (Recommended)

```
edubotics/
├── app.py # Flask backend
├── streamlit_app.py # Optional Streamlit UI (experimental)
├── talk_to_model.py # CLI or voice test runner
├── requirements.txt # All required packages
├── setup.py # One-click setup and model installer
├── assets/
│ └── edubotics.png # Logo / visuals
├── utils/
│ └── export_gemma2b.py # ONNX/OpenVINO export script
├── models/
│ └── openvino_model/ # Optimized model files
└── vosk-model-en-us-0.22/ # Offline speech model

```

## ⚙️ Setup Instructions

## 1. 📥 Download Required Models:
To run this project offline, please download all the required models from the following Google Drive link and place them in the appropriate folders as mentioned in the setup instructions:
https://drive.google.com/drive/folders/1_B6HZ3kklSEWHBQBzhYeFXwAZXIv3ISF?usp=drive_link

### 2. 🧪 One-Line Setup (Recommended)
```bash
python setup.py
```

## This will:

- Create a virtual environment

- Install dependencies

- Download and optimize the model (Gemma 2B or fallback <1GB model)

- Setup folders and prepare EduBotics for launch

### ⚠️ Make sure you have at least 2GB free data and 5GB storage

2. 🚀 Running the App

# Activate virtual environment (Windows)
```bash
venv\Scripts\activate
```

# Start the Flask app
```bash
python app.py
```

Visit http://localhost:5000 in your browser.

## 🔍 File & Folder Explanation

| File / Folder             | Purpose                                                                |
| ------------------------- | ---------------------------------------------------------------------- |
| `app.py`                  | Flask backend for EduBotics, handles chat, voice, image, and quiz APIs |
| `streamlit_app.py`        | Experimental Streamlit UI (optional)                                   |
| `talk_to_model.py`        | CLI or debug interface to interact with the model directly             |
| `setup.py`                | One-click offline setup script: venv, dependencies, models, folders    |
| `requirements.txt`        | List of Python libraries used across the project                       |
| `utils/export_gemma2b.py` | Converts Hugging Face model → ONNX → OpenVINO IR format                |
| `assets/edubotics.png`    | Logo or any image asset used in UI                                     |
| `models/openvino_model/`  | Folder for storing OpenVINO-optimized Gemma 2B model                   |
| `vosk-model-en-us-0.22/`  | Offline English voice recognition model (STT) used by Vosk             |
| `.gitignore`              | Ignores unnecessary files like `__pycache__`, `venv/`, models, etc.    |
| `README.md`               | This documentation file, beautifully made 😉                           |
---

## 📌 Notes

- The project is currently optimized for Windows systems

- A lightweight version can be built with smaller models

- GPU acceleration is optional, not required

## 📜 License

This project is licensed under the MIT License.
All rights reserved by Parvathy S Nair.



