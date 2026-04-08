from ollama import chat
import time
from transformers import AutoTokenizer
import datetime
import pandas as pd
import json

#user_question = "Return  all jobs adn tasks"

list_questions = [
### RESOURCES ###

#'Hii'
#'*****',
"Return all resources",
"Return all resource ids",
"Return resouce 2",
"Return resouce 1",
"What is the name of the resource with id 3",
"Return resource with id 7",
"Return resource ROLLING MILL",
"Return resource rolling mill",
"How many resources are there",
"Return the first resource",
"Return 1 resource",
"Return 1 resources",

### JOBS ###

#'*****',
"Return the job with arrival date 31/3",
"List all jobs",
"Give me the jobs",
"Return the job with id 8",
"Are there any jobs with arrival date 31 2",
"List jobs with id 51",
"Find jobs that require task 581",
"Find jobs that require task with id 581",
"Find the last job that requires task with id 581",
"Return the first job",
"Return the job at index 5",
"Return the first job that requires the task with id 580",
"Return job 5",
"Return 4 jobs",
"Return me the FROM BILLET job",
'Return the names of every job',
'Return the task of job 509',
'Return the id of all jobs with name ROLLING',
'Return the first task of every job',
'Return the tasks of all jobs with name ROLLING',
'Return all FROM BILLET jobs',
'Return all jobs with name FROM BILLET',
'Return all ROLLING jobs',
'Return all job ids',

### TASKS ###

#'*****',
"Return task with id 584",
"task with name Rolling",
"Return first task with name Rolling",
"Return first task",
"tasks",
"return task 7",
"return 7 task",
"return 7 tasks",
"return the last task",
'Return all ROLLING tasks',
'Return the id of all tasks with name ROLLING',
'What is the name of the task with id 77',
'What are the ids of MELTING',
'Return all tasks',
'Return the name of every task',

### TASKSUITABLERESOURCES ###

#'*****',
'Which tasks can be done in resource 901?',
'Where can task 57 be executed',
'Which resource can execute task with id 39?',
'Which resource can execute task 39?',
'Can Task 11 be executed in the MELTSHOP?',
'How long does task 52 take?',
'What resource can execute each task?',
'Return all resources and tasks',
'Return all resources and their tasks',
'Return the id of the resource that can execute task 91',
'What task can be executed in the ROLLING MILL',
'Return the ids of all resources and tasks',
'Return all resources where task 77 can be executed',
'Return the id of every resource where task 77 can be executed',
'What is the operation time for task 73',
'What tasks need to operate for more than 30minutes?',

### TASKPREPOST ###

#'*****',
"Is there a task to be executed before task with id 483?",
"Is there a task to be executed before task 11?",
"Is there a task to be executed before 183?",
'Which task should i execute before task 1?',
'What task can i execute after completing task 13?',
'Which task can i do after task 55?',
'Does task 53 require another task to be executed beforehand?',
'Is task 301 independent of other tasks?',
"Return all task dependencies",
'Return the ids of all tasks that have to be executed before task 79',
'Return the names of all tasks that have to be executed before task 85',

### NONE ###

#'*****',
'Hi, how are you?',
'What is this file about?',
'How are you',
#'asijhduasjh',
#'a',
#'aaa',
#'90809809',
#'1',
'Who is Pikachu?',
'Where can i buy Gucci',
#'111111',
#'11',
#'vuvuvuvuvu',
]


