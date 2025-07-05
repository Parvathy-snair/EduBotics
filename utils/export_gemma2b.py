from optimum.intel import OVModelForCausalLM
from transformers import AutoTokenizer

model_id = "google/gemma-2b-it"

print("🔄 Downloading and converting Gemma-2B...")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = OVModelForCausalLM.from_pretrained(model_id, export=True)

model.save_pretrained("openvino_model")
tokenizer.save_pretrained("openvino_model")

print("✅ Export complete. Files saved to: openvino_model/")
