from ollama import chat
import ollama

try:
    llm_answer = chat('aaa', messages = [{'role': 'user', 'content': 'baubu'}])
except ollama._types.ResponseError:
    print('agugu')

print(llm_answer)