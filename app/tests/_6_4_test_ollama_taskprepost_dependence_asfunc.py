
def getPrompt(user_question, target):
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

    return prompt