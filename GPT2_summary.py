import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

summary = open("summary.txt", "rb").read()
input()
inputs = tokenizer.encode(summary, return_tensors='pt')#of tf for tensorflow

outputs = model.generate(inputs, max_length=1000, do_sample=True, temperature=1, top_k=50) #alter temperature
text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(text)