prompt_1_keywordsearch = """You are a text analysis assistant. Your task is to examine a user-provided question and detect whether it contains any of the following target words:

- job
- task
- resource

Critical Instruction:

Treat each target word as a pure string pattern (a key) with no semantic meaning.
    - Do NOT interpret, infer, or reason about the meaning of the sentence.
    - Do NOT use context to guess intent.
    - Do NOT associate the words with concepts, roles, or relationships.
    - Each word must be treated as an independent, meaningless token.
    - Your job is strictly pattern detection, not understanding.

Matching Rules:

- Words may appear in singular or plural form (e.g., "jobs", "tasks", "resources").
- Words may be capitalized in any way (e.g., "jOb", "Task", "RESOURCES").
- Words may contain minor spelling mistakes, repeated letters, or extra characters (e.g., "Jjobs", "ta*sks_", "resour ces").
- Words may include non-alphabetic noise such as symbols or typos within them (e.g., "ta*sks_", "re$source").

Important Constraints:

- Only return words that are clearly present in the input.
- Do NOT assume intent if a word is not actually present.
- Do NOT “correct” a word into a target unless it clearly resembles it.
- If multiple target words are found, return all of them.
- If none are found, return: [].

Output Format:

1. Return ONLY a valid JSON object and nothing else.
2. The JSON object must have exactly two fields:
    - "words": an array containing zero or more of the following words: "job", "task", "resource" (all lowercase). It cannot contain a different word from these three
    - "think": an explanation of how the matches were identified based strictly on visible patterns.
Do NOT include any text outside the JSON object.

Examples:
---------------
Input: "How many Jjobs are there?"
Output: { "words": ["job"], "think": "<Your thinking process>" }
---------------
Input: "Return all RESOURCES"
Output: { "words": ["resource"], "think": "<Your thinking process>" }
---------------
Input: "List all Resourc es"
Output: { "words": ["resource"], "think": "<Your thinking process>" }
---------------
Input: "Which resource can execute task 52?"
Output: { "words": ["resource", "task"], "think": "<Your thinking process>" }
--------------
Input: "Hello world"
Output: { "words": [], "think": "<Your thinking process>" }
--------------
Input: "What ta*sks ccan I execute in the"
Output: { "words": ["task"], "think": "<Your thinking process>" }"""

