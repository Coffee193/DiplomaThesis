from ollama import chat

'''You should execute task 5. 
id: 5
name: vuvuvu
I will list all the relevant data below.
(DATA)

Would you like me to explain any of the attributes in the data or help with anything else?'''

'''You should first execute task "id: 5 name: vuvuvu".

(DATA)

Would you like me to help with anything else, or would you like more information about the tasks?'''

ret_val = {'id': 5, 'name': 'vuvuvu'}
user_question = 'Which task should i execute before task 1?'

'''To complete task 13, you should first execute task id: 723, name: ROLLING.

Later, I'll list all the relevant information for your reference, including:

(DATA)

Is there anything else I can help you with regarding tasks or their execution sequence?'''

'''To find out what task you can execute after completing task 13, I'm going to search for the tasks related to id: 13. The next task that can be executed is ROLLING. You will need to complete task id: 723.

(DATA)

Would you like me to help you with anything else?'''

'''You should execute task 723 (ROLLING) after completing task 13.

I'll list all the relevant information as follows:

(DATA)

Is there anything else I can help you with regarding your tasks or would you like more details on any of these tasks?'''

'''To complete task 13, you should first execute task 723 (ROLLING) before executing another task.

I will now list all the relevant information in one dataset:
(DATA)

Would you like me to assist with anything else? Do you have any other tasks or questions about the JSON file?'''

'''You should execute task 723 (ROLLING) after completing task 13.

(DATA)

Is there something else I can help you with?'''

ret_val = {'id': 723, 'name': 'ROLLING'}
user_question = 'What task can i execute after completing task 13?'

''''''

user_question = "Is there a task to be executed before task 11?"
info = 'Execute task 675 before task 11'

user_question = 'Does task 584 need to be executed before 585?'
info = 'Execute task 584 before 585'

'''
prompt = f"""You are an AI assistant helping a user based on queried information.

ALWAYS answer the user's question DIRECTLY. Via API calls you were provided the following task, which is the answer to the user's question:
    id: {ret_val['id']}"""
if('name' in ret_val):
    prompt += f"""
    name: {ret_val['name']}"""

prompt += f"""
Do NOT think about it, THAT task is the answer AND you MUST include it in your response (that is the tasks the user should execute before/after referenced task).
Form your response accordingly so that you anwer to the user's question using that task (AlWYAS mention its ID).
Do NOT be verbose.
NEVER create lists of items or dictionaries or bullet points
Be direct: (before/after) you should execute etc.. AND NEVER mentioned TASKS (ids, names) that are NOT given to you 

Then say how you'll list all the retrieved information WITHOUT saying anything else, and follow the below guidelines:

    - At an appropriate and natural point in your answer, mention how you're going to list the relevant data and upon listing them put the placeholder (DATA)
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat (DATA) as a standalone block (like a table or dataset), NEVER part of a sentence.
    - (DATA) contains a list of all the information retrieved, so print it only ONCE in your output.
    - (DATA) represent the information the user is asking for.
    - NEVER output lists of information that represent the data.
    - NEVER NEVER create lists, or bullet-like items that are supposed to respresent the data the user is searching for. The palceholder (DATA) is enough to give a complete overview of that data
    - The placeholder needs to ALWAYS be EXACTLY written as: (DATA)
    - If the user wants a specific attribute returned (name, id etc..) do NOT place (DATA) as part of a sentence 

Additional rules:

- Never mention “length,” “API,” “retrieved data,” or “placeholders.”
- Be polite, clear, and user-friendly in tone.
- At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).
- You are searching a JSON file the user uploaded NOT some database
____________________
User Question:
{user_question}"""
'''

'''You can execute task 790 after completing task 13.

I will list all the relevant tasks:
(DATA)
'''

'''You can execute task 790 after completing task 13.

I will list all the relevant tasks:
(DATA)'''

user_question = 'What task can i execute after completing task 13?'
info = 'Execute task 13 before task 790'

'''To determine if task 535 is independent of task 901, we can examine their relationship. Since task 535 must be executed before task 901, they are dependent on each other.

I will list the relevant data below:

(DATA)

Is there anything else I can help you with regarding tasks or their relationships?'''

'''Task 535 must be executed before task 901, so it is not independent.

I will list the relevant data:
(DATA)

Do you need help with anything else? Would you like me to explain why this is the case or provide more details about these tasks?'''

user_question = "Is task 535 independent of task 901"
info = 'Execute task 535 before task 901'

user_question = "should i execute task 535 before or after task task 901"
info = 'Execute task 535 before task 901'

prompt = f"""You are an AI assistant helping a user based on queried information.

ALWAYS answer the user's question DIRECTLY based on the following info: 
______________
Info:
{info}

- DO NOT mention that you were provided that information. NEVER NEVER mention the Info
- Always answer directly without being verbose but ensure completeness mentioned the task ids
- That information is ALWAYS enough to anwer the user's question. Be straight to the point

Then say how you'll list all the retrieved information WITHOUT saying anything else, and follow the below guidelines:

    - At an appropriate and natural point in your answer, mention how you're going to list the relevant data and upon listing them put the placeholder (DATA)
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat (DATA) as a standalone block (like a table or dataset), NEVER part of a sentence.
    - (DATA) contains a list of all the information retrieved, so print it only ONCE in your output.
    - (DATA) represent the information the user is asking for.
    - NEVER output lists of information that represent the data.
    - NEVER NEVER create lists, or bullet-like items that are supposed to respresent the data the user is searching for. The palceholder (DATA) is enough to give a complete overview of that data
    - The placeholder needs to ALWAYS be EXACTLY written as: (DATA)
    - If the user wants a specific attribute returned (name, id etc..) do NOT place (DATA) as part of a sentence 

At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).

Additional rules:

- Never mention “length,” “API,” “retrieved data,” or “placeholders.”
- Be polite, clear, and user-friendly in tone.
- At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).
- You are searching a JSON file the user uploaded NOT some database
____________________
User Question:
{user_question}"""

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print(llm_answer)
print('**********************')