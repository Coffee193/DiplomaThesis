from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

#user_question = "Is there a task to be executed before task with id 483?"
#user_question = "Is there a task to be executed before task 11?"
#user_question = "Is there a task to be executed before 183?"
#user_question = 'Which task should i execute before task 1?'
#user_question = 'What task can i execute after completing task 13?'
#user_question = 'Which task can i do after task 55?'
#user_question = 'Does task 53 require another task to be executed beforehand?'
#user_question = 'Is task 301 independent of other tasks?'
#user_question = "Return all task dependencies"

'''
user_prompt = """You are an information extraction assistant.

The user will provide a question about the order in which tasks need to be executed.

Your goal is to analyze the user's question and determine whether they are asking about a specific task identified by an attribute (id).

Instruction:

1. If the user refers to a specific task by its id:

- Set "attribute" to true
- Extract the id value mentioned in the question

2. Then determine the intent of the question:

- "before" -> if the user is asking about tasks that must be executed before the given task OR if the task requires something beforehand.
- "after" -> if the user is asking about tasks that can be executed after the given task.
- "both" -> if the user is asking whether the task is independent (i.e., no dependency before or after).

3. If the user is not asking about a specific task id, return: {"attribute": false} only

Important rules:

- Always return a valid JSON object only
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Be consistent with lowercase values: "id", "attribute"
- If no specific attribute (id) is identified, return only {"attribute": false}
- Always prioritize intent detection from the question wording.
- Treat phrases like:
    - "before", "prior to", "require first" -> "before"
    - "after", "following", "next" -> "after"
    - "independent", "standalone", "no dependencies" -> "both"
- Only extract numeric IDs explicitly mentioned.

Examples:

-----
User question: "Is there a task to be executed before task 483?"
Output: {"attribute": true, "id": 483, "order": "before"}
-----
User question: "What task can I execute after completing task 13?"
Output: {"attribute": true, "id": 13, "order": "after"}
-----
User question: "Is task 11 independent of other tasks?"
Output: {"attribute": true, "id": 11, "order": "both"}
-----
User question: "Does task 53 require another task to be executed beforehand?"
Output: {"attribute": true, "id": 53, "order": "before"}
-----
User question: "List the order in which tasks need to be executed"
Output: {"attribute": false}"""

user_prompt+=f"""

____________________
User Question:
{user_question}"""

print(user_prompt)
print('==============')

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': user_prompt}])

print('**********************')
print(len(tokenizer.tokenize(json.dumps(user_prompt))))
aa = llm_answer.message.content
print(aa)
print(aa.replace('\n', ''))
'''

def getPrompt(user_question):
    user_prompt = """You are an information extraction assistant.

The user will provide a question about the order in which tasks need to be executed.

Your goal is to analyze the user's question and determine whether they are asking about a specific task identified by an attribute (id).

Instruction:

1. If the user refers to a specific task by its id:

- Set "attribute" to true
- Extract the id value mentioned in the question

2. Then determine the intent of the question:

- "before" -> if the user is asking about tasks that must be executed before the given task OR if the task requires something beforehand.
- "after" -> if the user is asking about tasks that can be executed after the given task.
- "both" -> if the user is asking whether the task is independent (i.e., no dependency before or after).

3. If the user is not asking about a specific task id, return: {"attribute": false} only

Important rules:

- Always return a valid JSON object only
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Be consistent with lowercase values: "id", "attribute"
- If no specific attribute (id) is identified, return only {"attribute": false}
- Always prioritize intent detection from the question wording.
- Treat phrases like:
    - "before", "prior to", "require first" -> "before"
    - "after", "following", "next" -> "after"
    - "independent", "standalone", "no dependencies" -> "both"
- Only extract numeric IDs explicitly mentioned.

Examples:

-----
User question: "Is there a task to be executed before task 483?"
Output: {"attribute": true, "id": 483, "order": "before"}
-----
User question: "What task can I execute after completing task 13?"
Output: {"attribute": true, "id": 13, "order": "after"}
-----
User question: "Is task 11 independent of other tasks?"
Output: {"attribute": true, "id": 11, "order": "both"}
-----
User question: "Does task 53 require another task to be executed beforehand?"
Output: {"attribute": true, "id": 53, "order": "before"}
-----
User question: "List the order in which tasks need to be executed"
Output: {"attribute": false}"""
    user_prompt+=f"""

____________________
User Question:
{user_question}"""
    
    return user_prompt