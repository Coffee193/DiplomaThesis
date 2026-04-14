from ollama import chat

### ANSWER JOBS ###

'''I've found 9 results that match your request. Let me see what I can show you...

(DATA)

It seems like there's quite a bit of information here! Would you like me to help you sort through it or would you like more context about any specific job?'''

'''I've found 9 matching records for your request.

(DATA)

It seems like I have a substantial list of items that might be related to what you're looking for. If you'd like, I can help you narrow down the options or provide more information about any of these? Are there any specific details you'd like me to focus on or would you like me to summarize each item for you?'''

user_question = "List all jobs"
len_data = 9

'''There's only one result for your query.

(DATA)

It seems like you're looking for information about tasks. Is there anything else I can help you with? Would you like to know more details about the single job that matched your criteria?'''

'''I've found one result that might be relevant.

(DATA)

It appears there's only one match for your search. Would you like me to elaborate on the specifics of this result? Or would you prefer to explore other options?'''

'''I've searched through the data you provided. It looks like there is only one match for your query.

(DATA)

It seems I have found what you're looking for, but if you'd like more information or would like me to clarify anything, please let me know. Do you need help with anything else? '''

user_question = "Find jobs that require task with id 581"
len_data = 1

'''It looks like there are 9 items that match your search. I've found multiple jobs with the name "ROLLING". 

(DATA)

Would you like me to help with anything else? Do you need more information about these specific jobs, or would you like to filter them further by another criterion?'''

'''You've got 9 results from your upload. I'll make sure to take a look.

Based on your request, I'm focusing on jobs with the name "ROLLING". To summarize, here's what I found:

(DATA)

It looks like there are several jobs matching this criterion. Let me know if you'd like more details about any of these or if you need help filtering them further!'''

'''It looks like we've got 9 potential matches for your search.

Let me take a closer look at these results.

(DATA)

It appears that there are several job listings matching the search term "ROLLING". I can provide you with more information about these roles if you'd like.

Would you like me to explain what each of these jobs entails, or would you prefer I help narrow down the list based on specific criteria?'''

user_question = 'Return the id of all jobs with name ROLLING'
len_data = 9

'''I've got 9 pieces of information related to your query. 

To provide more context, the JSON file contains data about various elements, including jobs and their associated tasks.

Let me give you an overview of what I found:

(DATA)

You mentioned that you're interested in the tasks for all jobs with a specific name - ROLLING. Based on this information, it seems like there might be multiple occurrences of "ROLLING" within the JSON file. If that's correct, would you like me to clarify which tasks you're looking for? Perhaps we can discuss further and narrow down the search based on any additional details you'd like to provide.'''

'''I found 9 potential matches for your query. It seems you're looking for information about specific jobs. I'll take a closer look at the JSON file you uploaded.

For jobs with the name "ROLLING", here are their details:
(DATA)

Would you like me to help you filter these results further or provide more context? Or perhaps you'd like to know how to proceed from here?'''

'''I've searched through the JSON data and found 9 matching results. It looks like there are multiple jobs with the name "ROLLING" in the system.

Here is a summary of what I found:

(DATA)

Now that we have this information, would you like me to help you drill down further into the tasks associated with these jobs?'''

user_question = 'Return the tasks of all jobs with name ROLLING'
len_data = 9

'''I've found one result for your request.

This appears to be related to just one specific item in our search results. Let's see what we have here: (DATA)

It looks like this is all the information I was able to find regarding your query. Is there anything else I can help you with, or would you like me to try and retrieve more details about this result?'''

'''It looks like we have a single result for you. We've found one item that matches your query.

Here is the information we were able to find:

(DATA)

It seems like this might be what you're looking for. However, I'd like to clarify - are you sure it's the correct job with id _90? Would you like me to help you confirm or explore other related options?'''

user_question = 'Return the job with id _90'
len_data = 1

'''It looks like we have just one matching result for your question.

(DATA)

Let me know if you'd like to take a closer look at the details or if there's anything else I can help you with. Are you interested in exploring other aspects of the information, or would you like more context about what each part means?'''

'''There's just one match for your question. According to the information I found, (DATA)

Would you like me to clarify anything about these requirements or help with something else?'''

'''It looks like we found a single match for your question.

(DATA)

Would you like me to explain what these results mean, or would you prefer more information about jobs 90?'''

user_question = 'How many tasks does job 90 require?'
len_data = 1

'''It looks like we've found something for you.

(DATA)

I'd be happy to help you further. Would you like me to clarify any details about what I just showed you, or are there any other questions you'd like to ask? For example, would you like more information about job 277 or is there something else I can assist you with?'''

'''Let me help you with that.

Since we found only one result, I'll provide it directly. Here's the information you requested:

(DATA)

As for your question about job 277, I'm happy to assist further if needed! Would you like to know more details about this particular job or would you like to ask another question?  '''

