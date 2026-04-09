from ollama import chat

user_question = "Return the job with arrival date 31/3" # false 3/3 times # {"attribute": false, "think": "The user wants to return the full job object, but they specified a condition (arrival date) that will be used for filtering. Since it's not about returning a specific attribute of the job, I set 'attribute' to false and left out the 'return' value."}
user_question = "List all jobs" # false 3/3 times # {"attribute": false, "think": "The user wants to retrieve all jobs without specifying any filtering conditions or specific attributes. Therefore, the entire job object should be returned."}
user_question = "Give me the jobs" # false 3/3 time # {"attribute": false, "think": "The user wants all jobs returned without specifying any attribute to be extracted. Therefore, I will return the entire job object for each job."}
user_question = "Return the job with id 300" #  false 3/3 times # {"attribute": false, "think": "The user wants to return the entire job object, so 'attribute' is set to false. The key 'id' was mentioned in the question, but according to the rules, it doesn't affect what's returned."}
user_question = "Return the job with id _300" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire job object, even if filtered by some condition. The specific condition mentioned is the job's id."}
user_question = "Are there any jobs with arrival date 31 2" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire job object(s) where the arrival date is 31/2 (assuming this is a specific format), so 'attribute' is set to False and there's no need for a 'return' value."}
user_question = "List jobs with id 295" # false 3/3 times # {"attribute": false, "think": "The user wants to return all attributes of the job(s) with id 295. Since it's asking for a list and doesn't specify which attribute to return, I'll set 'attribute' to False, indicating that they want the full job object returned."}
user_question = "Find jobs that require task 581" # false 3/3 times # {"attribute": false, "think": "The user wants to find all jobs that match a certain condition (requiring task 581), so I assume they want the entire job object returned."}
user_question = "Find jobs that require task with id 581" # false 3/3 times # {"attribute": false, "think": "The user is asking to find jobs, which implies returning the entire job object. The condition 'require task with id 581' is a filtering condition, but it does not affect what attributes are returned."}
user_question = "Find the last job that requires task with id 581" # false 3/3 times # {"attribute": false, "think": "Since the user is asking for a specific task id (581) and then using 'the last job' which implies returning the full job object, I'm assuming the user wants to return the entire job object filtered by the specified condition."}
user_question = "Return the first job" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire job object without specifying any attribute or condition."}
user_question = "Return the job at index 5" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire job object. Since they mentioned 'at index', it implies a filtering condition but since we're focusing only on what is returned and not the conditions, the entire job will be returned."}
user_question = "Return the first job that requires the task with id 580" # false 3/3 times # {"attribute": false, "think": "The user wants to return the full job object because they mentioned 'the first job', which implies they want all attributes of a single job."}
user_question = "Return job 5" #<---implies id here # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire job object, so I set 'attribute' to False. The 'return' field is empty since it's not specified which attribute to return."}
user_question = "Return 4 jobs" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire job object for a specified number of jobs, but the question doesn't specify which attributes or conditions to apply. Therefore, I assume they want to see all relevant information about each job."}
user_question = "Return me the FROM BILLET job" #<---understand theres name here # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire job object. The keyword 'job' suggests that they want a specific job returned, and the phrase 'FROM BILLET' indicates the name of the job they are looking for."}
user_question = 'Return the job with id 509' # false 1/1 times # {"attribute": false, "think": "The user wants to return the entire job object because they specified 'the job', which implies they want all attributes of the job. The id is used as a condition for filtering the jobs, but it does not imply that only the id should be returned."}
user_question = 'Return all jobs with name: from billet' # false 2/2 times # {"attribute": false, "think": "The user wants to return the entire job object for jobs with a specific name, so 'attribute' is set to False. Since the question asks for 'all jobs', it implies returning the full job object, not just a specific attribute."}
#user_question = 'Return all jobs with arrivaldate 31 3'
#user_question = 'Return all jobs with due date 31 march' # 
user_question = 'Return all jobs that require task 574' # false 2/2 times # {"attribute": false, "think": "The user wants to return all jobs, so 'attribute' is set to false. The question mentions 'require task 574', but since the goal is to determine what's being returned and not filtered conditions, I didn't include a 'return' value in this case."}
#user_question = 'Return job 299' # 
#user_question = 'Return 299 job' # 
#user_question = 'Return 299 jobs'  # 
user_question = 'Return the name of job 52' # name 3/3 times # {"attribute": true, "return": "name", "think": "The user wants to return a specific attribute from a job, so I'm assuming they want to extract a value from the 'job' dictionary. The keyword 'name' indicates that they're looking for the 'name' attribute of the job with id 52."}
user_question = 'What is the name of job 277' # name 3/3 times # {"attribute": true,"return": "name","think": "The user wants to retrieve a specific attribute from a job object. The question specifies 'the name', which implies they want the value associated with the 'name' key in the job dictionary."}
user_question = 'Return the name of job that require task 55' # name 2/2 times # {"attribute": true, "return": "name", "think": "The user wants to return a specific attribute of a job. The keyword 'name' is explicitly mentioned in the question, indicating that the user wants to retrieve the name of the job. The phrase 'require task 55' suggests that filtering by this condition might be necessary, but it's not relevant to determining what the user wants returned."}
user_question = 'Return 3 jobs that require task 71' # false 1/1 times # {"attribute": false, "think": "The user wants to return the entire job object for jobs that require task 71. No specific attribute is mentioned, so it's assumed to be the full job."}
user_question = 'Return the ids of all jobs' # id 1/1 times # {"attribute": true, "return": "id", "think": "The user wants to return a specific attribute of each job, and since 'ids' is not specified in the question, I assume they want the 'id' attribute. The keyword 'all' suggests that they want all jobs returned, but according to the rules, this should be handled as returning a specific attribute."}

