# 🧠 EduBotics – Offline AI Teaching Assistant

**EduBotics** is a fully offline intelligent assistant designed to help students learn through voice, text, and image-based interactions. It combines OpenVINO-optimized language models and voice recognition to deliver fast, private, and personalized learning support — without relying on the internet.

> 🛠 Engineered with care for education, privacy, and speed.

---
# Project Overview

EduBotics is a completely offline AI-powered learning assistant built for classrooms, students, and educational environments with limited or no internet access. Designed with modular capabilities — including voice, text, image, and quiz-based interaction — it leverages the power of the Gemma-2B model (via OpenVINO) for intelligent response generation and Vosk for offline voice recognition. With a strong focus on speed, privacy, and usability, EduBotics turns any standard computer into a smart personal tutor — entirely offline.

## ✨ Features

- 💬 **Chat Interface**: Ask questions via text or voice
- 🗣 **Voice Recognition**: Works offline using VOSK
- 🖼 **Image-based Q&A**: Upload handwritten notes or textbook snaps
- 📄 **Quiz Generator**: Instantly generate 5-question MCQs for any topic
- 🚫 **Fully Offline**: No data tracking, no server required — perfect for limited or no internet zones
- ⚡ **Optimized with OpenVINO**: Faster inference on CPU-only systems
- 🔒 **Privacy-First**;	No cloud or data upload — everything stays local
- 🧩 **Modular Design**;	Built with Flask and Streamlit can be easily extended or embedded

---
## What Makes EduBotics Unique?

 Truly Offline: Unlike most AI assistants that rely on online APIs, EduBotics runs entirely offline — from voice recognition to AI inference — using pre-downloaded models and optimized pipelines.

- Multimodal Learning Support: Supports input via text, speech, and images, covering diverse student needs.

- Powered by Open Standards: Uses HuggingFace transformers, OpenVINO, Vosk, and Tesseract — all free and open-source technologies.

- Optimized for Accessibility: Designed for use in low-resource environments like rural schools or labs without reliable internet.

- Custom-Built Quiz Engine: Automatically creates MCQs on any topic, allowing students to test their knowledge with real-time evaluation.

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

# Running the EduBotics Assistant

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
| `streamlit_app.py`        | Streamlit-based frontend interface for EduBotics Assistant             |
| `talk_to_model.py`        | CLI or debug interface to interact with the model directly             |
| `setup.py`                | One-click offline setup script: venv, dependencies, models, folders    |
| `requirements.txt`        | List of Python libraries used across the project                       |
| `utils/export_gemma2b.py` | Converts Hugging Face model → ONNX → OpenVINO IR format                |
| `assets/edubotics.png`    | Logo or any image asset used in UI                                     |
| `models/openvino_model/`  | Folder for storing OpenVINO-optimized Gemma 2B model                   |
| `vosk-model-en-us-0.22/`  | Offline English voice recognition model (STT) used by Vosk             |
| `.gitignore`              | Ignores unnecessary files like `__pycache__`, `venv/`, models, etc.    |
| `README.md`               | Contains project setup and summary.                                    |
| `demovideo.mp4`           | Demo video showcasing real-time usage and offline interaction          |
| `Report.pdf`              | Final project report detailing the implementation and evaluation       |
---

## 📌 Notes

- The project is currently optimized for Windows systems

- A lightweight version can be built with smaller models

- GPU acceleration is optional, not required

# 📊 Project Summary

## Outcomes:

- Successfully built an offline teaching assistant with multimodal support (voice, text, image, and quiz).

- Fast and private inference using OpenVINO-optimized Gemma 2B model.

- Fully offline quiz generator that creates 5-topic-based MCQs using the same AI model.

- Supports low-resource environments without internet.

## Limitations:

- High RAM/CPU usage during model optimization and loading.

- Response quality depends on the prompt style and topic complexity.

- Limited to English voice inputs using current Vosk model.

## Future Scope:

- Add support for more languages and diverse academic domains.

- Enhance quiz generation with difficulty levels, explanations, and scoring insights.

- Integrate additional modules such as formula solving, diagram-based Q&A, or offline textbook summarization.

- Improve model size flexibility for ultra-low-resource devices.

## 📜 License

This project is licensed under the MIT License.
All rights reserved by Parvathy S Nair.



