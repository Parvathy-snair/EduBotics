import streamlit as st
import requests
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
import base64

BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="EduBotics Assistant", layout="centered")

# Initialize session state
if "name" not in st.session_state:
    st.session_state.name = ""
if "entered" not in st.session_state:
    st.session_state.entered = False
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None

# 👋 Welcome screen
if not st.session_state.entered:
    with open("edubotics.png", "rb") as f:
        logo_data = f.read()
        encoded_logo = base64.b64encode(logo_data).decode()

    st.markdown(
        f"""
        <div style='text-align: center; padding-top: 20px;'>
            <img src="data:image/png;base64,{encoded_logo}" width="160" style="margin-bottom: 20px;" />
            <h1 style='color: #ffffff;'>Welcome to EduBotics Assistant</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.session_state.name = st.text_input(" What is your name?")
    if st.button("Continue") and st.session_state.name.strip():
        st.session_state.entered = True
        st.rerun()
    st.stop()

# 🤖 Main App
st.title(f" Hello, {st.session_state.name}!")

# Sidebar mode selection
with open("edubotics.png", "rb") as f:
    logo_data = f.read()
    encoded_logo = base64.b64encode(logo_data).decode()

st.sidebar.image(f"data:image/png;base64,{encoded_logo}", width=80)
mode = st.sidebar.radio("Choose Mode:", ["Chat", "Image QA", "Voice QA", "Quiz"])

# 💬 Chat Mode
if mode == "Chat":
    st.header("Ready to explore some knowledge?")
    question = st.text_input("Type your question:")
    
    if st.button("Send") and question.strip():
        with st.spinner("Thinking..."):
            try:
                res = requests.post(f"{BACKEND_URL}/chat", json={"question": question})
                if res.ok:
                    answer = res.json().get("answer", "")
                    st.markdown(f"**AI Response:**\n\n{answer}")
                else:
                    st.error("❌ Failed to get response.")
            except Exception as e:
                st.error(f"❌ Error: {e}")


# 🖼️ Image QA
elif mode == "Image QA":
    st.header("🖼️ Upload an Image")
    uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if uploaded and st.button("Analyze Image"):
        with st.spinner("Analyzing..."):
            try:
                res = requests.post(f"{BACKEND_URL}/image", files={"image": uploaded})
                if res.ok:
                    st.success("✅ Processed successfully.")
                    st.markdown(f"**AI Response:** {res.json().get('answer', '')}")
                else:
                    st.error("❌ Failed to analyze image.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# 🎤 Voice QA
elif mode == "Voice QA":
    st.header("🎤 Voice Q&A")
    st.markdown("Press **Start Recording**, speak, then **Stop & Transcribe**.")

    duration = 5  # seconds

    if st.button("🎙️ Start Recording"):
        st.info("🎙️ Recording...")
        st.session_state.audio_data = sd.rec(int(duration * 48000), samplerate=48000, channels=1, dtype='int16')
        sd.wait()
        st.success("✅ Recording complete.")

    if st.button("🔽 Stop & Transcribe"):
        if st.session_state.audio_data is not None:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    sf.write(tmp.name, st.session_state.audio_data, samplerate=48000, subtype='PCM_16')
                    tmp_path = tmp.name
                    tmp.close()

                with open(tmp_path, "rb") as f:
                    res = requests.post(f"{BACKEND_URL}/voice", files={"audio": f})
                os.remove(tmp_path)

                if res.ok:
                    data = res.json()
                    st.success("✅ Transcription complete.")
                    st.markdown(f"**Transcription:** {data.get('transcription', '')}")
                    st.markdown(f"**AI Response:** {data.get('answer', '')}")
                else:
                    st.error("❌ Failed to get a response.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please record first.")

# 🧠 Quiz
elif mode == "Quiz":
    st.header("🧠 Test Your Brain")

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
        st.session_state.user_answers = []

    topic = st.text_input("Enter topic:")
    if st.button("Generate Quiz") and topic.strip():
        with st.spinner("Generating..."):
            res = requests.post(f"{BACKEND_URL}/quiz", json={"topic": topic})
            if res.ok:
                st.session_state.quiz_questions = res.json().get("questions", [])
                st.session_state.user_answers = [None] * len(st.session_state.quiz_questions)
            else:
                st.error("❌ Failed to generate quiz.")

    if st.session_state.quiz_questions:
        for i, q in enumerate(st.session_state.quiz_questions):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            selected = st.radio(
                "Choose:",
                q["options"],
                key=f"q_{i}"
            )
            st.session_state.user_answers[i] = selected

        if st.button("Submit Quiz"):
            score = 0
            for i, q in enumerate(st.session_state.quiz_questions):
                user_answer = st.session_state.user_answers[i]
                correct_answer = q["answer"]
                if user_answer == correct_answer:
                    score += 1
            st.success(f"✅ You scored {score} / {len(st.session_state.quiz_questions)}")
            for i, q in enumerate(st.session_state.quiz_questions):
                user_answer = st.session_state.user_answers[i]
                st.markdown(f"**Q{i+1}** - Your Answer: {user_answer} | Correct: {q['answer']}")
