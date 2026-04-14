from ollama import chat

'''It looks like we've found one result for your question. We have (DATA).

For that specific "task" (id: 584), it appears that its execution status is dependent on another task, which is indeed "task" (id: 585). The relationship between these two tasks indicates that "task" (id: 584) does need to be executed before "task" (id: 585).

Is there anything else I can help you with regarding the execution order of your tasks?'''

'''The relevant information for this question is:

(DATA)

Yes, it appears that task 584 needs to be executed before task 585.'''

user_question = 'Does task 584 need to be executed before 585?'
len_data = 1

'''Yes, you can find that information in (DATA).

I'd be happy to help with anything else. Would you like me to clarify the details of any specific "tasks"?'''

'''Yes, based on the information in your JSON file, (DATA)

Would you like me to explain how this data relates to the tasks or provide further assistance with anything else?'''

user_question = "Is there a task to be executed before task with id 483?"
len_data = 1

'''You can find the tasks to consider executing before task 1 in the following list: 
(DATA)

Is there anything else I can help you with regarding these tasks or would you like more information about them?'''

'''According to the information, tasks:

(DATA)

May I help you understand how these tasks relate to each other or would you like me to assist with something else?'''

user_question = 'Which task should i execute before task 1?'
len_data = 1

'''Yes, based on the information I have, (DATA)

Would you like me to clarify any specific details about these tasks or help with anything else?'''

'''Yes, based on the tasks, it appears that task 584 needs to be executed before task 585.

(DATA)

Would you like me to provide more details about these tasks or help with anything else?'''

'''Yes, task 584 needs to be executed before task 585.

I will list all the relevant data below:

(DATA)

Is there anything else I can help you with regarding these tasks?'''

'''Yes, task 584 does need to be executed before 585.

I will list all relevant information below in a single block:

(DATA)

Would you like me to provide more details about the execution order of these tasks or assist with anything else?'''

user_question = 'Does task 584 need to be executed before 585?'
len_data = 1

prompt = f"""You are an AI assistant helping a user based on queried information.

You are given only the length of retrieved results, not the actual data.

ALWAYS answer the user's question DIRECTLY positively, affirmatively.

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
- Do NOT assign meaning to the words: “tasks”
    - This is simply a key and must not influence your wording unless the user explicitly refers to it
    - NEVER replace this words with other words such as "position", "opportunities" or any other word.
    - Refer to it STRICTLY by key
    - Write this key by its name: "tasks" ONLY. NEVER write things like: "task openings", "task listings" simply write "tasks"
- You are searching a JSON file the user uploaded NOT some database

____________________
Fetched Data Length:
{len_data}

____________________
User Question:
{user_question}"""

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content

print(llm_answer)
print('**********************')