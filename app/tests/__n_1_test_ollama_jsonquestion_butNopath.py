from ollama import chat

user_question = 'Return all tasks'

prompt = f"""The user is asking for information about a JSON file, but no JSON file has been provided in the conversation. Clearly inform the user that no JSON file has been uploaded yet. Then, politely instruct the user to upload the JSON file so you can analyze it and help with their request. Keep the response concise and helpful, and avoid making assumptions about the file's contents.

Instructions:
- Do NOt say phrases like: "we haven't discussed a specific JSON file"

____________
User Question:
{user_question}"""

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print('**********************')
print(llm_answer)