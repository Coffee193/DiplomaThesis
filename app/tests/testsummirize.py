from langchain_classic.chains.summarize import load_summarize_chain
from langchain_ollama import ChatOllama
from transformers import AutoTokenizer

from langchain_classic.schema.document import Document
import time



document_path = "C:/Users/Chris/Downloads/diplomat/xml_examples/InputXML.xml"
docs = []
with open(document_path, encoding = 'utf-8') as file:
    doc = file.read()

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct", token = hf_token)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
tokens = tokenizer.tokenize(doc)

# print(tokens)
# print(len(tokens))
# print('&&&&&')
# print(tokenizer.convert_tokens_to_string(tokens))

context_window = 4000
i = 0
while i <= len(tokens):
    docs.append(tokens[i : i+context_window])
    i+= context_window

print(docs)
print(len(docs))
for i in range(0, len(docs)):
    docs[i] = tokenizer.convert_tokens_to_string(docs[i])

print(docs)

lang_docs = [Document(page_content=x) for x in docs]
print('------------------')
print(lang_docs)

llm = ChatOllama(model = "llama3.1")
print('&&&')
chain = load_summarize_chain(llm, chain_type = 'map_reduce')
print(';;;;')
#summary = chain.invoke(lang_docs)
print(llm.invoke([("human", "Hi how are you?")]))
print('*****')
start_t = time.time()
summary = chain.invoke(lang_docs)
print(summary)
print('>>>>>>>>')
print(time.time()-start_t)

# Output: Here is a concise summary:\n\nThis XML document appears to be a production schedule for a manufacturing process. It contains information about job assignments, resource availability, task suitability, precedence constraints, setup matrices, and detailed setup instructions for an industrial process or experiment. The document defines multiple tasks, resources, and setup processes with specific times and codes, suggesting it is part of an automated process control system or calibration procedure.
# Avg Time: 480 seconds -> 8 mins
# Not ideal (was split in 4k tokens and used map_reduce langchain summarizer)