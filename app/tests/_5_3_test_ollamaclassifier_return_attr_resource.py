from ollama import chat

user_question = "Return all resources" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire resource object for all available resources, so 'attribute' is set to False and there's no need to specify a return value."}
user_question = "Return all resource ids" # id 3/3 times # {"attribute": true, "return": "id", "think": "The user wants to return a specific attribute of a resource, which is the id. The keyword 'ids' and the phrase 'all resources' indicate that the user wants every id returned."}
user_question = "Return resouce 2" # false 3/3 times # {"attribute": false, "think": "The user wants to return the full resource, as indicated by 'resource' in the question. There's no mention of a specific attribute to return, so I'm assuming they want the entire object."}
user_question = "Return resouce 1" # false 3/3 times # {"attribute": false, "think": "The user asked to return a resource, but did not specify which attribute. Assuming the entire resource object is wanted."}
user_question = "What is the name of the resource with id 3" # name 3/3 times # {"attribute": true, "return": "name", "think": "The user wants to return a specific attribute, which is 'name'. This attribute must be present in each resource dictionary. The condition (id = 3) is not relevant to determining what to return, only how to filter the results."}
user_question = "Return resource with id 7" # false 3/3 times # {"attribute": false, "think": "The user wants the entire resource object returned because they used 'resource', which typically implies a full object. No specific attribute is mentioned in the question."}
user_question = "Return resource ROLLING MILL" # false 3/3 times # {"attribute": false, "think": "The user wants to return the full resource object, as they mentioned 'resource' without specifying any attributes."}
user_question = "Return resource rolling mill" # false 3/3 times # {"attribute": false, "think": "The user wants to return the entire resource object without any filtering conditions, so 'attribute' is set to False. The key 'rolling mill' in the user's question suggests that they are referring to a specific resource, but since there is no condition specified like 'with id 63', I assume they want all attributes of this specific resource returned."}
user_question = "How many resources are there" # false 3/3 times # {"attribute": false, "think": "The question is asking for information about the count of resources, but it doesn't specify what attribute to return. Therefore, I'm assuming the user wants the entire resource object returned."}
user_question = "Return the first resource" # false 3/3 times # {"attribute": false, "think": "Since the user wants to 'return' the first resource, it's likely they want all attributes of this specific resource, which means the entire object should be returned."}
user_question = "Return 1 resource" # false 1/1 times
user_question = "What are the working periods of resource 1" # period 3/3 time # {"attribute": true, "return": "period", "think": "The user wants to return a specific attribute (period) from a resource. The 'resource' keyword is used, indicating that the user likely wants all attributes returned, but since period is mentioned explicitly, it should be returned instead of the entire object"}
user_question = "When is ROLLING MILL available?" # period 1/1 times # {"attribute": true, "return": "period", "think": "The user wants to know the availability of a specific resource, which implies looking at its period attribute. Since they're asking when it's available, I assume they mean not working, which aligns with the 'period' key."}
#user_question = "Return 1 resources"

prompt = """You are an information extraction assistant.

The user will provide a question about the resources.

Each resource is basically a dictionary that contains the following keys:

- name: The name of the resource
- id: The id of the resource
- period: The non-working periods (the time periods at which the resource is idle, it is NOT working)

Your goal is to analyze the user's question and determine what the user wants returned:

- A specific attribute of a resource (e.g., name, id, period), OR
- The entire resource object

Rules:

- Focus ONLY on what the user wants returned, not on filtering conditions.
- If the user wants for a specific attribute returned (e.g., "name", "id"), set "attribute": true and specify which attribute in "return".
- If the user wants the full resource (even if filtered by some condition like id) returned, set "attribute": false.
- The "return" field must ONLY be one of the valid keys listed above AND cannot be anything else.
- If "attribute": false, do NOT include a "return" value.
- Never assume the user wants an attribute returned unless its explicitly specified in the user question. It MUST BE mentioned by its key (name, id, period).

Remember:
You are identifying what the user wants RETURNED. That is your goal

Output format:

Return ONLY a valid JSON object:

{"attribute": <bool>, "return": "<string>", "think": "<string>"}

- You must ALWAYS return a valid JSON object and nothing else. Do NOT explain yourself.
- Your thinking process should be placed in the 'think' key of dictionary
- Do not put anything outside the JSON object.

Examples:

User: "Return the name of the resource with id 63"
Output: {"attribute": true, "return": "name", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return the resource with id 73"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "What is the name of the resource with id 77?"
Output: {"attribute": true, "return": "name", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all resources"
Output: {"attribute": false, "think": "<Your thinking process>"}
------------------------------------------------
User: "Return the id of all resources with name ROLLING MILL"
Output: {"attribute": true, "return": "id", "think": "<Your thinking process>"}
------------------------------------------------
User: "When is resource _2 available?"
Output:{"attribute": true, "return": "period", "think": "<Your thinking process>"}
------------------------------------------------
User: "What are the ids of ROLLING MILL'"
Output:{"attribute": true, "return": "id", "think": "<Your thinking process>"}
------------------------------------------------
User: "When is the ROLLING MILL working"
Output:{"attribute": true, "return": "period", "think": "<Your thinking process>"}
------------------------------------------------
User: "Return all resources names"
Output:{"attribute": true, "return": "name", "think": "<Your thinking process>"}"""

prompt += f"""

____________________
User Question:
{user_question}"""

#print(prompt)
llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
print(llm_answer)
print(llm_answer.replace('\n', ''))
print('***********')