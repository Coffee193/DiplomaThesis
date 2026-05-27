def getPrompt(user_question):
    prompt = f"""The user asked a question about job durations. However, they have not uploaded an Input JSON file, which is required to determine which tasks belong to each job.

Your task is to:

1. Politely inform the user that an Input JSON file is needed to answer job duration questions.
2. Briefly explain why: job duration is calculated from the tasks that belong to each job, and this mapping is only available in Input files.
3. Ask them to upload an Input JSON file and try again.

Keep the tone friendly, concise, and supportive.

___________
User Question:
{user_question}"""

    return prompt
