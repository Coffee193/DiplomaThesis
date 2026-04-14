from ollama import chat

user_question = 'Does task 139 need to be executed before 722?' # {"attribute": true, "think": "The question asks about a condition or necessity for task execution, which can be answered with a simple Yes/No."}
user_question = "Is there a task to be executed before task with id 483?" # {"attribute": true, "think": "The question is asking for existence of a task relative to another task, which can be answered with a simple Yes or No."}
user_question = 'Which task should i execute before task 1?'
#user_question = 'Does task 584 need to be executed before 585?'
#user_question = 'Which task should i execute before task 1?'
#user_question = 'What task can i execute after completing task 13?'
#user_question = "Is there a task to be executed before task 11?"
user_question = 'Does task 584 need to be executed before 585?'
#user_question = 'What task can i execute after completing task 13?'
#user_question = "Is task 535 independent of task 901"
#user_question = 'Is task 301 independent of other tasks?'
#user_question = 'Does task 71 depend on other tasks?'
#user_question = 'What tasks must I execute before or after task 93?'
#user_question = 'Does task 72 need to be executed before or after task 90?'
#user_question = "Is task 535 independent of task 901"

prompt = """You are a classifier. Your task is to determine whether a given user question is a boolean question, meaning it can be answered with a simple "Yes" or "No".

Instructions:

- Consider entirely the grammatical structure of the question.
- If the question starts with things like (Can, Is, Are etc..) its a clear indication of boolean questions
- If the question starts with things like (What, Which etc..) its a clear indication of NOT boolean questions

Output Format:

Return ONLY a valid JSON object:

{"attribute": <bool>, "think": "<Your thinking process>"}

- attribute: true if question is boolean, false otherwise

Important rules:

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:
User Question: "Does task 139 need to be executed before 722?"
Output: {"attribute": true, "think": "<Your thinking process>"}
-------------------
User Question: "Is there a task to be executed before task with id 483?"
Output: {"attribute": true, "think": "<Your thinking process>"}
-------------------
User Question: "What task can i execute after completing task 13?"
Output: {"attribute": false, "think": "<Your thinking process>"}
-------------------
User Question: "Which task should i execute before task 19?"
Output: {"attribute": false, "think": "<Your thinking process>"}
-------------------
User Question: "Return the task that I should complete before task 753?"
Output: {"attribute": false, "think": "<Your thinking process>"}"""

prompt += f"""

___________________
User Question:
{user_question}"""


llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print(llm_answer)
print('**********************')