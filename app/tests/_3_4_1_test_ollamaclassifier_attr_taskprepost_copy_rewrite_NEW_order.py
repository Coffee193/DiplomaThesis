from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

user_question = 'Does task 584 need to be executed before 585?' # 584/585, 3/3 times # {  "attribute": true,  "before": 584,  "after": 585,  "think": "The question is asking about the execution order of tasks, specifically whether task 584 must be executed before task 585."}
user_question = "Is there a task to be executed before task with id 483?" # */483, 3/3 times # {  "attribute": true,  "before": "*",  "after": 483,  "think": "The user is asking about the relationship between tasks based on their IDs. The question mentions 'task with id 483', which implies a specific task ID. However, there's no explicit mention of an ID that must be executed before task 483, so I assume it's any task."}
user_question = "Is there a task to be executed before 183?" # */183, 3/3 times # {  "attribute": true,  "before": "*",  "after": 183,  "think": "The user is asking about the relationship between tasks, specifically if there's a task that needs to be executed before task 183. Since they're not specifying which task should come after, it implies 'any task' or '*'."}
user_question = 'Which task should i execute before task 1?' # */1, 3/3 times # {  "attribute": true,  "before": "*",  "after": 1,  "think": "Detected a question about task relationships using task IDs. User is asking for a specific task to be executed before task 1, so the 'before' value is set to '*' (any task). The 'after' value is set to the ID of task 1."}
user_question = 'What task can i execute after completing task 57?' # 57/* # {  "attribute": true,  "before": 57,  "after": "*",  "think": "Identified a query about execution order and specific task IDs. Extracted the ID of the task that needs to be executed before another task, which is '57'. Since the user asked for a task to execute after completing task 57, used '*' as the task ID for the after relationship."}
user_question = 'Which task can i do after task 55?' # 55/*, 3/3 times # {"attribute": true, "before": 55, "after": "*", "think": "Identified question as asking for a specific attribute-based relationship. Extracted the before and after tasks based on the user's query."}
user_question = 'Does task 92 require another task to be executed beforehand?'# */92, 3/3 times # {"attribute": true, "before": "*", "after": 92, "think": "The user is asking about the relationship between task IDs, specifically whether task 92 requires another task to be executed before it. The question wording indicates a 'before' relationship, so I've prioritized extracting this information."}
user_question = 'Return the ids of all tasks that have to be executed before task 79' # */79, 3/3 times # {  "attribute": true,  "before": "*",  "after": 79,  "think": "The user is asking about the relationship between 'any task' and task 79, indicating a before-after relationship."}
user_question = 'Return the names of all tasks that have to be executed after task 85' #  # {  "attribute": true,  "before": 85,  "after": "*",  "think": "Identified a specific task ID (85) and inferred a relationship with other tasks. The user is asking for tasks that must be executed after task 85, implying a 'before' condition on task 85 itself."}
user_question = 'Return the names of all tasks that have to be executed before task with id 85' # {  "attribute": true,  "before": "*",  "after": 85,  "think": "The user is asking about task relationships, specifically what tasks need to be executed before a task with ID 85. Given the wording of the question, it appears to be referring to 'any task' that must be executed before the task with ID 85."}
user_question = 'Return the names of all tasks that have to be executed before task 85' # {  "attribute": true,  "before": "*",  "after": 85,  "think": "Identified task ID 85 as a specific attribute. Determined that user is asking about tasks to be executed before this task, so used '*' for 'any task'."}  

user_prompt = """You are an information extraction assistant.

The user will provide a question about the order in which tasks need to be executed.

Your job is to determine whether the user is querying a relationship between tasks based on a specific attribute (id), and if so, extract the relationship.

Interpretation Rules:

- If the user refers to an unknown/any task, use "*"
- Always return valid JSON (no explanations, no extra text)


Output Format (STRICT JSON ONLY):

Return a JSON object with the following structure:

If "attribute": true, return:
{"attribute": true, "before": <int or "*">, "after": <int or "*">, "think" <str>}

If "attribute": false, return:
{"attribute": false, "think": <str>}

- attribute: true if the user is asking about task relationships using one or more task IDs. false otherwise
- before: The task ID that must be executed before another task. Use "*" if the user is referring to "any task"
- after: The task ID that must be executed after another task. Use "*" if the user is referring to "any task"

Important rules:

- Always return a valid JSON object only and nothing else. DO not include explanations
- Do not include any explanations or extra text
- Use exactly the keys and structure specified
- If no specific attribute (id) is identified, return only {"attribute": false}
- Always prioritize intent detection from the question wording.
- Only extract numeric IDs explicitly mentioned.
- Although not mentioned in the examples, place your thinking process in the think key of the JSON string

Examples:

-----
User question: "Can task 81 be executed before task 483?"
Output: {"attribute": true, "before": 81, "after": 483, "think": "<Your thinking process>"}
-----
User question: "What task can I execute after completing task 13?"
Output: {"attribute": true, "before": 13, "after": "*", "think": "<Your thinking process>"}
-----
User question: "Is there a task to be executed before task 77?"
Output: {"attribute": true, "before": "*", "after": 77, "think": "<Your thinking process>"}
-----
User question: "Does task 53 require another task to be executed beforehand?"
Output: {"attribute": true, "before": "*", "after": 53, "think": "<Your thinking process>"}
-----
User question: "List the order in which tasks need to be executed"
Output: {"attribute": false, "think": "<Your thinking process>"}
-----
User question: "Does task 90 require task 88 to be executed afterwards?"
Output: {"attribute": true, "before": 90, "after": 88, "think": "<Your thinking process>"}
-----
User question: "Return the ids of all tasks that need to be done after task 37"
Output: {"attribute": true, "before": 37, "after": "*", "think": "<Your thinking process>"}
-----
User question: "Return the names of all tasks that need to be done after task 91 has finished"
Output: {"attribute": true, "before": 91, "after": "*", "think": "<Your thinking process>"}
-----
User question: "Return the names of all tasks that must have finished before task 32"
Output: {"attribute": true, "before": "*", "after": 32, "think": "<Your thinking process>"}"""

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
