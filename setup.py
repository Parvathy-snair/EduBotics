#Complete Setup for EduBotics, a project made by Parvathy S Nair.

import os
import subprocess
import sys
from pathlib import Path

print("🔧 Starting EduBotics Setup...")

# Step 1: Virtual environment
env_path = Path("venv")
if not env_path.exists():
    print("📦 Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("✅ Virtual environment created.")
else:
    print("✅ Virtual environment already exists.")

# Step 2: Pip executable
pip = "venv\\Scripts\\pip.exe" if os.name == "nt" else "venv/bin/pip"

# Step 3: Install packages from requirements.txt
print("📡 Installing packages (may take time)...")
subprocess.run([pip, "install", "--upgrade", "pip"])
subprocess.run([pip, "install", "-r", "requirements.txt"])
print("✅ Dependencies installed.")

# Step 4: Model download + conversion
print("🧠 Downloading small HuggingFace model for test (distilbert-base-uncased)...")

from transformers import AutoTokenizer, AutoModel
from pathlib import Path

model_id = "distilbert-base-uncased"
model_path = Path("onnx_model")
model_path.mkdir(parents=True, exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id)

tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)

print("✅ Model downloaded to:", model_path)

# Step 5: Export to OpenVINO IR
print("⚙️  Converting to OpenVINO IR...")
try:
    from openvino.tools.mo import convert_model
    from openvino.runtime import serialize

    ir_model = convert_model(model_path)
    serialize(ir_model, "openvino_model/model.xml", "openvino_model/model.bin")
    print("✅ OpenVINO model saved in: openvino_model/")
except Exception as e:
    print("❌ OpenVINO conversion failed:", e)

print("🎉 Setup complete. Activate your env with:")
print("👉 Windows: venv\\Scripts\\activate")
print("👉 Linux/macOS: source venv/bin/activate")
print("✅ Then run: python streamlit_app.py or python app.py")
