def getPrompt(user_question):
    prompt = f"""The user asked a question about job start or end times. However, they have not uploaded both an Input and an Output JSON file, which are required to answer this type of question.

Your task is to:

1. Politely inform the user that both an Input and an Output JSON file are needed to answer job start/end time questions.
2. Briefly explain why: the Input file maps jobs to their tasks, and the Output file contains the actual dispatch times for those tasks. Both are needed to determine when a job starts or ends.
3. Ask them to upload a matching pair of Input and Output JSON files (e.g., InputJSON_1.json and OutputJSON_1.json) and try again.

Keep the tone friendly, concise, and supportive.

___________
User Question:
{user_question}"""

    return prompt
