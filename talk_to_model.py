from transformers import AutoTokenizer
from optimum.intel import OVModelForCausalLM
import torch

print("🔄 Loading Cipher brain (Gemma-2B via OpenVINO)... Please wait ⏳")

model_dir = "openvino_model"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = OVModelForCausalLM.from_pretrained(model_dir)

print("✅ Cipher is now offline and ready, Miss Parvathy. Ask me anything.\n(Type 'bye' to exit)\n")

chat_history = []

while True:
    user_input = input("You 🧠: ").strip()
    if user_input.lower() in ["bye", "exit", "quit"]:
        print("Cipher: Powering down. See you later, Miss Parvathy.")
        break

    chat_history.append(f"User: {user_input}")
    prompt = "\n".join(chat_history) + "\nAssistant:"

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    full_text = tokenizer.decode(output[0], skip_special_tokens=True)
    reply = full_text.split("Assistant:")[-1].strip()

    print("Cipher:", reply, "\n")
    chat_history.append(f"Assistant: {reply}")
