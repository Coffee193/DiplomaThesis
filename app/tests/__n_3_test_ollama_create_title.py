from ollama import chat
user_question = 'Return all tasks'
'''Task List from JSON File'''
'''Tasks in JSON File'''

user_question = 'Return all Job IDs with arrival date 31/2'
'''Job IDs by Arrival Date'''

user_question = 'Hi, how are you?'
'''Small talk with JSON data'''
'''Small Talk with User'''

user_question = 'asjidjasoidjas'
'''JSON File Analysis'''
'''Understanding JSON data structure'''

user_question = 'aaaaaaaaaaaaaaaaaaa'
'''Extract data from JSON'''
'''JSON Data Extraction'''
'''JSON Data Retrieval Issues'''
'''JSON File Content'''
'''JSON Data Retrieval'''
'''JSON File Information'''
'''JSON File Details'''

user_question = 'a'
'''JSON File Information'''
'''JSON File Contents '''

user_question = '1'
'''Extracting data from JSON'''

###### NOTE: Cannot handle gibberish OR EMPTY question

prompt = f"""You are given a user question and a JSON file. Based only on this information, generate a concise and relevant title for the conversation.

Requirements:

- The title must be no more than 5 words
- It should clearly reflect the main topic or intent
- Keep it short, specific, and to the point
- Do not include punctuation unless necessary
- Do not add explanations—output only the title
- Never mention a database, instead reference the JSON file

_________________
User Question:
{user_question}"""

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print('**********************')
print(llm_answer)