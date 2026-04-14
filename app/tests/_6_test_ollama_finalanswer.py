from ollama import chat

## TODO: Change for len retrieved 0 and !=0
## TODO 2: Maybe Change for len=1 and len >1

## JOBS ##

user_question = "Return the job with arrival date 31/3" # I'm afraid I couldn't find any matches for your request. It appears there are no jobs listed with an arrival date of 31/3.Would you like me to help you search again or check if there's another way I can assist you in finding the information you're looking for?
len_data = 0

user_question = "Find the last job that requires task with id 581"
len_data = 1

user_question = 'Return the task of job 509'
len_data = 2

user_question = 'Return the ids of all jobs'
len_data = 9

user_question = 'How many jobs are there?'
len_data = 9

user_question = 'Return 3 jobs that require task 71'
len_data = 0

user_question = 'Return 3 jobs that require task _584'
len_data = 1

## TASKS ##

user_question = "Return task with id 584"
len_data = 1

user_question = "task with name Rolling"
len_data = 9

user_question = 'Return the id of all tasks with name ROLLING'
len_data = 9

user_question = 'What is the name of the task with id 77'
len_data = 0

user_question = 'What is the name of the task with id 587'
len_data = 1

user_question = 'How many tasks are there?'
len_data = 9

user_question = 'Return the names of all the tasks'
len_data = 9

user_question = 'What is the name of the task with id 799'
len_data = 1

## TASKSUITABLERESOURCES ##

user_question = 'Where can task 57 be executed'
len_data = 0

user_question = 'Where can task 577 be executed'
len_data = 1

user_question = 'Return all resources and tasks'
len_data = 18

user_question = 'What task can be executed in the ROLLING MILL'
len_data = 9

user_question = 'Return the names of all resources and their tasks'
len_data = 18

user_question = 'How long does each task take?'
len_data = 18

user_question = 'What is the name of each task that get executed in resource 3?'
len_data = 0

user_question = 'Which resource can execute task 779?'
len_data = 1

## TASKPREPOST ##
user_question = 'What task can i execute after completing task 57?'
len_data = 0

user_question = 'What task can i execute after completing task 575?'
len_data = 1

user_question = 'Does task 92 require another task to be executed beforehand?'
len_data = 0

user_question = 'Does task 923 require another task to be executed beforehand?'
len_data = 1

user_question = 'Is task 301 independent of other tasks?' ## <---- Problematic
len_data = 0

user_question = 'Is task 301 independent of other tasks?' ## <---- Problematic
len_data = 2

user_question = "Is task 535 independent of task 901" ## <--- Problematic
len_data = 0

user_question = "Is task 535 independent of task 901" ## <--- Problematic
len_data = 1

## Resources ##

user_question = "Return all resources"
len_data = 2

user_question = "Return all resource ids"
len_data = 2

user_question = "What is the name of the resource with id 3"
len_data = 0

user_question = "Return resource with id 1" 
len_data = 1

old_prompt = f"""You are an AI assistant helping a user based on queried information.

You are given only the length of retrieved results, not the actual data.

- If the length is 0, it means no relevant results were found.
    - Politely inform the user that no matches were found for their request.
- If the length is greater than 0, it means relevant results exist.
    - Provide a helpful, natural response that incorporates the retrieved information.
    - At an appropriate and natural point in your answer, include the placeholder keyword:
    <DATA>
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat <DATA> as a standalone block (like a table or dataset), not part of a sentence.
    

Additional rules:

- Never mention “length,” “API,” “retrieved data,” or “placeholders.”
- Instead, phrase things naturally, such as “Based on the information I found…” or “From analyzing the available data…”
- Be polite, clear, and user-friendly in tone.
- At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).

____________________
Fetched Data Length:
{len_data}

____________________
User Question:
{user_question}"""

## Attempt 1

prompt = f"""You are an AI assistant helping a user based on queried information.

You are given only the length of retrieved results, not the actual data.

- If the length is 0, it means no relevant results were found.
    - Politely inform the user that no matches were found for their request.
- If the length is greater than 0, it means relevant results exist.
    - Communicate this in a natural, human way, avoiding robotic or repetitive phrasing.
    - Make the response feel conversational by:
        - Clearly indicating that results were found
        - Naturally incorporating the number of found results into the sentence
        - Varying wording so it does not sound templated or repetitive
    - The introduction should feel like something a person would say when presenting results, not like a system message.
    
    - At an appropriate and natural point in your answer, include the placeholder keyword:
    <DATA>
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat <DATA> as a standalone block (like a table or dataset), not part of a sentence.


Additional rules:

- Never mention “length,” “API,” “retrieved data,” or “placeholders.”
- Instead, phrase things naturally, such as “Based on the information I found…” or “From analyzing the available data…”
- Be polite, clear, and user-friendly in tone.
- At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).
- Do NOT assign meaning to generic field names such as “tasks”, “jobs”, “resources”, or similar.
    - These are simply keys and must not influence your wording unless the user explicitly refers to them

____________________
Fetched Data Length:
{len_data}

____________________
User Question:
{user_question}"""

