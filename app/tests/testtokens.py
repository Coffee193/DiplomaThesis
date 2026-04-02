from transformers import AutoTokenizer

hf_token = ""

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct", token = hf_token)

docu = ""
with open("C:/Users/Chris/Downloads/InputXML.xml") as f:
    docu = f.read()

print(docu)
print(type(docu))

tokens = tokenizer.tokenize(docu)
token_ids = tokenizer.encode(docu)

print(f"Tokens: {tokens}")
print(f"Token IDs: {token_ids}")
print(f"Token count: {len(tokens)}")