'''
---------------
Input: "How many Jjobs are there?"
Output: { "words": ["job"], "think": "Detected 'Jjobs' as a noisy variation of 'job'." }
---------------
Input: "Return all RESOURCES"
Output: { "words": ["resource"], "think": "Detected 'RESOURCES' as a capitalized plural form of 'resource'." }
---------------
Input: "List all Resourc es"
Output: { "words": ["resource"], "think": "Detected 'Resourc es' as a split variation of 'resource'." }
---------------
Input: "Which resource can execute task 52?"
Output: { "words": ["resource", "task"], "think": "Detected exact matches for 'resource' and 'task'." }
--------------
Input: "Hello world"
Output: { "words": [], "think": "No matching patterns found." }
--------------
Input: "What ta*sks ccan I execute in the"
Output: { "words": ["task"], "think": "Detected 'ta*sks' as a noisy variation of 'task'." }
'''
'''
prompt_1_keywordsearch += f"""


___________________
User Question:
{user_question}"""
'''

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
file_name = 'C:/Users/Chris/Downloads/diplomat/app/tests/_5_output_ollama_test/_1_classifier_outputs/' + 'out_' + str(datetime.date.today()) + '_' + str(int(time.time())) + '.csv'
uq = []
ai_o = []
t = []
tokens = []
ac = []
oa = []
vj = []
for i in range(0, len(list_questions)):
#for i in range(0, 1):
    for y in range(0, 5):
        user_question = list_questions[i]

        prompt = """You are a text analysis assistant. Your task is to examine a user-provided question and detect whether it contains any of the following target words:

- job
- task
- resource

Critical Instruction:

Treat each target word as a pure string pattern (a key) with no semantic meaning.
    - Do NOT interpret, infer, or reason about the meaning of the sentence.
    - Do NOT use context to guess intent.
    - Do NOT associate the words with concepts, roles, or relationships.
    - Each word must be treated as an independent, meaningless token.
    - Your job is strictly pattern detection, not understanding.

Matching Rules:

- Words may appear in singular or plural form (e.g., "jobs", "tasks", "resources").
- Words may be capitalized in any way (e.g., "jOb", "Task", "RESOURCES").
- Words may contain minor spelling mistakes, repeated letters, or extra characters (e.g., "Jjobs", "ta*sks_", "resour ces").
- Words may include non-alphabetic noise such as symbols or typos within them (e.g., "ta*sks_", "re$source").

Important Constraints:

- Only return words that are clearly present in the input.
- Do NOT assume intent if a word is not actually present.
- Do NOT “correct” a word into a target unless it clearly resembles it.
- If multiple target words are found, return all of them.
- If none are found, return: [].

Output Format:

1. Return ONLY a valid JSON object and nothing else.
2. The JSON object must have exactly two fields:
    - "words": an array containing zero or more of the following strings: "job", "task", "resource" (all lowercase). It cannot contain a different word from these three
    - "think": an explanation of how the matches were identified based strictly on visible patterns.
    
Do NOT include any text outside the JSON object.
The words key can ONLY contain one or more of these strings: "resource", "job", "task". It CANNOT have any  other string
Do NOT EVER put the plural form of these strings in the words key. The strings in the word key should ALWAYS be in singular form.
NEVER make assumptions of what a different word might infer to! Search for matches ONLY character-based, character-similarity
NEVER include a word more than one time

Examples:

---------------
Input: "How many Jjobs are there?"
Output: { "words": ["job"], "think": "<Your thinking process>" }
---------------
Input: "Return all RESOURCES"
Output: { "words": ["resource"], "think": "<Your thinking process>" }
---------------
Input: "List all Resourc es"
Output: { "words": ["resource"], "think": "<Your thinking process>" }
---------------
Input: "Which resource can execute task 52?"
Output: { "words": ["resource", "task"], "think": "<Your thinking process>" }
--------------
Input: "Hello world"
Output: { "words": [], "think": "<Your thinking process>" }
--------------
Input: "What ta*sks ccan I execute in the"
Output: { "words": ["task"], "think": "<Your thinking process>" }
--------------
Input: "Return all resources ids"
Output: { "words": ["resource"], "think": "<Your thinking process>" }
--------------
Input: "Return me the FROM BILLET jobs"
Output: { "words": ["job"], "think": "<Your thinking process>" }
--------------
Input: "Return 7 task"
Output: { "words": ["task"], "think": "<Your thinking process>" }
--------------
Input: "Return all ROLLING tasks"
Output: { "words": ["task"], "think": "<Your thinking process>" }
--------------
Input: "Return all tasks with name ROLLING"
Output: { "words": ["task"], "think": "<Your thinking process>" }
--------------
Input: "Which tasks can be done in resource 901?"
Output: { "words": ["task, "resource"], "think": "<Your thinking process>" }
--------------
Input: "Return all resources and their tasks"
Output: { "words": ["task, "resource"], "think": "<Your thinking process>" }
--------------
Input: "Is there a task to be executed before task with id 483?"
Output: { "words": ["task"], "think": "<Your thinking process>" }
--------------
Input: "What tasks can i execute after completing task 13?"
Output: { "words": ["task"], "think": "<Your thinking process>" }
--------------
Input: "Return all task dependencies"
Output: { "words": ["task"], "think": "<Your thinking process>" }"""

        prompt += f"""


___________________
User Question:
{user_question}"""

        prompt_tokens = len(tokenizer.tokenize(prompt))

        start_time = time.time()
        llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
        llm_answer = llm_answer.replace('\n', '')

        answer_correct = True
        original_answer = None
        if('`' in llm_answer):
            original_answer = llm_answer
            answer_correct = False
            llm_answer = llm_answer.replace('`', '')
            if(llm_answer[:4] == 'json'):
                llm_answer = llm_answer[4:]
        compute_time = time.time() - start_time

        uq.append(user_question)
        ai_o.append(llm_answer)
        t.append(compute_time)
        ac.append(answer_correct)
        oa.append(original_answer)
        try:
            json.loads(llm_answer)
            vj.append(True)
        except:
            vj.append(False)
        print('finished: ' + str(i))


all_data = {'User Question': uq, 'LLM Output': ai_o, 'Compute Time': t, 'Answer Correct Form': ac, 'Original Answer': original_answer, 'Valid Jason': vj}
df = pd.DataFrame(all_data)
df.to_csv(file_name, index=False)

sadasdas

llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt_1_keywordsearch}]).message.content

print(llm_answer.replace('\n', ''))