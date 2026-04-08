from ollama import chat

user_question = "Return task with id 584" # Picked 3, 3/3 times {"pick": 3, "think": "The question is asking to return a task with a specific id, which doesn't concern the location, duration or execution time of a task, nor the order of tasks or their dependencies. Therefore, it falls under 'tasks' but doesn't fit into any other category."}
user_question = "task with name Rolling" # Picked 3, 3/3 times {"pick": 3,"think": "The question only mentions the name of a task and does not concern location, duration, order, or dependencies. It fits into none of the categories for picking options 1, 2, so option 3 is selected."}
user_question = "Return first task with name Rolling" # Picked 3, 3/3 times {"pick": 3, "think": "The question concerns the name of a task, which doesn't fit into any of the previous categories such as location, duration, execution time, or order/dependencies between tasks."}
user_question = "Return first task" # Picked 3, 3/3 times {"pick": 3,"think": "The question 'Return first task' concerns tasks but doesn't fall into any of the categories mentioned in rules 1 and 2 (it's not about execution location or time, nor is it about task order or dependencies). Therefore, according to rule 3, I should pick option 3."}
user_question = "tasks" # Picked 3, 3/3 times {"pick": 3, "think": "The question is asking about tasks in general, without specifying any particular aspect such as execution location, duration, or order. Therefore, it falls under the category of task-related questions that don't fit into the previous categories."}
user_question = "return task 7" # Picked 3, 3/3 times {"pick": 3,"think": "The question concerns tasks but does not fall into any of the previous categories. It's asking for a specific task to be returned, which suggests it's about retrieving information related to a task, rather than its execution order or duration."}
user_question = "return 7 tasks" # Picked 3, 3/3 times {"pick": 3, "think": "The question concerns tasks but does not fall into the categories of location (where) a task can be executed or execution time/duration, nor order in which tasks must be executed. Therefore, it falls under category 3: tasks and doesn't fit any of the previous categories."}
user_question = "return the last task" # Picked 3, 3/3 times {"pick": 3, "think": "The question concerns tasks but does not fall into any of the previous categories related to location, duration, or order of execution."}
user_question = "Return all ROLLING tasks" # Picked 3, 3/3 times {"pick": 3,"think": "The question is asking for a list of tasks with a specific attribute (ROLLING), which doesn't concern the location, duration, or execution time of tasks, nor does it specify any order or dependencies between tasks."}
user_question = "Return the id of all tasks with name ROLLING" # Picked 3, 3/3 times {"pick": 3,"think": "The question is asking for the id of tasks based on their name, which does not involve the location of task execution, duration, or dependencies. Therefore, it falls under the category of 'tasks' and does not fall into any of the previous categories."}
user_question = "What is the name of the task with id 77" # Picked 3, 3/3 times {"pick": 3,"think": "The question concerns tasks but does not fall into any of the previous categories (location, duration, execution time). It specifically asks for the 'name' of a task, which implies some other attribute or metadata about the task."}
user_question = "Return all tasks" # Picked 3, 3/3 times {  "pick": 3,  "think": "The question 'Return all tasks' concerns tasks in general but doesn't ask about location, duration, execution time or order of tasks. Therefore, it falls into the category that doesn't fit any previous one."}
user_question = "Return the name of every task" # Picked 3, 3/3 times {"pick": 3,"think": "The question is asking for information about tasks in general, without specifying any details about execution location, duration, order, or dependencies. This falls under the category of 'tasks and doesn't fall in any of the previous categories'."}

user_question = 'Where can task 57 be executed' # Picked 1, 3/3 times {"pick": 1, "think": "The question concerns the location in which a task can be executed, so I picked option 1."}
user_question = 'Can Task 11 be executed in the MELTSHOP?' # Picked 1, 3/3 times {"pick": 1,"think": "The question concerns the location in which (where) a task can be executed, so it falls under rule 1."}
user_question = 'How long does task 52 take?' # Picked 1, 3/3 times {"pick": 1,"think": "The question concerns the duration of a task, which falls under rule 1. The question is asking how long task 52 takes, indicating that we need to consider the execution time or duration of a task."}
user_question = 'What task can be executed in the ROLLING MILL' # Picked 1, 3/3 times {"pick": 1,"think": "The question concerns where a task can be executed, which falls under the first category."}
user_question = 'What is the operation time for task 73' # Picked 1, 3/3 times {"pick": 1,"think": "The question concerns the duration of a task, which is 'operation time' and it's related to task 73. Therefore I pick option 1."}
user_question = 'What tasks need to operate for more than 30minutes?' # Picked 1, 3/3 times {  "pick": 1,  "think": "The question concerns the duration of a task (operating time), so I picked '1' according to rule 1."}

