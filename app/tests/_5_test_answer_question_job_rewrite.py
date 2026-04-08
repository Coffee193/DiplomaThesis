from ollama import chat
from transformers import AutoTokenizer

dict_list = [{'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_584'}, {'refid': '_585'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_299'}, {'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_574'}, {'refid': '_575'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_294'}, {'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_578'}, {'refid': '_579'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_296'}, {'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_587'}, {'refid': '_586'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_300'}, {'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_583'}, {'refid': '_582'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_298'}, {'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_577'}, {'refid': '_576'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_295'}, {'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_590'}, {'refid': '_591'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_302'}, {'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_580'}, {'refid': '_581'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_297'}, {'name': 'FROM BILLET', 'description': None, 'arrivaldate': {'day': 9, 'month': 2, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'duedate': {'day': 31, 'month': 3, 'year': 2026, 'hour': 0, 'minute': 0, 'second': 0}, 'jobtaskreference': [{'refid': '_588'}, {'refid': '_589'}], 'jobworkcenterreference': {'refid': 'WC'}, 'id': '_301'}]

### JOBS ###
# user_question = "Return the job with arrival date 31/3"
'''Let's see what I can find for you.

It looks like there are no relevant results matching your question in the provided data. I've reviewed the list, but unfortunately, there doesn't seem to be any entries related to a specific job with an arrival date of 31/3. If you're looking for information on a different topic or have another query, feel free to ask and I'll do my best to assist you!'''
user_question = "List all jobs"

prompt_old = f"""You are given:

1. A list of dictionaries (data) containing information about a specific job.
2. A user question (question) related to that job.

Your task is to answer the question using only the information available in the provided data, while maintaining a helpful and slightly conversational tone.

Instructions:
- Carefully analyze the list of dictionaries and identify all entries relevant to the user’s question.
- Provide a clear, accurate, and slightly detailed answer based strictly on the provided data.
- Use natural, conversational phrasing (e.g., “Sure thing…”, “Here’s what I found…”, “It looks like…”).
- If relevant results are found:
    - Clearly present them.
    - Optionally introduce them with a short explanatory sentence.
    - Include the matching dictionary entries exactly as they appear.
- If no relevant results are found:
    - Clearly state that no matching information exists in the data.
    - Add a polite and helpful follow-up, such as suggesting the user try another query.
- Do NOT use any external knowledge or make assumptions beyond the provided data.
- If the data is insufficient or ambiguous, explain that clearly.
Output Requirements:
- Respond in plain text.
- Be friendly, clear, and slightly verbose without being overly long.
- Structure the answer so it is easy to understand.
- Do not reference that you were passed a dictionary

----------------------
Dictionary List:
{dict_list}

----------------------
User Question:
{user_question}"""

prompt_new = f"""You are an intelligent assistant tasked with analyzing a collection of job-related data and answering user questions based on it.

You will be given:

1. A collection of job information.
2. A user question.

Your responsibilities:

- Carefully analyze the user's question and determine exactly what information is being requested.
- Examine the available job data thoroughly and extract only the relevant information needed to answer the question.
- Provide a clear, accurate, and well-structured response based strictly on the available data.
- Do not mention or imply the format, structure, or source of the data (e.g., do not refer to “dictionaries”, “JSON”, or similar terms). Instead, frame your response as if you conducted a careful review and analysis of available information.
- If the user asks for the entire dataset, return all available information in a clean and organized manner.
- If the user asks for a subset (e.g., filtered results, specific attributes, or summaries), return only those relevant parts.
- If the requested information is not available, politely state that it could not be found based on your analysis.

Tone and style guidelines:

- Always be polite, professional, and helpful.
- Write naturally, as if explaining results from a careful and thoughtful review.
- At the end of every response, include a friendly closing that invites further interaction, such as offering additional analysis, refinement, or more data.

Example closing tone (adapt as needed):

- “Feel free to let me know if you'd like a deeper analysis or help exploring other aspects.”
- “I;d be happy to refine this further or look into additional details—just let me know how I can help.”

Your goal is to deliver precise, relevant, and user-focused answers while maintaining a natural and conversational tone.

____________
User Question:
{user_question}

____________
Jon Data:
{dict_list}"""

prompt = f"""You are an intelligent assistant tasked with analyzing a collection of job-related data and answering user questions based on it.

You will be given:

1. A collection of job entries, each containing:
    - name: the name of the job
    - arrivaldate: the earliest date the job can start
    - duedate: the latest date by which the job should be completed
    - id: the id of the job
    - jobtaskreference: a list of objects, where each object contains:
        - refid: the id of a task that the job can execute
2. A user query.

Your Instructions:

- Carefully analyze the user's question and interpret their intent with precision.
- Examine the available job information thoroughly before answering.
- Provide a clear, accurate, and relevant response based only on the available data.
- Do NOT mention or imply that the data comes from dictionaries, JSON, or any structured format. Instead, phrase your reasoning naturally (e.g., “after closely examining the available information…”).
- Always maintain a polite and helpful tone.

Output Rules:

- If the user asks for all jobs, return the complete set of jobs.
- If the user asks for specific jobs (e.g., filtered by date, id, name, or task reference), return only the relevant subset.
- If the user asks for details, provide those details clearly and concisely.
- If the requested information is not available, politely state that after careful examination, the information could not be found.

Style Guidelines:

- Use natural language explanations where appropriate.
- You may summarize, filter, or organize the information to improve clarity.
- Avoid unnecessary verbosity, but ensure completeness.

Closing Requirement:

Always end your response with a polite and open-ended offer for further assistance, such as:
- “Please let me know if you'd like me to explore this further.”
- “I'd be happy to help with additional analysis or retrieve more details.”
- “How else can I assist you?

____________
User Question:
{user_question}

____________
Jon Data:
{dict_list}”"""

print(prompt)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
print(len(tokenizer.tokenize(prompt)))

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}])
print(llm_answer.message.content)
with open('C:/Users/Chris/Downloads/diplomat/app/tests/_5_output_ollama_test/outputs.txt') as file:
    file.write(user_question)