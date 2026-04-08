from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# user_question = "Is there a task to be executed before task with id 483?" # {  "attribute": true,  "id": 483,  "order": "before",  "think": "Identified specific task by its id, determined intent as 'before' based on question wording."}
# user_question = "Is there a task to be executed before task 11?" # {  "attribute": true,  "id": 11,  "order": "before",  "think": "Looking for the id of task 11 in the question. Found it. The user is asking about tasks that must be executed before task 11."}
# user_question = "Is there a task to be executed before 183?" # {"attribute": true, "id": 183, "order": "before", "think": "Looking for specific task id in the question and determining intent as 'before' based on the wording"}
# user_question = 'Which task should i execute before task 1?' # {"attribute": true,"id": 1,"order": "before","think": "Extracted 'task 1' id and determined intent as 'before'"}
# user_question = 'What task can i execute after completing task 13?' # {"attribute": true,"id": 13,"order": "after","think": "The user is asking about tasks that can be executed after a specific task, identified by its id. The keyword 'after' indicates the intent of the question."}
# user_question = 'Which task can i do after task 55?' # {  "attribute": true,  "id": 55,  "order": "after",  "think": "The user is asking about a specific task id, which is 55. They are looking for tasks that can be executed after this task."}
# user_question = 'Does task 53 require another task to be executed beforehand?' # {  "attribute": true,  "id": 53,  "order": "before",  "think": "The user is asking about the dependency of a specific task (task 53), indicating it requires something before execution."}
# user_question = 'Is task 301 independent of other tasks?' # {  "attribute": true,  "id": 301,  "order": "both",  "think": ["identified specific task id", "user asked about independence"]}
# user_question = "Return all task dependencies" # {"attribute": false, "think": "The user is asking for a general overview of task dependencies rather than a specific task id. Returning attribute as false."}
# user_question = 'Return the ids of all tasks that have to be executed before task 79' # {  "attribute": true,  "id": 79,  "order": "before",  "think": "Identified a specific task id, '79', in the question. Analyzing the question wording, it indicates a dependency or requirement for tasks to be executed before this specific task."}
# user_question = 'Return the names of all tasks that have to be executed before task 85' # {  "attribute": true,  "id": 85,  "order": "before",  "think": "user is asking for tasks that must be executed before task 85, will need to query database or task list for dependencies"}

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

- Always return a valid JSON object only and nothing else. DO not include explanations
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
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:

-----
User question: "Is there a task to be executed before task 483?"
Output: {"attribute": true, "id": 483, "order": "before", "think": <Your thinking process>}
-----
User question: "What task can I execute after completing task 13?"
Output: {"attribute": true, "id": 13, "order": "after", "think": <Your thinking process>}
-----
User question: "Is task 11 independent of other tasks?"
Output: {"attribute": true, "id": 11, "order": "both", "think": <Your thinking process>}
-----
User question: "Does task 53 require another task to be executed beforehand?"
Output: {"attribute": true, "id": 53, "order": "before", "think": <Your thinking process>}
-----
User question: "List the order in which tasks need to be executed"
Output: {"attribute": false, "think": <Your thinking process>}
-----
User question: "Return all task dependencies"
Output: {"attribute": false, "think": <Your thinking process>}"""

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