user_question = "Is there a task to be executed before task with id 483?" # Picked 2, 3/3 times {"pick": 2, "think": "The question concerns the order in which tasks must be executed and which task must happen before another task."}
user_question = "Is there a task to be executed before task 11?" # Picked 2, 3/3 times {  "pick": 2,  "think": "The question concerns the order in which tasks must be executed, specifically which task must happen before another task. This falls under rule 2."}
user_question = "Is there a task to be executed before 183?" # Picked 2, 3/3 times {"pick": 2, "think": "The question concerns the order in which tasks must be executed and specifically asks for a task that must happen before another task."}
user_question = 'Which task should i execute before task 1?' # Picked 2, 3/3 times {"pick": 2,"think": "The question concerns the order in which tasks must be executed, specifically which task should happen before another task."}
user_question = 'What task can i execute after completing task 13?' # Picked 2, 3/3 times {  "pick": 2,  "think": "The question concerns the order in which tasks must be executed and which task must happen before another task."}
user_question = 'Which task can i do after task 55?' # Picked 2, 3/3 times {"pick": 2, "think": "The question concerns the order in which tasks must be executed and the relationship between two specific tasks."}
user_question = 'Does task 53 require another task to be executed beforehand?' # Picked 2, 3/3 times {"pick": 2, "think": "The question concerns the order in which tasks must be executed and dependencies between tasks."}
user_question = 'Is task 301 independent of other tasks?' # {"pick": 2, "think": "The question concerns the independencies between tasks, so according to rule 2, I should pick '2'."}
user_question = "Return all task dependencies" # {"pick": 2,"think": "The question concerns the dependencies between tasks, which falls under rule 2."}
user_question = 'Return the names of all tasks that have to be executed before task 85' # {"pick": 2, "think": "The question concerns dependencies between tasks and specifically which task must happen before another task."}

prompt = """ou are a classifier. Your task is to analyze a user's question and pick EXACTLY ONE number from the predefined list below.

You must ALWAYS pick a number from the list below

Possible numbers:
- 1
- 2
- 3

Classification rules:

1. 5. Pick "1" if the question concerns one or more of the following:
   - the location in which (where) a task can be executed
   - how long a task takes, the duration, operating time of a task
   - execution time or duration of a task

2. Pick "2" if the question concerns:
   - the order in which tasks must be executed
   - dependencies between tasks
   - independencies between tasks
   - which task must happen before/after another task
   - which task must be executed before/after another
   
3. Pick "3" if the question concerns:
    - tasks and doesn't fall in any of the previous categories
    
-> NEVER correlate a number in the question with a Pick option. These are completely irrelevant. If the number 5 is present in the question NEVER ASSUME that you should pick 5.

Output Format:

{'pick': <int>, 'think': <Your thinking process>}

- pick: the number that you picked from the predefined list
- think: Your thinking process as to why you picked that number

Remember:
- Always return ONLY valid JSON and nothing else. Do not explain Youserlf.
- The number you pick must be one of the above. You CANNOT pick a number that is NOT in the possible numbers

Examples:

Input: "Return task with id 584"
Output: {"pick": 3, "think": "<Your thinking process>"}
----------------
Input: "Can Task 11 be executed in the MELTSHOP?"
Output: {"pick": 1, "think": "<Your thinking process>"}
----------------
Input: "Is there a task to be executed before 183?"
Output: {"pick": 2, "think": "<Your thinking process>"}
----------------
Input: "Is task 301 independent of other tasks?"
Output: {"pick": 2, "think": "<Your thinking process>"}"""

prompt += f"""

_____________
User Question:
{user_question}"""

print(prompt)
print('llllllllllllllllll')

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
llm_answer = llm_answer.replace('\n', '')

print(llm_answer)
print(';;;;;;;;;;;')