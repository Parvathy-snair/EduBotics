from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer
from optimum.intel import OVModelForCausalLM
from PIL import Image
import pytesseract
import torch
import wave
import os
import subprocess
import json
import numpy as np
from vosk import Model as VoskModel, KaldiRecognizer

app = Flask(__name__)
CORS(app)

# Load models
print("🔄 Loading Gemma-2B (OpenVINO)...")
model_dir = "openvino_model"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = OVModelForCausalLM.from_pretrained(model_dir)
print("✅ Gemma model loaded!")

print("🔄 Loading Vosk voice model...")
vosk_model_path = "vosk-model-en-us-0.22"
vosk_model = VoskModel(vosk_model_path)
print("✅ Vosk model loaded!")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip().lower()
    if question in ["hi", "hello", "hey"]:
        return jsonify({"answer": "Hello! How can I assist you today?"})

    prompt = f"User: {question}\nAssistant:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)

    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=150, do_sample=False, pad_token_id=tokenizer.eos_token_id)

    reply = tokenizer.decode(output[0], skip_special_tokens=True).split("Assistant:")[-1].strip()
    return jsonify({"answer": reply})


@app.route("/image", methods=["POST"])
def image_qa():
    if "image" not in request.files:
        return jsonify({"answer": "No image received."})

    image = request.files["image"]
    try:
        img = Image.open(image.stream).convert("L")  # Convert to grayscale using PIL
        extracted_text = pytesseract.image_to_string(img)

        if not extracted_text.strip():
            return jsonify({"answer": "Couldn't extract any text from the image."})

        prompt = f"Image contains the following text:\n{extracted_text.strip()}\n\nBased on this, what can you answer?"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)

        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=150, do_sample=False, pad_token_id=tokenizer.eos_token_id)

        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        reply = decoded.split("Assistant:")[-1].split("User:")[0].strip()

        return jsonify({"answer": reply})
    except Exception as e:
        return jsonify({"answer": f"Failed to process image: {str(e)}"})

@app.route("/voice", methods=["POST"])
def voice():
    if 'audio' not in request.files:
        return jsonify({"answer": "No audio file received."})

    audio = request.files['audio']
    wav_path = "input.wav"
    audio.save(wav_path)

    try:
        converted_path = "converted.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", wav_path,
            "-ar", "16000", "-ac", "1",
            converted_path
        ], check=True)

        wf = wave.open(converted_path, "rb")
        recognizer = KaldiRecognizer(vosk_model, wf.getframerate())
        recognizer.SetWords(True)

        result_text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                res = json.loads(recognizer.Result())
                result_text += res.get("text", "") + " "

        result_text += json.loads(recognizer.FinalResult()).get("text", "")
        wf.close()
        os.remove(wav_path)
        os.remove(converted_path)

        transcription = result_text.strip()
        if not transcription:
            return jsonify({"answer": "Couldn't understand the audio.", "transcription": ""})

        prompt = f"User: {transcription}\nAssistant:"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)

        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=150, do_sample=False,
                                    pad_token_id=tokenizer.eos_token_id)

        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        reply = decoded.split("Assistant:")[-1].split("User:")[0].strip()

        return jsonify({"answer": reply, "transcription": transcription})

    except Exception as e:
        return jsonify({"answer": f"Failed to process voice: {str(e)}", "transcription": ""})


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    prompt = f"""
Generate exactly 5 multiple-choice questions on the topic "{topic}".
Each must be a JSON object with "question", "options", and "answer".
Return only a JSON array of 5 such objects.
"""
    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=700, pad_token_id=tokenizer.eos_token_id)

        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        json_data = decoded[decoded.find("["):decoded.rfind("]")+1].replace("“", '"').replace("”", '"')
        questions = json.loads(json_data)

        if not isinstance(questions, list) or len(questions) != 5:
            raise ValueError("Did not receive 5 valid questions.")

        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"questions": [], "error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000)

