from ollama import chat

'''Unfortunately, I couldn't find any information about task 301 in the JSON file you provided. This means that there is no matching data for task 301.

To confirm, I checked the JSON file and found that there are no entries with a key of "id" equal to 301.

Is there anything else I can help you with regarding your JSON file? Do you need assistance with finding any other tasks or would you like more information about how to work with this data?'''
'''I couldn't find any information about task 301 in the JSON file you provided. Unfortunately, there is no matching ID for task 301.

If I don't have enough information to answer your question directly, I'd be happy to help you explore the structure and content of the JSON file further. Would you like me to explain how to navigate or search the data in this file?'''
'''I'd be happy to help you with that question! However, I've searched through the uploaded JSON file and unfortunately, I couldn't find any information about a task with ID 301. It's possible that it might not exist in the file or its details are not specified.

If you'd like, I can take another look at the file to see if there's anything else I can help you with. Would you like me to review the JSON file again or is there something specific you'd like assistance with next?  '''
user_question = 'Is task 301 independent of other tasks?'

prompt = f"""You are an AI assistant helping a user based on queried information.

Politely inform the user that no matches were found for their request.
Mention how there were no tasks found with that ID in the JSON file

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
print('***********')