user_question = 'What is the name of job 277'
len_data = 1

'''I found one result matching your query.

(DATA)

It seems like there's only one match. I'd be happy to help you understand it better or answer any other questions you might have. Would you like me to explain anything specific about this result? Or perhaps you'd like more information on tasks or jobs in general?'''

'''We've found one relevant result.

The (DATA) contains information about jobs, and we can see that it includes details about tasks assigned to each job. Specifically, it mentions a job that requires task 55.

Would you like me to look up more details about this job or provide more context about the requirements for task 55?'''

'''It seems you have one match for your request. I'll just go ahead and provide the details.

(DATA)

Would you like me to help with anything else or would you like more information about this particular match?'''

user_question = 'Return the name of job that require task 55' 
len_data = 1

### ANSWER TASKS ###

'''It looks like you're looking for information about a specific "task". I found one relevant result.

(DATA)

Is there anything else I can help you with regarding this particular "task"? Would you like me to clarify or provide more context?'''

'''It looks like we have just one result matching your query. Would you like me to go ahead and share the details of that task? 

(DATA)

How can I assist you further today? Do you need help reviewing this task or is there something else I can do for you?'''

'''It looks like we have only one result matching your search.

(DATA)

Would you like me to help with anything else, or would you like more information about the task with id 584?'''

user_question = "Return task with id 584"
len_data = 1

'''I've found some relevant information for you. It appears there were multiple results matching your query, and I was able to find 9 occurrences in total.

(DATA)

Would you like me to help with anything else? Do you need more assistance or would you prefer to explore other aspects of the data?'''

'''I've found 9 results that might be related to your query. Let's take a look at them.

(DATA)

It seems like you're looking for information about tasks, specifically ones with the label "MELTING". If I've understood correctly, would you like me to help you filter these results further or see if there are any other tasks that match what you're searching for?'''

user_question = 'What are the ids of MELTING task'
len_data = 9

'''I found information for you in 9 items.

(DATA)

Would you like me to help with anything else, or would you like more details on any specific item?'''

'''I've found 9 tasks that match your search. The list of matching tasks is:

(DATA)

Would you like me to help with anything else, or perhaps provide more details about these tasks?'''

user_question = 'Return the name of every task'
len_data = 9

### ANSWER RESOURCES ###

'''It looks like you'd like to get information about your resources. I've found 2 relevant pieces of data for you.

(DATA)

Is there anything else I can help you with, or would you like me to clarify any part of the result?'''

'''It looks like there were 2 matching results found. (DATA)

Would you like me to help you with anything else, or would you like more information about these results?'''

'''It looks like we have 2 results for your query. I'd be happy to share them with you!

(DATA)

Would you like me to help with anything else or do you need more information about these results?'''

user_question = "Return all resources"
len_data = 2

'''I found that there were 2 matching results for your query. (DATA)

Would you like me to help with anything else, or would you like more details on the resources themselves?'''

'''It looks like we've found 2 matching results for your query.

(DATA)

Would you like me to help with anything else or would you like more details about these resources?'''

user_question = "Return all resource ids"
len_data = 2

'''It looks like we have just one resource in our results. 

(DATA)

Would you like me to help you with anything else, such as retrieving more resources or providing information about this single resource? Or would you like to go back and check the uploaded JSON file for any other details?'''

'''It looks like there's only one item in your data. I'd be happy to help you access it.

(DATA)

Is there something specific you'd like to do with this resource, or would you like me to help you explore its properties further?'''

user_question = "Return resouce 2" 
len_data = 1

'''I found one matching result.

Here is what I was able to find: (DATA)

Is there anything else you'd like me to help with regarding this result, or would you like to explore other resources?'''

'''I found one match for "ROLLING MILL" in the provided information. Let me take a look at it.

(DATA)

Based on what I've seen, would you like me to help with anything else, or is there another aspect of the resources you'd like more information about?'''

user_question = "Return resource ROLLING MILL"
len_data = 1

'''There are 2 items that match your search.

(DATA)

Would you like me to help with filtering or sorting these results in any way? Or perhaps you'd like more information about how I can assist you further?'''

'''I've found 2 matching results.

(DATA)

Would you like me to help with filtering or sorting these results, or would you prefer more information about a specific attribute?'''

user_question = "How many resources are there"
len_data = 2

'''It looks like there's one piece of information about resource 1 in our search results. Let me see what I can find.

(DATA)

Looks like we've got some information on resource 1 now! Do you need help understanding or using this data for anything else, or is there something specific you'd like to know?  '''

'''It looks like there's only one result for your question.

(DATA)

Can you tell me what would be the next step for you regarding this resource? Would you like to explore any related information or is there something else I can assist you with?  '''

