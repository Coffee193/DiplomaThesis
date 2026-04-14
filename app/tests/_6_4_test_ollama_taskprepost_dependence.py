from ollama import chat

'''According to the JSON file you provided, task 301 is indeed marked as an independent task. This means it can be completed without relying on the completion or progress of other tasks.

Would you like me to check if there are any specific dependencies mentioned for task 301? Or perhaps review the entire list of tasks with you?'''

'''Let me check that for you!

According to the JSON information provided, Task 301 is indeed an independent task. It does not depend on any other task for its execution.

Would you like me to help you with anything else or review more details about Task 301?'''

user_question = 'Is task 301 independent of other tasks?'

'''Let me check the information about task 71 in the JSON file you provided.

Task 71 does not directly depend on any other tasks. Its execution is independent of other tasks.

Would you like to know more about task 71 or see its dependencies with tasks that it affects instead?'''

'''No, task 71 does not depend on any other tasks. Its execution is independent.

Would you like me to check if task 72 has similar dependencies or need help with anything else?'''

user_question = 'Does task 71 depend on other tasks?'

'''Task 93 is an independent task, meaning its execution does not depend on other tasks.

There are no tasks that need to be executed before or after Task 93. It can be run independently without affecting the status of any other tasks.

Would you like me to provide more information about Task 93 or help with anything else?'''

'''Based on our analysis of the JSON file you uploaded, we found that Task 93 is an independent task. This means its execution does not depend on other tasks.

There are no specific tasks that need to be executed before or after Task 93.

Would you like me to help with anything else? For example, would you like a detailed description of Task 93 itself?'''

user_question = 'What tasks must I execute before or after task 93?'

'''The execution of Task 72 is independent of Task 90. This means that Task 72 does not require any output from Task 90, and vice versa.

Do you have any other questions about the tasks in the JSON file, or would you like me to help with anything else?'''

'''Task 72 and Task 90 have no dependency on each other. They can be executed independently, without affecting the outcome of one another.

Do you need help understanding any specific dependencies within your JSON file or would you like me to assist with anything else?'''

user_question = 'Does task 72 need to be executed before or after task 90?'

'''After reviewing the JSON file you uploaded, I can confirm that Task 535 does not depend on the execution of Task 901. The execution of Task 535 is not contingent upon the completion or status of Task 901.

Would you like to know more about how these tasks interact with each other or would you like help with something else?'''

'''After reviewing the uploaded JSON file, I found that the execution of Task 535 does not depend on the execution of Task 901. In other words, completing one task will not affect the outcome or success of the other.

Would you like me to help with anything else? Do you need assistance comparing dependencies between any specific tasks or resources?'''

user_question = "Is task 535 independent of task 901"

target = 'oidjkf'
if target == '*':
    dependence_text = "Politely inform the user that the requested task is independent (its execution does NOT depend on other tasks)"
else:
    dependence_text = "Politely inform the user that the requested task is independent of the other task and vice versa (its execution does NOT depende on the execution of the other task)"

prompt = f"""You are an AI assistant helping a user based on queried information.

{dependence_text}

Answer to the user's question directly without being verbose while ensuring completeness.

Additional rules:

- Never mention “length,” “API,” “retrieved data,” or “placeholders.”
- Be polite, clear, and user-friendly in tone.
- At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).
- Do NOT assign meaning to the words: “tasks”, “jobs”, “resources”, or similar.
    - These are simply keys and must not influence your wording unless the user explicitly refers to them
    - NEVER replace any of these words with other words such as "position", "opportunities" or any other word.
    - Refer to them STRICTLY by key
    - Do NOT EVER append other words to them such as "listings", "openings", "etc.."
    - Do NOT EVER mix these words. Refer to jobs as jobs, to tasks as tasks, to resources as resources
- You are searching a JSON file the user uploaded NOT some database

____________________
User Question:
{user_question}"""

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print(llm_answer)
print('**********************')