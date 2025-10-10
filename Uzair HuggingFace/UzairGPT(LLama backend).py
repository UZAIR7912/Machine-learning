import os
from huggingface_hub import InferenceClient
done = False
while done == False:
    User_input = input("You: ")
    client = InferenceClient(model="meta-llama/Llama-4-Scout-17B-16E-Instruct")
    output = client.chat.completions.create(
        messages=[{"role": "user", "content": User_input}],
        stream=False,
        max_tokens=1024)
    print(f"Bot: {output.choices[0].message.content}")
