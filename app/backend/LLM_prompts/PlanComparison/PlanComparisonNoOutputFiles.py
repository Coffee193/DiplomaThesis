def getPrompt(user_question):
    prompt = f"""The user asked a question about comparing plans. However, they have not uploaded at least 2 Output JSON files, which are required to compare plan makespans.

Your task is to:

1. Politely inform the user that at least 2 Output JSON files are needed to compare plans.
2. Briefly explain why: plan comparison requires calculating the makespan (total schedule duration) from each Output file's assignments. With fewer than 2 Output files, there is nothing to compare.
3. Ask them to upload at least 2 Output JSON files and try again.

Keep the tone friendly, concise, and supportive.

___________
User Question:
{user_question}"""

    return prompt
