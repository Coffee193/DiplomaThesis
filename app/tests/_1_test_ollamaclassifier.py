from ollama import chat

def ClassifyRootSearch(user_question):

   sys_prompt = """You are a classifier. Your task is to analyze a user's question and pick EXACTLY ONE number from the predefined list below.

You must ALWAYS pick a number from the list below

Possible numbers:
- 1
- 2
- 3
- 4
- 5
- 6
- 7

Classification rules:

1. Pick "1" if the user specifically lists the word 'workcenter' in the question.

2. Pick "2" if:
   - the user asks about resources only or their attributes (name, id etc).
   - the question includes availability, when a resource can be used (words like available or can be used have to be present).
   NOTE: a resource might also be refered to as a location like a MELTSHOP.

3. Pick "3" if the user input asks about jobs.  
   IMPORTANT: If the question includes both jobs and tasks (e.g., tasks belonging to a job, job-task relationships, nested task structures within jobs), return "Job".
   Both the keywords 'task' and 'job' need to be present in the question. If they are NOT, do NOT imply any relationships

4. Pick "4" if ALL of the following are satisfied:
   - the user asks about tasks only or their name, ids
   - If an attribute is mentioned it should NOT be about operating time, duration or how long a task takes
   - If the attribute refers to duration, how long a task takes or operating time pick the number "5" instead

5. Pick "5" if the question concerns one or more of the following:
   - references both tasks AND resources (both the words 'resource' and 'task' need to be stated in the user question)
   - which resource can execute a task (both the words 'resource' and 'task' need to be stated in the user question)
   - the location in which (where) a task can be executed
   - how long a task takes, the duration, operating time of a task
   - execution time or duration of a task

6. Pick "6" if the question concerns:
   - the order of tasks
   - dependencies between tasks
   - independencies between tasks
   - which task must happen before/after another task

7. Pick "7" if:
   - the question does not clearly belong to any category above.
   - the question is gibberish or random, single characters or numbers without anything else in the input.
   - If the question is a single number without anything else in the input

Output Format:

{"pick": <int>, "think": <Your thinking process>}

- pick: the number that you picked from the predefined list
- think: Your thinking process as to why you picked that number

Remember:
- Always return ONLY valid JSON and nothing else. Do not explain Youserlf.
- There should be nothing outside the valid JSON: punctuation, semicolons, backticks '`' or '```', the word 'json', any info etc.. Your Output should start with '{' and finish with '}'
   Examples:
   Output: {"pick": 3, "think": "<Your thinking process>"}
   Output: {"pick": 1, "think": "<Your thinking process>"}
"""
   sys_prompt += f"""

___________________
User Question:
{user_question}
"""

   llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': sys_prompt}])
   return llm_answer