prompt = """You are an information extraction assistant.

The user will provide a question about the jobs.

Each job is basically a dictionary that contains the following keys:

- name: The name of the job
- arrivaldate: The earliest date the job can start
- duedate: The latest date the job should be finished
- task: The id of the tasks executed during the job
- workcenter: The id of the workcenter where the job will be executed
- id: The id of the job

Your task is to analyze the user's question and determine what the user wants returned:

- A specific attribute of a job (e.g., name, id, duedate, etc.), OR
- The entire job object

Rules:

- Focus ONLY on what the user wants returned, not on filtering conditions.
- If the user wants for a specific attribute returned (e.g., "name", "task", "duedate"), set "attribute": true and specify which attribute in "return".
- If the user wants the full job (even if filtered by some condition like id) returned, set "attribute": false.
- The "return" field must ONLY be one of the valid keys listed above AND cannot be anything else.
- If "attribute": false, do NOT include a "return" value.
- Never assume the user wants an attribute returned unless its explicitly specified in the user question. It MUST BE mentioned by its key (name, id etc.).

Remember:
You are identifying what the user wants RETURNED. That is your goal

Output format:

Return ONLY a valid JSON object:

{"attribute": <boolean>, "return": "<string>", "think": "<string>"}

- You must ALWAYS return a valid JSON object and nothing else. Do NOT explain yourself.
- Your thinking process should be placed in the 'think' key of dictionary
- Do not put anything outside the JSON object.

Examples:

User: "Return the name of the job with id 63"
Output: {"attribute": true, "return": "name", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return the job with id 73"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "What tasks can be executed in job 33?"
Output: {"attribute": true, "return": "task", "think": "<Your thinking process>"}
------------------------------------------------
User: "What is the name of the job with id 12?"
Output: {"attribute": true, "return": "name", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all jobs"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "What is the duedate of job 502"
Output: {"attribute": true, "return": "duedate", "think": "<Your thinking process>"}
------------------------------------------------
User: "Find jobs that require task 581"
Output:{"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Return the tasks of jobs with name ROLLING"
Output:{"attribute": true, "return": "task", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return the FROM BILLET job"
Output:{"attribute": false, "think": "<Your thinking process>"}"""

prompt += f"""

____________________
User Question:
{user_question}"""

#print(prompt)
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
print(llm_answer)
print(llm_answer.replace('\n', ''))
print('***********')