from ollama import chat

user_question = 'Does task 139 need to be executed before 722?'
#user_question = "Is there a task to be executed before task with id 483?"
#user_question = 'Which task should i execute before task 1?'
#user_question = 'Does task 584 need to be executed before 585?'
#user_question = 'Which task should i execute before task 1?'
#user_question = 'What task can i execute after completing task 13?'
#user_question = "Is there a task to be executed before task 11?"
#user_question = 'Does task 584 need to be executed before 585?'
#user_question = 'What task can i execute after completing task 13?'
#user_question = "Is task 535 independent of task 901"
#user_question = 'Is task 301 independent of other tasks?'
#user_question = 'Does task 71 depend on other tasks?'
#user_question = 'What tasks must I execute before or after task 93?'
#user_question = 'Does task 72 need to be executed before or after task 90?'
#user_question = "Is task 535 independent of task 901"

'''
prompt = """You are a classifier. Your task is to categorize a user question into one of the following two classes:

1. retrieval

Classify the question as retrieval if ANY of the following conditions are met:

- The user asks about task dependencies or independencies
- The user asks whether a task can be executed before or after another task
    - IMPORTANT: The question must explicitly mention BOTH "before" AND "after"
- The user requests information about a task (e.g., details, description, status, or properties of a task)

2. bool

Classify the question as bool if:

- The question can be answered with "yes" or "no"
    - IMPORTANT: The question must NOT mention BOTH "before" AND "after"

Output Format:

Return ONLY a valid JSON object in the following format:

{"intent": "<str>", "think": "<Your thinking process>"}

Where <str> is either:
- "retrieval"
- "bool"

Examples:

User Question: "Is task 301 independent of other tasks?"
{"intent": "retrieval", "think": "<Your thinking process>"}
--------------------
User Question: "Does task 72 need to be executed before or after task 90?"
{"intent": "retrieval", "think": "<Your thinking process>"}
--------------------
User Question: "Is task 535 independent of task 901"
{"intent": "retrieval", "think": "<Your thinking process>"}
--------------------
User Question: "Which task should i execute before task 77?"
{"intent": "retrieval", "think": "<Your thinking process>"}
--------------------
User Question: "Is there a task to be executed before task 19?"
{"intent": "bool", "think": "<Your thinking process>"}
--------------------
User Question: "Does task 584 need to be executed before 585?"
{"intent": "bool", "think": "<Your thinking process>"}"""

prompt += f"""
_____________
User Question:
{user_question}
"""
'''
prompt = """You are a classifier. Your task is to determine whether a user question satisfies specific criteria.

Classification Rules:

Return True if the user question meets any of the following conditions:

1. The user asks about task dependencies or independencies.
2. The user asks whether a task can be executed before or after another task.
    - Important: The question must explicitly include BOTH concepts: "before" and "after". BOTH "before" AND "after" have to be present

Return False if none of the above conditions are met.

Output Format:

Return ONLY a valid JSON object:

{"attribute": "<str>", "bool": "<Your thinking process>"}

- You must ALWAYS return a valid JSON object and nothing else. Do NOT explain yourself.
- Your thinking process should be placed in the 'think' key of dictionary
- Do not put anything outside the JSON object.

Examples:

User Question: "Is task 301 independent of other tasks?"
{"attribute": true, "think": "<Your thinking process>"}
--------------------
User Question: "Does task 72 need to be executed before or after task 90?"
{"attribute": true, "think": "<Your thinking process>"}
--------------------
User Question: "Is there a task to be executed before task 19?"
{"attribute": false, "think": "<Your thinking process>"}
--------------------
User Question: "Does task 584 need to be executed after 585?"
{"attribute": false, "think": "<Your thinking process>"}
--------------------
User Question: "Is task 535 independent of task 901"
{"attribute": true, "think": "<Your thinking process>"}
--------------------
User Question: "Which task should i execute before task 77?"
{"attribute": false, "think": "<Your thinking process>"}
--------------------
User Question: "Does task 15 need to be executed before 19?"
{"attribute": false, "think": "<Your thinking process>"}"""

prompt += f"""

_________________
User Question:
{user_question}
"""

print(prompt)
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print(llm_answer)
print('**********************')