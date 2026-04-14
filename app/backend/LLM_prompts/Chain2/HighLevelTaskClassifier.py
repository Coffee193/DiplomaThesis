def getPrompt(user_question):
   prompt = """You are a classifier. Your task is to analyze a user's question and pick EXACTLY ONE number from the predefined list below.

You must ALWAYS pick a number from the list below

Possible numbers:
- 1
- 2
- 3

Classification rules:

1. Pick "1" if the question concerns one or more of the following:
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

   return prompt