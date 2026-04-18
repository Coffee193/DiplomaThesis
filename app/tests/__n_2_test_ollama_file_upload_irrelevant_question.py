from ollama import chat

file_name = 'TimesheetData5.json'
'''I'm doing well, thank you for asking! I'm a large language model here to assist with any questions or tasks you may have.

You've also uploaded a JSON file named TimesheetData5.json. If you'd like help analyzing its contents or would like me to summarize the information it contains, just let me know and I'll be happy to assist.'''
'''I'm doing well, thank you for asking! I'm here to assist you with any questions or topics you'd like to discuss.

By the way, we received a JSON file named TimesheetData5.json. If you're interested in exploring its contents, I can help you analyze it, summarize its key points, or even retrieve specific information from it – just let me know how I can assist!'''
user_question = 'Hi, how are you?'

prompt = f"""You are given a user query along with a JSON file upload. The user's question is unrelated to the contents of the JSON file.

Your task:

1. Answer the user's question directly and helpfully, as if the JSON file were not present.
2. After fully answering the question, add a brief, polite note acknowledging that the user has uploaded a JSON file named {file_name}.
3. In that note, offer assistance with the file, such as analyzing it, summarizing it, or retrieving specific information from it.
4. Do NOT analyze, interpret, or make any assumptions about the contents of the JSON file.
5. Keep the tone polite, natural, and helpful.

Structure your response as:

- Main answer to the user's question
- A short follow-up paragraph mentioning the uploaded file and offering help

_____________________
User Question:
{user_question}"""

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print('**********************')
print(llm_answer)