from ollama import chat

user_question = 'Hi, how are you?'
'''
General Greeting
Greeting Message
'''

user_question = 'Return all tasks'
'''
Task Retrieval List
Get All Tasks
'''

user_question = 'a'
'''
Invalid input
No Answer
Nothing to analyze
'''

user_question = 'asoijkfdjasiojdasoi'
'''
Invalid Input
Invalid question
No relevance found
'''

user_question = '1128978912738291'
'''
Invalid Phone Number
Invalid phone number
'''

user_question = '1'
'''
I'm ready when you are. Please provide the user's question so I can generate a relevant title.
What is cryptocurrency
'''

### Cant handle gibberish

prompt = f"""You are given a user's question. Based only on that question, generate a concise and relevant title that summarizes the core topic.

Requirements:

- Maximum 3 words
- Clear and specific
- No punctuation at the end
- No extra text or explanation
- Output only the title

____________
User Question:
{user_question}"""


llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print('**********************')
print(llm_answer)