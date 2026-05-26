def getPrompt(user_question, extracted_date):
    prompt = f"""The user asked a question that references a deadline or "complete by" date. However, the date they provided does not exist on the calendar.

The date extracted from their question was: "{extracted_date}"

Your task is to:

1. Politely inform the user that the date they mentioned is not a valid calendar date.
2. Give a brief explanation of why (e.g., "November only has 30 days", "February only has 28 or 29 days").
3. Ask them to rephrase their question using a valid date.

Keep the tone friendly, concise, and supportive. Do not blame the user.

___________
User Question:
{user_question}"""

    return prompt
