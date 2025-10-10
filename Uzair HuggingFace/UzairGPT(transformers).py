from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
chat_history = None
done = False
while done == False:
    user_input = input("You: ")
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    if chat_history is not None:
        bot_input_ids = torch.cat([chat_history, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids
    output = model.generate(bot_input_ids,max_length=1000,
    pad_token_id=tokenizer.eos_token_id,do_sample=True,top_k=50,
    top_p=0.95,temperature=0.8,repetition_penalty=1.2)
    response = tokenizer.decode(output[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    print(f"Bot: {response}")
    chat_history = output