user_question = "What are the working periods of resource 1"
len_data = 1

### TASKSUITABLERESOURCES ###

## PROBLEM --> Fixed in 6_2
user_question = 'Does task 584 need to be executed before 585?'
len_data = 1

'''It looks like there's only one piece of information related to your request.

(DATA)

I'd be happy to help you understand what this result means. Do you need me to explain how it relates to the specific task you're looking for, or would you like to explore other aspects of the information?'''

'''You've got only one result matching your query.

(DATA)

Is there anything else I can help you with? Perhaps you'd like more information about this specific result or if you need assistance with another question?'''

user_question = 'Return the names of all tasks that have to be executed before task 85'
len_data = 1

## SOMEWHAT GOOD OF AN ANSWER

'''We have a single piece of information available.

You're looking for guidance on which task to run prior to "task 1". I'll take a look at the details.

(DATA)

It seems that there's only one relevant item in the list, but I want to confirm if you'd like me to elaborate on what it is. Would you like me to provide more context or help with anything else?'''

'''Only one item matches your search query.

(DATA)

It seems like you're looking for information about tasks. Can I help you find any specific details or would you like me to clarify something else related to the result?'''

user_question = 'Which task should i execute before task 1?'
len_data = 1

'''I've found that there is only one match for your query.

(DATA)

Would you like me to help with anything else, such as checking the status of a specific resource or exploring more information about a particular job?'''

'''It looks like we've found one result matching your query.

(DATA)

You can see that there's only one related task in the data. I'd be happy to help you understand this further. Would you like me to explain any specific details about it, or would you like to ask a follow-up question?'''

user_question = "Is there a task to be executed before task 11?"
len_data = 1

## PROBLEMATIC
user_question = "Is task 535 independent of task 901"
len_data = 1

### TASKSUITABLERESOURCES ###

'''I've found one relevant match for your query.

(DATA)

Would you like me to help with anything else or would you like more details on this particular result?'''

'''That's a specific query. Based on our search, we found one relevant result.

(DATA)

Would you like me to help with anything else? Perhaps you'd like to know more about this particular resource or its capabilities regarding task execution?'''

'''It looks like we have only one result matching your query. Let me take a closer look.

(DATA)

Is there anything else I can help you with, or would you like more information about the single match found?'''

user_question = 'Return the id of the resource that can execute task 91'
len_data = 1

'''It seems we have found only one result that matches your query.

(DATA)

Would you like me to help with anything else related to this result or would you like more information about the remaining resources on your JSON file?'''

'''It looks like we've got a single result for you!

The details of this result are represented by (DATA).

Would you like me to help with anything else, or would you like more information about the resources available for task execution?'''

user_question = 'Which resource can execute task 39?'
len_data = 1

prompt = f"""You are an AI assistant helping a user based on queried information.

You are given only the length of retrieved results, not the actual data.

    - Make the response feel conversational by:
        - Naturally incorporating the number of found results into the sentence
        - Varying wording so it does not sound templated or repetitive
    - The introduction should be short and simple.

    - At an appropriate and natural point in your answer, include the placeholder keyword:
    (DATA)
    - This placeholder will later be replaced with the actual retrieved content, so ensure it fits smoothly into the sentence.
    - Treat (DATA) as a standalone block (like a table or dataset), NEVER part of a sentence.
    - (DATA) contains a list of all the information retrieved, so print it only ONCE in your output.
    - (DATA) represent the information the user is asking for.
    - NEVER output lists of information that represent the data.
    - NEVER NEVER create lists, or bullet-like items that are supposed to respresent the data the user is searching for. The palceholder (DATA) is enough to give a complete overview of that data
    - The placeholder needs to ALWAYS be EXACTLY written as: (DATA)
    - NEVER explain the data fetched as you have no access to them.
    - Do NOT mention that you have no information about the data.
    - Do NOT try to answer the question
    - If the user wants a specific attribute returned (name, id etc..) do NOT place (DATA) as part of a sentence 

Additional rules:

- Never mention “length,” “API,” “retrieved data,” or “placeholders.”
- Be polite, clear, and user-friendly in tone.
- At the end of every response, ask a follow-up question or offer further assistance to keep the interaction going (e.g., ask if they need help with anything else or want more details).
- Do NOT assign meaning to the words: “tasks”, “jobs”, “resources”, or similar.
    - These are simply keys and must not influence your wording unless the user explicitly refers to them
    - NEVER replace any of these words with other words such as "position", "opportunities" or any other word.
    - Refer to them STRICTLY by key
    - Write these keys by their name: "jobs", "resources", "tasks" ONLY. NEVER write things like: "job openings", "job listings" simply write "jobs"
    - Do NOT EVER mix these words. Refer to jobs as jobs, to tasks as tasks, to resources as resources
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