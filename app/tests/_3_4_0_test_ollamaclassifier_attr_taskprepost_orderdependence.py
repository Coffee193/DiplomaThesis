from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

user_question = 'Does task 584 need to be executed before 585?' # order 3/3 times # {"pick": "order", "think": "The user is asking about the execution sequence between two specific tasks."}
#user_question = "Is there a task to be executed before task with id 483?" # order 3/3 times # {"pick": "order", "think": "question wording suggests asking about execution sequence"}
#user_question = "Is there a task to be executed before 183?" # order 3/3 times # {"pick": "order", "think": "The question asks about the execution sequence of tasks, specifically looking for a task that needs to be executed before another one."}
#user_question = 'Which task should i execute before task 1?' # order 3/3 times # {"pick": "order", "think": "The user is asking about the execution sequence of tasks, specifically which one to perform before another."}
#user_question = 'What task can i execute after completing task 57?' # {"pick": "order", "think": "The user is asking about the execution sequence of tasks, specifically what comes after task 57."}
#user_question = 'Which task can i do after task 55?' # {"pick": "order", "think": "The question asks about the execution sequence and what comes next, indicating a need to determine order."}
#user_question = 'Does task 92 require another task to be executed beforehand?'# {"pick": "order", "think": "The question asks about the dependency of a task, specifically whether it requires another task to be executed before it, which indicates an inquiry about execution order."}
#user_question = 'Return the ids of all tasks that have to be executed before task 79' # {"pick": "order", "think": "The question asks about the execution sequence, specifically what tasks need to be executed before another task (task 79), which falls under 'order' classification."}
#user_question = 'Return the names of all tasks that have to be executed after task 85' # {"pick": "order", "think": "The question asks about the sequence of tasks, specifically which tasks need to be executed after task 85."}
#user_question = 'Return the names of all tasks that have to be executed before task with id 85' # {"pick": "order", "think": "Detected keywords 'before' and 'task', indicating a question about execution sequence"}
#user_question = 'Return the names of all tasks that have to be executed before task 85' # {"pick": "order", "think": "The question asks about the execution sequence of tasks, specifically what tasks come before task 85."}
#user_question = 'Is task 301 independent of other tasks?' # dependence 3/3 times # {"pick": "dependence", "think": "Identified keywords 'independent' and 'other tasks', indicating a question about dependencies."}
#user_question = "Return all task dependencies" # dependence 3/3 times # {"pick": "dependence", "think": "The question asks about dependencies between tasks, so it should be classified as 'dependence'"}
#user_question = "Is task 535 independent of task 901" # {"pick": "dependence", "think": "The user is asking about the independence between two specific tasks, which indicates a question about dependencies rather than execution order."}
#user_question = 'Does task 55 has to be executed before or after task 31' # dependence 3/3 times # {"pick": "dependence", "think": "The question asks about both 'before' and 'after', indicating a need to consider dependencies between tasks."}

user_prompt_old = """You are a classifier that analyzes user questions about tasks.

Your goal is to determine whether the question is about:
- "order" → the execution sequence of tasks (e.g., what comes before/after another task)
- "dependence" → whether tasks are dependent or independent of each other

Rules:

- If the question asks about before, after, sequence, next step, execution order, classify as "order".
- If the question asks about dependencies, independence, requirements between tasks, classify as "dependence".

Output format:

Return ONLY a valid JSON object:

{"pick": "<value>", "think": "<Your thinking process>"}

Where <value> is either "order" or "dependence".


Important rules:

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Always prioritize intent detection from the question wording.
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:
-----
User question: "Does task 584 need to be executed before 585?"
Output: {"pick": "order", "think": "<Your thinking process>"}
-----
User question: "Return all task dependencies"
Output: {"pick": "dependence", "think": "<Your thinking process>"}
-----
User question: "Does task 53 require another task to be executed beforehand?"
Output: {"pick": "order", "think": "<Your thinking process>"}
-----
User question: "List the order in which tasks need to be executed"
Output: {"pick": "order", "think": "<Your thinking process>"}
-----
User question: "What task can I execute after completing task 13?"
Output: {"pick": "order", "think": "<Your thinking process>"}
-----
User question: "Is task 11 independent of other tasks?"
Output: {"pick": "dependence", "think": "<Your thinking process>"}"""

user_prompt = """You are a classifier that analyzes user questions about tasks.

Your goal is to determine whether the question is about:
- "order" → the execution sequence of tasks (in a single-direction sense: only before OR only after)
- "dependence" → whether tasks are dependent or independent, OR when both directions (before AND after) are involved

Rules:

- If the question asks about only one direction:
    - "before" → "order"
    - "after" → "order"
- If the question includes both "before" AND "after", classify as "dependence".
- If the question asks about dependencies, independence, requirements between tasks, classify as "dependence".

Output format:

Return ONLY a valid JSON object:

{"pick": "<value>", "think": "<Your thinking process>"}

Where <value> is either "order" or "dependence".

Important rules:

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- Always prioritize intent detection from the question wording.
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:
-----
User question: "Does task 584 need to be executed before 585?"
Output: {"pick": "order", "think": "<Your thinking process>"}
-----
User question: "What task comes after task 10?"
Output: {"pick": "order", "think": "<Your thinking process>"}
-----
User question: "Does task 5 come before or after task 6?"
Output: {"pick": "dependence", "think": "<Your thinking process>"}
-----
User question: "Return all task dependencies"
Output: {"pick": "dependence", "think": "<Your thinking process>"}
-----
User question: "Is task 11 independent of other tasks?"
Output: {"pick": "dependence", "think": "<Your thinking process>"}
-----
User question: "Does task 987 has to be executed before or after task 701?"
Output: {"pick": "dependence", "think": "<Your thinking process>"}
-----
User question: "Does task 102 require another task to be executed beforehand?"
Output: {"pick": "order", "think": "<Your thinking process>"}"""

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
