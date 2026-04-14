def getPrompt(user_question):
    prompt = """You previously received a user question, but your response resulted in an invalid (non-JSON) output and caused an error. Your task is to respond to the user in a polite and helpful manner.

Kindly include one or more following points in your response:

1. Inform the user that their question may not have been fully clear, and suggest rewriting it in a clearer and more specific way to help produce a correct response.
2. Mention that the issue might have been temporary (e.g., a transient or seed-related error), and encourage them to simply try again.
3. Advise the user to remove any instructions in their question that force the response into a specific format (such as explicitly requesting a certain output structure), as this may have contributed to the issue.

Do not include point 3 if the user didn't provide any special formatting for the answer in the question

Keep the tone friendly, concise, and supportive. Do not blame the user. Do not mention internal errors or technical details like “invalid JSON” explicitly—refer to it more generally as an issue processing the request."""

    prompt += f"""

___________
User Questtion:
{user_question}"""
    
    return prompt