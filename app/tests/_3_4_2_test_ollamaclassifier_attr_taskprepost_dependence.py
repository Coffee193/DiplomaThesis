from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

user_question = 'Is task 13 independent of other tasks?' # 13/*, 3/3 times {"attribute": true, "reference": 13, "target": "*", "think": "The user is asking about task dependencies using one or more task IDs, specifically the task with ID 13, and refers to any other task."}
user_question = "Return all task dependencies" # false 3/3 times {"attribute": false, "think": "The user is asking for a general query about all task dependencies rather than a specific task's dependency"}
user_question = "Is task 535 independent of task 901" # 535/901, 3/3 times # {  "attribute": true,  "reference": 535,  "target": 901,  "think": "The user is asking about the dependencies between two specific tasks, so I'm assuming they're looking for a dependency relationship between these tasks."}
user_question = 'Does task 55 has to be executed before or after task 31' # 55/31, 3/3 times # {    "attribute": true,    "reference": 55,    "target": 31,    "think": "The user is asking about the dependency between two specific tasks, so I extracted their IDs."}
user_question = 'Does task 71 depend on other tasks?' # {  "attribute": true,  "reference": 71,  "target": "*",  "think": "The user is asking about the dependencies of a specific task (task 71) in relation to other tasks, indicated by 'other tasks'."}
user_question = 'What tasks must I execute before or after task 93?' # {  "attribute": true,  "reference": 93,  "target": "*",  "think": "Identified question as task dependency inquiry, extracted reference and target task id"}
user_question = 'Does task 72 need to be executed before or after task 90?' # {  "attribute": true,  "reference": 72,  "target": 90,  "think": "The user is asking about the dependencies of task 72 in relation to another specific task, which is task 90."}

user_prompt = """You are a classifier that analyzes user questions about tasks.

You are given a user question about task dependencies. The tasks are represented as a list of dictionaries, where each task has an id.

Your goal is to determine whether the user is asking about a specific task (by id) in relation to another task (or tasks).

Instructions:

1. Identify if the user is querying based on a specific task id (attribute-based query).
    - If YES → "attribute": true
    - If NO → "attribute": false
2. If "attribute": true, extract:
    - "reference": the main task id the user is asking about
    - "target":
        - the other task id mentioned in the question, OR
        - "*" if the user refers to any task (e.g., "any", "other tasks", "before or after")
3. If "attribute": false, return only:
{"attribute": false}
4. Output must always be valid JSON in the format:
{"attribute": <bool>, "reference": <int>, "target": <int or "*">}

Output format:

Return ONLY a valid JSON object:

If "attribute": true, return:
{"attribute": true, "reference": <int>, "target": <int or "*">, "think": "<Your thinking process>"}

If "attribute": false, return:
{"attribute": false, "think": "<Your thinking process>"}

- attribute: true if the user is asking about task dependencies using one or more task IDs. false otherwise
- reference: The task ID for which he's searching any dependencies
- target: The other task ID. If the question refers to any task, does NOT specify another ID set this to "*".

Important rules:

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Always prioritize intent detection from the question wording.
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:
-----
User question: "Is task 59 dependent on task 37?"
Output:{"attribute": true, "reference": 59, "target": 37, "think": "<Your thinking process>"}
-----
User question: "Does task 55 have to be executed before or after task 31?"
Output: {"attribute": true, "reference": 55, "target": 31, "think": "<Your thinking process>"}
-----
User question: "Return all task dependencies"
Output: {"attribute": false, "think": "<Your thinking process>"}
-----
User question: "Is task 301 independent of other tasks?"
Output: {"attribute": true, "reference": 301, "target": "*", "think": "<Your thinking process>"}
-----
User question: "Return the names of all tasks that have to be executed before or after task 581"
Output: {"attribute": true, "reference": 581, "target": "*", "think": "<Your thinking process>"}"""

user_prompt+=f"""

____________________
User Question:
{user_question}"""

print(user_prompt)
print('==============')

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': user_prompt}])

print('**********************')
#print(len(tokenizer.tokenize(json.dumps(user_prompt))))
aa = llm_answer.message.content
print(aa)
print(aa.replace('\n', ''))