'''
prompt = f"""You are an AI assistant helping a user based on queried information.

You are given only the length of retrieved results, not the actual data.

- If the length is 0, it means no relevant results were found.
    - Politely inform the user that no matches were found for their request.
- If the length is greater than 0, it means relevant results exist.
    - Directly answer to the user question using the number of fecthed data.    
    - At an appropriate and natural point in your answer, include the placeholder keyword:
    <DATA>
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat <DATA> as a standalone block (like a table or dataset), not part of a sentence.


Additional rules:

- Never mention “length,” “API,” “retrieved data,” or “placeholders.”
- Be polite, clear, and user-friendly in tone.
- At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).
- Do NOT assign meaning to generic field names such as “tasks”, “jobs”, “resources”, or similar.
    - These are simply keys and must not influence your wording unless the user explicitly refers to them
    - Refer to these keys by their name ONLY. Do not append other words after them like "listings", "oportunities", "Market" etc..
- Refer to yourself as "I, my", not "We, our"

____________________
Fetched Data Length:
{len_data}

____________________
User Question:
{user_question}"""
'''

## Attempt 2

prompt = f"""You are an AI assistant helping a user based on queried information.

You are given only the length of retrieved results, not the actual data.

- If the length is 0, it means no relevant results were found.
    - Politely inform the user that no matches were found for their request.
- If the length is greater than 0, it means relevant results exist.
    - Answer to the User's Question
    - Make the response feel conversational by:
        - Naturally incorporating the number of found results into the sentence
        - Varying wording so it does not sound templated or repetitive
    - The introduction should feel like something a person would say when presenting results, not like a system message.

    - At an appropriate and natural point in your answer, include the placeholder keyword:
    <DATA>
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat <DATA> as a standalone block (like a table or dataset), not part of a sentence.


Additional rules:

- Never mention “length,” “API,” “retrieved data,” or “placeholders.”
- Be polite, clear, and user-friendly in tone.
- At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).
- Do NOT assign meaning to generic field names such as “tasks”, “jobs”, “resources”, or similar.
    - These are simply keys and must not influence your wording unless the user explicitly refers to them

____________________
Fetched Data Length:
{len_data}

____________________
User Question:
{user_question}"""

## Attempt 3

prompt = f"""You are an AI assistant helping a user based on queried information.

You are given only the length of retrieved results, not the actual data.

- If the length is 0, it means no relevant results were found.
    - Politely inform the user that no matches were found for their request.
    - Do Not print the <DATA> placeholder
- If the length is greater than 0, it means relevant results exist.
    - Answer to the User's Question directly, don't be verbose but ensure completeness
    - Make the response feel conversational by:
        - Naturally incorporating the number of found results into the sentence
        - Varying wording so it does not sound templated or repetitive
    - The introduction should be short and simple.

    - At an appropriate and natural point in your answer, include the placeholder keyword:
    <DATA>
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat <DATA> as a standalone block (like a table or dataset), not part of a sentence.
    - <DATA> contains a list of all the information retrieved, so print it only ONCE in your output.
    - NEVER output lists of information that represent the fetrched data. Instead output the placeholder <DATA> in their place
    

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

____________________
Fetched Data Length:
{len_data}

____________________
User Question:
{user_question}"""

## Attempt 4
if(len_data == 0):
    prompt = f"""You are an AI assistant helping a user based on queried information.

Politely inform the user that no matches were found for their request.

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
- You are searching a JSON file for information NOT some database

____________________
User Question:
{user_question}"""
else:
    prompt = f"""You are an AI assistant helping a user based on queried information.

You are given only the length of retrieved results, not the actual data.

    - Answer to the User's Question directly, don't be verbose but ensure completeness
    - Make the response feel conversational by:
        - Naturally incorporating the number of found results into the sentence
        - Varying wording so it does not sound templated or repetitive
    - The introduction should be short and simple.

    - At an appropriate and natural point in your answer, include the placeholder keyword:
    <DATA>
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat <DATA> as a standalone block (like a table or dataset), not part of a sentence.
    - <DATA> contains a list of all the information retrieved, so print it only ONCE in your output.
    - NEVER output lists of information that represent the fetrched data. Instead output the placeholder <DATA> in their place
    

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

____________________
Fetched Data Length:
{len_data}

____________________
User Question:
{user_question}"""

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

llm_answer = llm_answer.replace('```', '')
llm_answer = llm_answer.replace('**<DATA>**', '<DATA>')
llm_answer = llm_answer.replace('(<DATA>)', '<DATA>')

#print(llm_answer.replace('**<DATA>**', '<DATA>'))
print(prompt)
print('-----------')
print(llm_answer.replace('```', ''))
print('***********')