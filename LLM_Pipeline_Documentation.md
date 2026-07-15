# Diplomat - LLM Pipeline Full Documentation

This document contains everything needed to understand the LLM pipeline of the "Diplomat" diploma thesis project. The project is a chat application where users upload JSON files representing industrial scheduling/planning problems and ask natural-language questions about them. The backend uses a multi-chain LLM pipeline to classify, filter, and answer those questions.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [JSON File Schemas (Input & Output)](#3-json-file-schemas)
4. [The 5-Chain LLM Pipeline (Mode m=1)](#4-the-5-chain-llm-pipeline)
5. [Chain 0: Upload Recognition](#5-chain-0-upload-recognition)
6. [Chain 1: Gibberish Detection](#6-chain-1-gibberish-detection)
7. [Chain 2: High-Level Entity Classification](#7-chain-2-high-level-entity-classification)
8. [Chain 3: Attribute Retrieval (Filtering)](#8-chain-3-attribute-retrieval)
9. [Chain 4: Wanted Return Value Classification](#9-chain-4-wanted-return-value-classification)
10. [Chain 5: Final Answer Generation](#10-chain-5-final-answer-generation)
11. [Data Query Functions](#11-data-query-functions)
12. [Special Query Types](#12-special-query-types)
13. [Utility Functions](#13-utility-functions)
14. [Alternative Modes (m=2, m=3)](#14-alternative-modes)
15. [Title Generation](#15-title-generation)
16. [Streaming & Frontend Integration](#16-streaming-and-frontend-integration)
17. [All Prompt Templates (Complete Text)](#17-all-prompt-templates)

---

## 1. Project Overview

**Diplomat** is a diploma thesis project - a full-stack chat application with an LLM-powered backend for answering questions about uploaded JSON scheduling/planning data files.

**Domain**: Industrial scheduling - the JSON files describe manufacturing/production scheduling problems with:
- **Jobs** (e.g., "FROM BILLET") - work orders with arrival dates and due dates
- **Tasks** (e.g., "Melting", "Rolling") - operations within jobs
- **Resources** (e.g., "MELTSHOP", "ROLLING MILL") - machines that execute tasks
- **Task-Suitable Resources** - which resources can execute which tasks, with operation times
- **Task Precedence Constraints** - which tasks must be executed before/after others
- **Assignments** (Output files only) - the actual scheduled execution plan

**Key behavior**: Users upload one or more JSON files and ask natural-language questions like:
- "Return all jobs"
- "What is the name of task 584?"
- "Which resource can execute task 57?"
- "Does task 585 need to be executed before task 584?"
- "Which plan has the shortest makespan?"
- "When did job 95 start and end?"
- "How many jobs are completed by March 15?"

The LLM does NOT directly read/query the JSON. Instead, a 5-chain classification pipeline determines WHAT the user is asking about, extracts filter criteria and desired return fields, then Python code performs the actual JSON data extraction. The LLM only generates the final natural-language response with a `(DATA)` placeholder that the frontend replaces with actual query results.

---

## 2. Architecture

### Tech Stack
- **Backend**: Django 4.1 + Django REST Framework (Python)
- **Frontend**: React 19 + Vite + SWC
- **Databases**: PostgreSQL (users), MongoDB (chats), Redis (streaming + cache)
- **LLM**: Ollama (local, default model `llama3.1`) or OpenAI GPT-4.1 (cloud)

### Three Model Modes (controlled by `data['m']` in the request)
- **m=1**: "Thinking" mode - runs the full 5-chain classification pipeline via Ollama
- **m=2**: "No-agent" mode - raw JSON content is injected directly into the conversation context, LLM answers freely
- **m=3**: "Cloud" mode - files uploaded to OpenAI Files API, conversation sent to GPT-4.1

### Data Flow (m=1, the main pipeline)
```
User submits question (+optional JSON files)
         |
         v
views.py: AnswerQuestionLLMThink() [multiprocessing.Process]
         |
         v
LLMpipeline.py: PassLLMThinkCompletePipeline()
    |
    |-- PassLLMThink() -- Chains 0-4
    |     Chain 0: File upload without question -> acknowledge
    |     Chain 1: Gibberish detection
    |     Chain 2: Entity classification (jobs/tasks/resources/etc)
    |     Chain 3: Attribute retrieval (filter extraction)
    |     Chain 4: Return value classification
    |
    |-- LLMGetFinalQuery() -- Python reads JSON files, filters/transforms data
    |
    |-- PassLLMFinalAnswer() -- Chain 5: LLM generates natural language answer
    |
    v
Response streamed via Redis Streams to frontend
    |
    v
Frontend renders text, replaces (DATA) placeholder with structured data blocks
```

### LLM Communication
All LLM calls use the Ollama Python library:
```python
from ollama import chat
# Non-streaming (classification chains):
answer = chat(llm_model, messages=[{'role': 'user', 'content': prompt}]).message.content
# Streaming (final answer):
response = chat(llm_model, messages=[{'role': 'user', 'content': prompt}], stream=True)
```

### Streaming Protocol
LLM answers stream to the frontend via Redis Streams (`xadd`/`xread` on key `cs_{chat_id}`).
Stream message keys:
- `v` = text chunk (value)
- `t` = title
- `d` = done signal
- `i` = info (query results + search type)
- `u` = uploaded document info
- `e` = error

---

## 3. JSON File Schemas

The system distinguishes between **Input JSON** files (scheduling problem definition) and **Output JSON** files (scheduling solution/assignments). Files are identified by their filename containing "input" or "output" (case-insensitive).

### Input JSON Schema (scheduling problem definition)

```json
{
  "workcenters": {
    "workcenter": [{
      "name": "Generic Workcenter",
      "id": "WC",
      "workcenterresourcereference": [{"refid": "_1"}, {"refid": "_2"}]
    }]
  },
  "resources": {
    "resource": [{
      "name": "MELTSHOP",
      "id": "_1",
      "resourceavailability": {
        "nonworkingperiods": {
          "period": [{
            "fromdate": {"day": 9, "month": 2, "year": 2026, "hour": 0, "minute": 0, "second": 0},
            "todate": {"day": 9, "month": 2, "year": 2026, "hour": 6, "minute": 0, "second": 0}
          }]
        }
      }
    }, {
      "name": "ROLLING MILL",
      "id": "_2",
      "resourceavailability": { "nonworkingperiods": { "period": [...] } }
    }]
  },
  "jobs": {
    "job": [{
      "name": "FROM BILLET",
      "id": "_299",
      "arrivaldate": {"day": 9, "month": 2, "year": 2026, "hour": 0, "minute": 0, "second": 0},
      "duedate": {"day": 31, "month": 3, "year": 2026, "hour": 0, "minute": 0, "second": 0},
      "jobtaskreference": [{"refid": "_584"}, {"refid": "_585"}],
      "jobworkcenterreference": {"refid": "WC"}
    }]
  },
  "tasks": {
    "task": [{
      "name": "Rolling",
      "id": "_584"
    }, {
      "name": "Melting",
      "id": "_585"
    }]
  },
  "tasksuitableresources": {
    "tasksuitableresource": [{
      "resourcereference": {"refid": "_2"},
      "taskreference": {"refid": "_584"},
      "operationtimeperbatchinseconds": 4083.0,
      "setupcode": "Phi11.0"
    }]
  },
  "taskprecedenceconstraints": {
    "taskprecedenceconstraint": [{
      "preconditiontaskreference": {"refid": "_585"},
      "postconditiontaskreference": {"refid": "_584"}
    }]
  }
}
```

Key entities in Input JSON:
- **resources[].id**: IDs prefixed with underscore (e.g., "_1", "_2")
- **jobs[].jobtaskreference**: Array of task references (refid) belonging to this job
- **tasksuitableresources**: Maps which resource can execute which task, with operation time in seconds
- **taskprecedenceconstraints**: `preconditiontaskreference` must execute BEFORE `postconditiontaskreference`

### Output JSON Schema (scheduling solution)

```json
{
  "assignments": {
    "assignment": [{
      "task": {"id": "__191"},
      "resource": {"id": "__1"},
      "timeofdispatch": {
        "day": 20, "month": 11, "year": 2027,
        "hour": 6, "minutes": 25, "seconds": 2
      },
      "durationinmilliseconds": 16187100,
      "properties": null,
      "locked": null
    }]
  }
}
```

Note: Output JSON uses "minutes" and "seconds" (plural) while Input JSON uses "minute" and "second" (singular) in date objects.

### File Naming Convention
Files must contain either "input" or "output" in the filename (not both). Examples:
- `InputJSON_1.json`, `InputJSON_3.json`
- `OutputJSON_1.json`, `OutputJSON_5.json`

For cross-file queries (job duration, start/end, completion), the system pairs Input and Output files by their number suffix: `InputJSON_1.json` pairs with `OutputJSON_1.json` (matched via regex `(input|output)[a-z]*_(\d+)`).

---

## 4. The 5-Chain LLM Pipeline

The pipeline is a sequential series of LLM classification steps. Each chain calls the LLM with a specific prompt and parses the JSON response. The pipeline is implemented in `LLMpipeline.py` (1630 lines).

### Entry Point
```python
def PassLLMThinkCompletePipeline(llm_model, user_question, conv_id, db_chat=[], json_document=None):
    llm_res = PassLLMThink(llm_model, user_question, db_chat, json_document, conv_id)
    if llm_res['end'] != 'success_complete':
        return [llm_res['response_msg'], llm_res['think'], None, None, None]
    else:
        fetched_results = LLMGetFinalQuery(conv_id, llm_res['search'], ...)
        result = PassLLMFinalAnswer(...)
        return result
```

### Pipeline Return Structure
When all chains succeed, `PassLLMThink()` returns:
```python
{
    'end': 'success_complete',
    'think': [{'chain': '1', 'think': '...'}, {'chain': '2', 'think': '...'}, ...],
    'search': 'jobs' | 'tasks' | 'resources' | 'tasksuitableresources' | 'tasksprecedenceconstraints' | 'assignment' | 'dispatch' | 'duration' | 'plan',
    'retrieve_info': {...} or None,  # Chain 3 output
    'wanted_return': {...} or None,  # Chain 4 output
    'json_documents': [...],         # List of document references
    'taskprecedenceconstraints_pick': 'order' | 'dependence' | None,
    'complex': ['duration'] | ['start', 'end'] | ['complete'] | None,
    'complex_utils': {'duration_extremum': 'A'|'B'|None, 'complete_by': {...}} or {}
}
```

### Early Exit Points
The pipeline can exit early at many points:
- Chain 0: File uploaded without question -> acknowledge upload
- Chain 1: Gibberish detected -> polite error
- Chain 2: No entity words found and no output/plan keywords -> treat as general conversation (send question + chat history to LLM directly)
- Various validation gates (missing files, no fused pair, etc.)
- Any JSON parsing failure -> ExceptionHandler fallback

---

## 5. Chain 0: Upload Recognition

If the user uploads a file(s) without asking a question (`user_question == ''`), the pipeline returns immediately with a recognition message.

- Single file: Uses `JSONUploadNoQuestion.getPrompt(filename)`
- Multiple files: Uses `MultipleJSONUploadNoQuestion.getPrompt(filenames)`

---

## 6. Chain 1: Gibberish Detection

**Purpose**: Detect if the user's input is gibberish/random characters.

**Prompt**: `GibberishClassifier.getPrompt(user_question)`

**Expected LLM Output**:
```json
{"gibberish": true/false, "think": "reasoning..."}
```

**Behavior**:
- If `gibberish == true`: Returns ExceptionHandler response (polite error)
- If `gibberish == false`: Proceeds to Chain 2
- If JSON parsing fails: Returns ExceptionHandler response

---

## 7. Chain 2: High-Level Entity Classification

**Purpose**: Determine WHAT the user is asking about. This is a multi-step classification:

### Step 1: Word Pattern Detection (Input entities)
**Prompt**: `HighLevelClassifier.getPrompt(user_question)`

Detects character-pattern matches for: "job", "task", "resource" (pure string matching, no semantic inference).

**Expected Output**:
```json
{"words": ["job"] | ["task"] | ["resource"] | ["task", "resource"] | [], "think": "..."}
```

**Routing Logic**:
- `["job"]` -> `search = "jobs"`
- `["resource", "task"]` or `["task", "resource"]` -> `search = "tasksuitableresources"`
- `["resource"]` alone -> `search = "resources"`
- `["task"]` alone -> triggers sub-classifier (Step 1b)
- `[]` (empty) -> proceed to Step 2

### Step 1b: Task Sub-Classifier (when only "task" detected)
**Prompt**: `HighLevelTaskClassifier.getPrompt(user_question)`

Semantic classifier that picks 1, 2, or 3:
- `pick = 1`: tasksuitableresources (where can task be executed, how long does it take)
- `pick = 2`: tasksprecedenceconstraints (order, dependencies)
- `pick = 3`: tasks (general task info)

**Expected Output**:
```json
{"pick": 1|2|3, "think": "..."}
```

### Step 2: Output JSON Pattern Detection (if Step 1 found nothing)
**Prompt**: `HighLevelOutputJSONClassifier.getPrompt(user_question)`

Detects: "assignment", "dispatch", "duration"

**Expected Output**:
```json
{"words": ["assignment"] | ["dispatch"] | ["duration"] | [...] | [], "think": "..."}
```

If found: sets `search` to "assignment"/"dispatch"/"duration" and marks `output_specific = True`.

### Step 3: Plan Detection (if Step 2 found nothing)
**Prompt**: `HighLevelPlanClassifier.getPrompt(user_question)`

Detects: "plan"

If found: `search = "plan"`.
If not found: falls through to general conversation (no pipeline, just chat with LLM using conversation history).

### Complex Query Detection (for jobs/tasks/tasksuitableresources)
**Prompt**: `InputMultiOuputJSONClassifier.getPrompt(user_question)`

Detects: "complete", "start", "end", "duration", "production", "finish", "done"

Note: "production" is mapped to "duration" in the code: `words = ['duration' if w == 'production' else w for w in answer['words']]`

If complex words found, additional sub-classifiers may run:
- **Duration extremum**: `InputMultiOutputJSONDurationLongestShortestClassifier` - detects "longest"/"shortest"/"maximum"/"minimum" etc. Returns `pick: "A"` (longest), `"B"` (shortest), or `"None"`.
- **Complete date extraction**: `InputMultiOutputJSONCompleteDateExtractor` - extracts a date from the question (e.g., "By March 15..."). Then `StringToDateMonthForm` converts it to `{"day": int, "month": int}`.

### Validation Gates (after Chain 2)

1. **No file provided**: Searches chat history for last uploaded file. If none found: returns "please upload a file" message.

2. **Job Duration**: Requires at least one Input file (has 'input' in filename).

3. **Job Start/End**: Requires a "fused pair" - both an Input file AND Output file with matching number suffix (e.g., InputJSON_1 + OutputJSON_1).

4. **Job Complete**: Same fused pair requirement.

5. **Plan Comparison**: Requires at least 2 Output files. If satisfied, skips Chains 3-4 entirely.

---

## 8. Chain 3: Attribute Retrieval (Filtering)

**Purpose**: Extract the filter criteria from the user's question. What specific entity is the user looking for?

Different prompts depending on `search`:

### For `search = "jobs"`:
**Prompt**: `JobAttributeRetriever.getPrompt(user_question)`

Job has keys: name, arrivaldate, duedate, task, workcenter, id

**Expected Output**:
```json
// When filtering by attribute:
{"attribute": true, "key": "id", "value": 63, "think": "..."}
// When no filter (e.g., "Return all jobs"):
{"attribute": false, "think": "..."}
```

### For `search = "tasks"`:
**Prompt**: `TaskAttributeRetriever.getPrompt(user_question)`

Task has keys: name, id

### For `search = "resources"`:
**Prompt**: `ResourceAttributeRetriever.getPrompt(user_question)`

Resource has keys: name, id

### For `search = "tasksuitableresources"`:
**Prompt**: `TasksuitableresourceAttributeRetriever.getPrompt(user_question)`

More complex output format:
```json
{
  "attribute": true,
  "know": {"info": "resource"|"task", "key": "id"|"name", "value": ...},
  "search": {"info": "resource"|"task"|"time"},
  "think": "..."
}
```

This captures both what the user KNOWS (the reference point) and what they're SEARCHING FOR.

### For `search = "tasksprecedenceconstraints"`:

First runs a sub-classifier:
**Prompt**: `TaskprecedencecontraintOrderDependenceClassifier.getPrompt(user_question)`
```json
{"pick": "order"|"dependence", "think": "..."}
```
- "order": asking about sequence (before OR after, single direction)
- "dependence": asking about dependencies/independence, or both directions

Then:
- If "order": `TaskprecedenceconstraintOrderAttributeRetriever.getPrompt(user_question)`
  ```json
  {"attribute": true, "before": 81|"*", "after": 483|"*", "think": "..."}
  ```
- If "dependence": `TaskprecedenceconstraintDependenceAttributeRetriever.getPrompt(user_question)`
  ```json
  {"attribute": true, "reference": 59, "target": 37|"*", "think": "..."}
  ```

---

## 9. Chain 4: Wanted Return Value Classification

**Purpose**: Determine what field the user wants RETURNED (not what they're filtering by).

This chain is SKIPPED for:
- `tasksprecedenceconstraints` (always returns full constraint info)
- Complex queries with start/end/complete (return format is predetermined)

### For `search = "jobs"`:
**Prompt**: `JobAttributeReturnClassifier.getPrompt(user_question)`

**Expected Output**:
```json
// User wants a specific attribute:
{"attribute": true, "return": "name"|"id"|"task"|"arrivaldate"|"duedate", "think": "..."}
// User wants the full object:
{"attribute": false, "think": "..."}
```

### For `search = "tasks"`:
**Prompt**: `TaskAttributeReturnClassifier.getPrompt(user_question)`

Possible returns: "name", "id"

### For `search = "resources"`:
**Prompt**: `ResourceAttributeReturnClassifier.getPrompt(user_question)`

Possible returns: "name", "id", "period"

### For `search = "tasksuitableresources"`:
Uses different prompts depending on whether the user is searching for resource or task info:

- Searching resource info: `TasksuitableresourceAttributeReturnResourceClassifier`
  ```json
  {"attribute": true|false, "key": "name"|"id"|"period", "value": ...(optional), "think": "..."}
  ```
- Searching task info: `TasksuitableresourceAttributeReturnTaskClassifier`
  ```json
  {"attribute": true|false, "key": "name"|"id"|"time", "value": ...(optional), "think": "..."}
  ```

---

## 10. Chain 5: Final Answer Generation

**Purpose**: Generate the natural language response for the user.

The prompt is selected based on the search type and result count:

### Standard Entities (jobs, tasks, resources, tasksuitableresources)
- **Results found**: `OutputListResultsTaskJobResourceTasksuitableresource.getPrompt(user_question, len_data)` - includes `(DATA)` placeholder
- **No results**: `OutputNoResultsFound.getPrompt(user_question)` - politely says no matches found

### Task Precedence Constraints
More complex logic depending on `taskprecedenceconstraints_pick`:

**"dependence" mode**:
- No results + task doesn't exist: `OutputTaskprecedenceconstraintsTaskNoExist` - "no task found with that ID"
- No results + task is independent: `OutputTaskprecedenceconstraintsTaskIsIndependent` - "the task is independent"
- Single result: `OutputListResultsTaskprecedenceconstraints` - direct answer with info
- Multiple results: `OutputListResultsTaskJobResourceTasksuitableresource` - standard list with (DATA)

**"order" mode**:
- No results: `OutputNoResultsFound`
- Results found: first classifies if the question is boolean (yes/no):
  - Boolean (e.g., "Does task 584 need to run before 585?"): `OutputTaskprecedenceconstraintsAnswerBooleanQuestion` - answers affirmatively + (DATA)
  - Non-boolean (e.g., "What task comes after task 13?"): `OutputListResultsTaskprecedenceconstraints` - direct answer with info

### Plan Comparison
- Single winner: `OutputListResultsPlanComparisonSingle.getPrompt(user_question, best_doc_name)` - recommends the file with shortest makespan
- Multiple tied winners: `OutputListResultsPlanComparisonMultiple.getPrompt(user_question, best_doc_names)` - mentions all tied plans

### Multiple Documents
- `OutputListResultsMultipleDocuments.getPrompt(user_question)` - generic multi-doc response

### Invalid File Name
- `OutputInvalidName.getPrompt(user_question)` - file must contain "input" or "output" but not both

### The (DATA) Placeholder Pattern
All final answer prompts that include query results use a `(DATA)` placeholder. The LLM generates text like:
> "I found 5 jobs matching your criteria. Here are the results:
> (DATA)
> Would you like more details about any of these?"

The frontend then replaces `(DATA)` with the actual structured data rendered as HTML blocks. The LLM never sees the actual data in Chain 5 - it only knows the count.

---

## 11. Data Query Functions

After Chains 1-4 determine WHAT to query and HOW to filter, `LLMGetFinalQuery()` dispatches to specialized functions that read the JSON files from disk and extract data.

### Routing
```python
def LLMGetFinalQuery(conv_id, search, json_documents, retrieve_info, llm_model, wanted_return, complex=None, complex_utils={}):
    if search == 'plan':
        return LLMGetFinalQueryPlan(...)
    if search == 'jobs' and complex has 'duration':
        return LLMGetFinalQueryJobDuration(...)
    if search == 'jobs' and complex has 'start'|'end':
        return LLMGetFinalQueryJobStartEnd(...)
    if search == 'jobs' and complex has 'complete':
        return LLMGetFinalQueryJobComplete(...)
    # For each document:
    #   if "input" in filename -> LLMGetFinalQueryInputJSON()
    #   if "output" in filename -> LLMGetFinalQueryOutputJSON()
```

### LLMGetFinalQueryInputJSON
Handles queries on Input JSON files. Applies chains 2-4 results sequentially:

1. **Chain 2** (entity selection): Extracts the relevant array from JSON (`json_data["jobs"]["job"]`, `json_data["tasks"]["task"]`, etc.)

2. **Chain 3** (filtering): Applies filters based on `retrieve_info`:
   - For jobs: filter by id, name, task (refid), arrivaldate, duedate
   - For tasks: filter by id, name
   - For resources: filter by id, name
   - For tasksuitableresources: filter by known resource/task attribute
   - For taskprecedenceconstraints: filter by before/after task IDs

3. **Data cleaning**: Reshapes raw JSON into clean query format:
   - Jobs: `{name, arrivaldate, duedate, task: [refids], workcenter, id}`
   - Tasks: `{name, id}`
   - Resources: `{name, nonworkingperiods: [{fromdate, todate}], id}`
   - Tasksuitableresources: grouped by resource `{resource: {id, name}, tasks: [{id, operation_time, name}]}`
   - Taskprecedenceconstraints: `{before: refid, next: refid}`

4. **Chain 4** (projection): Keeps only requested return fields (e.g., if user wants only names, strips everything else)

### LLMGetFinalQueryOutputJSON
Handles queries on Output JSON files. Extracts assignment data based on search type:
- `assignment`: full assignment objects
- `tasks`: task IDs from assignments
- `resources`: resource IDs from assignments
- `dispatch`: dispatch times
- `duration`: duration in milliseconds

### ID Format Handling
The helper `IntToStrWithSlabInfornt(val)` prepends an underscore to numeric IDs (e.g., `95` -> `"_95"`). This handles the mismatch between how the LLM might extract an ID (as integer) vs. how IDs are stored in JSON (as strings with underscore prefix).

---

## 12. Special Query Types

### Job Duration (cross-file query)
Pairs Input + Output files by number suffix. For each job:
- If only Input available: sums `operationtimeperbatchinseconds` from tasksuitableresources for the job's tasks
- If Input+Output pair: sums `durationinmilliseconds` from matching assignments (divided by 1000 to get seconds)

Supports extremum filtering: longest (`duration_extremum = 'A'`) or shortest (`'B'`).

### Job Start/End (cross-file query)
Requires fused Input+Output pairs. For each job:
- **Start**: Finds the earliest `timeofdispatch` among all assignments matching the job's tasks
- **End**: Finds the latest end time (dispatch + duration) among all matching assignments

### Job Complete (cross-file query)
Requires fused Input+Output pairs + a target date. For each job:
- Calculates the latest end time across all task assignments
- Checks if `end_time <= deadline` (deadline = `complete_by` date extracted in Chain 2)
- Returns only jobs that complete before the deadline

### Plan Comparison
Requires 2+ Output files. For each Output file:
- Calculates **makespan** = latest assignment end time - earliest assignment start time (in milliseconds)
- Finds the plan(s) with shortest makespan
- If single winner: recommends it. If tied: mentions all tied plans.

---

## 13. Utility Functions

### LLMOutClean(answer)
Post-processes LLM text output:
```python
def LLMOutClean(answer):
    answer = answer.replace('\n', '')
    if '`' in answer:
        answer = answer.replace('`', '')
        if answer[:4] == 'json':
            answer = answer[4:]
    return answer
```
Removes newlines and strips markdown code block formatting (backticks + "json" prefix).

### BuildDocNames(json_documents)
Groups documents by their number suffix, pairing Input with Output files:
- Extracts number from filename via regex: `(input|output)[a-z]*_(\d+)`
- Returns list of groups: `[["InputJSON_1.json", "OutputJSON_1.json"], ["InputJSON_3.json"], ...]`

### GetLastFileFromChat(db_chat)
When user asks a question without uploading a file, searches backwards through chat history for the most recently uploaded documents.

### CreateChatConv(db_chat, user_question, file_name, conv_id)
Builds the conversation history for general (non-pipeline) LLM calls. Formats previous messages as user/assistant pairs, including file references.

### StringToDateMonthForm
Converts date strings to `{"day": int, "month": int}` via LLM. Handles various formats: "30 1", "28,2", "13/5", "12 January", "7 march", etc.

---

## 14. Alternative Modes

### Mode m=2 (No-Agent / Direct LLM)
The raw JSON file content is injected directly into the conversation prompt:
```python
# NoAgentJSONUpload.getPrompt(user_question, documents)
# For single file:
"The user uploaded a file:
--- filename.json ---
{...full JSON content...}
--- End of filename.json ---

User Question: ..."
```
No classification pipeline runs. The LLM answers freely based on the full file content.

### Mode m=3 (Cloud / OpenAI GPT-4.1)
Files are uploaded via the OpenAI Files API. The conversation is sent to GPT-4.1 via the Responses API. No pipeline runs. Requires user-provided OpenAI API key.

---

## 15. Title Generation

Automatic conversation title generation (`CreateConversationTitleThink`):

1. Runs Chain 1 (gibberish detection) on the question
2. If gibberish: generates a generic title via `TittleGibberishInput`
3. If file uploaded without question: `TitleJSONUploadNoQuestion` (generic file upload title)
4. If file + question:
   - Runs Chain 2 classification to check if question is relevant to JSON domain
   - Relevant: `TitleJSONUploadRelevantQuestion` (generates 5-word title from question)
   - Irrelevant: `TitleOnlyQuestionNoJSON` (generates title from question alone)
5. If question only (no file): `TitleOnlyQuestionNoJSON`

---

## 16. Streaming and Frontend Integration

### Backend Streaming
The LLM pipeline runs in a `multiprocessing.Process`. It writes response chunks to a Redis Stream:

```python
# Writing chunks (in views.py):
redis_client.xadd(f'cs_{chat_id}', {'v': chunk_text})
redis_client.xadd(f'cs_{chat_id}', {'t': title})
redis_client.xadd(f'cs_{chat_id}', {'i': json.dumps({'query': query_data, 'search': search_type})})
redis_client.xadd(f'cs_{chat_id}', {'d': 'done'})
```

### Frontend Rendering
The frontend reads the stream via `StreamingHttpResponse` and:
1. Displays text chunks (`v`) as they arrive
2. When `i` (info) arrives, stores the query data
3. When complete, replaces the `(DATA)` placeholder in the rendered text with structured data blocks showing the query results

### MongoDB Storage
After streaming completes, the full conversation turn is saved to MongoDB:
```json
{
  "_id": "snowflake_id",
  "chat": [{
    "q": "user question",
    "a": "full LLM answer",
    "d": [{"id": 123, "name": "InputJSON_1.json", "size": "68.9"}],
    "t": "2026-03-15T10:30:00",
    "think": [{"chain": "1", "think": "..."}, {"chain": "2", "think": "..."}, ...],
    "i": [{"query": [...], "json_data": {...}}],
    "s": "jobs"
  }]
}
```

---

## 17. All Prompt Templates (Complete Text)

Every prompt is a Python module with a `getPrompt(...)` function. Below are the complete prompt texts for all 51 modules.

---

### Chain 1: GibberishClassifier

```
You are a text analysis assistant. Your task is to examine a user-provided question and detect whether it is gibberish or not

Classify it as giberrish if:
- the question is gibberish or random, single characters or numbers without anything else in the input.
- If the question is a single number without anything else in the input

Output Format:

{"gibberish": <bool>, "think": <Your thinking process>}

- gibberish: whether the input is gibberish. Passed value should be: 'true' or 'false'
- think: Your thinking process as to why you picked that number

Remember:
- Always return ONLY valid JSON and nothing else. Do not explain Youserlf.
- Do NOT include any text outside the JSON object.

Examples:
Output: {"gibberish": true, "think": "<Your thinking process>"}
Output: {"gibberish": false, "think": "<Your thinking process>"}


_________________
User Question:
{user_question}
```

---

### Chain 2: HighLevelClassifier

Detects: "job", "task", "resource" via pure character-pattern matching. No semantic inference.

Output: `{"words": ["job"|"task"|"resource", ...], "think": "..."}`

Key rules:
- Words must be found via character-similarity matching only
- Returns singular forms only
- Words array can only contain: "resource", "job", "task"
- Empty array if none found

---

### Chain 2: HighLevelOutputJSONClassifier

Detects: "assignment", "dispatch", "duration" via character-pattern matching.

Output: `{"words": ["assignment"|"dispatch"|"duration", ...], "think": "..."}`

---

### Chain 2: HighLevelPlanClassifier

Detects: "plan" via character-pattern matching.

Output: `{"words": ["plan"] | [], "think": "..."}`

---

### Chain 2: HighLevelTaskClassifier

Semantic classifier - picks 1, 2, or 3:
- 1 = tasksuitableresources (location/duration of task)
- 2 = taskprecedenceconstraints (order/dependencies)
- 3 = tasks (general task info)

Output: `{"pick": 1|2|3, "think": "..."}`

---

### Chain 2: InputMultiOuputJSONClassifier

Detects: "complete", "start", "end", "duration", "production", "finish", "done"

Output: `{"words": [...], "think": "..."}`

Note: "finish" and "done" map to "complete" conceptually. "production" maps to "duration" in code.

---

### Chain 2: InputMultiOutputJSONDurationLongestShortestClassifier

Detects extremum words:
- Group A (longest): longest, most, maximum, max, greatest, highest, biggest, largest
- Group B (shortest): shortest, least, minimum, min, smallest, lowest, quickest, fastest

Output: `{"pick": "A"|"B"|"None", "think": "..."}`

---

### Chain 2: InputMultiOutputJSONCompleteDateExtractor

Extracts date from user question (e.g., "By November 31..." -> "November 31").

Output: `{"date": "November 31"|"", "think": "..."}`

---

### StringToDateMonthForm (utility)

Converts date string to structured format.

Output: `{"day": <int>, "month": <int>}`

Handles: "30 1", "28,2", "13/5", "12 January", "7 march", "19,MAY", "23 - July", etc.

---

### Chain 3: JobAttributeRetriever

Extracts filter attribute for jobs. Keys: name, arrivaldate, duedate, task, workcenter, id.

Output (with filter): `{"attribute": true, "key": "id", "value": 63, "think": "..."}`
Output (no filter): `{"attribute": false, "think": "..."}`

---

### Chain 3: TaskAttributeRetriever

Extracts filter attribute for tasks. Keys: name, id.

Same output format as JobAttributeRetriever.

---

### Chain 3: ResourceAttributeRetriever

Extracts filter attribute for resources. Keys: name, id.

Same output format.

---

### Chain 3: TasksuitableresourceAttributeRetriever

More complex - captures both what user knows and what they search for:

Output: `{"attribute": true, "know": {"info": "resource"|"task", "key": "id"|"name", "value": ...}, "search": {"info": "resource"|"task"|"time"}, "think": "..."}`

---

### Chain 3: TaskprecedencecontraintOrderDependenceClassifier

Classifies: "order" vs "dependence"

Output: `{"pick": "order"|"dependence", "think": "..."}`

---

### Chain 3: TaskprecedenceconstraintOrderAttributeRetriever

For "order" questions - extracts before/after:

Output: `{"attribute": true, "before": <int>|"*", "after": <int>|"*", "think": "..."}`

---

### Chain 3: TaskprecedenceconstraintDependenceAttributeRetriever

For "dependence" questions - extracts reference/target:

Output: `{"attribute": true, "reference": <int>, "target": <int>|"*", "think": "..."}`

---

### Chain 4: JobAttributeReturnClassifier

Determines what the user wants RETURNED about jobs.

Output (specific attribute): `{"attribute": true, "return": "name"|"id"|"task"|"arrivaldate"|"duedate", "think": "..."}`
Output (full object): `{"attribute": false, "think": "..."}`

---

### Chain 4: TaskAttributeReturnClassifier

Returns: "name" or "id"

---

### Chain 4: ResourceAttributeReturnClassifier

Returns: "name", "id", or "period"

---

### Chain 4: TasksuitableresourceAttributeReturnResourceClassifier

Output: `{"attribute": true|false, "key": "name"|"id"|"period", "value": ...(optional), "think": "..."}`

---

### Chain 4: TasksuitableresourceAttributeReturnTaskClassifier

Output: `{"attribute": true|false, "key": "name"|"id"|"time", "value": ...(optional), "think": "..."}`

---

### Chain 5: OutputListResultsTaskJobResourceTasksuitableresource

The main answer prompt. Given only the count of results (not the data). Must include `(DATA)` placeholder exactly once.

Key rules for the LLM:
- Naturally incorporate result count
- Place `(DATA)` as standalone block, never part of a sentence
- Never create lists/bullets representing the data
- Never mention "API", "retrieved data", "placeholders"
- Never assign semantic meaning to "tasks", "jobs", "resources" - treat as domain keys only
- End with follow-up question

---

### Chain 5: OutputNoResultsFound

Politely informs user no matches were found.

---

### Chain 5: OutputListResultsPlanComparisonSingle

Same as main answer prompt + recommends the file with shortest makespan by name.

---

### Chain 5: OutputListResultsPlanComparisonMultiple

Same + mentions all tied plan names using plural language.

---

### Chain 5: OutputListResultsMultipleDocuments

Generic multi-document answer with `(DATA)` placeholder.

---

### Chain 5: OutputListResultsTaskprecedenceconstraints

Given actual constraint info (not just count). Must answer directly based on the provided info, then include `(DATA)`.

---

### Chain 5: OutputTaskprecedenceconstraintsClassifyQuestionBoolean

Determines if the question is yes/no answerable.

Output: `{"attribute": true|false, "think": "..."}`

---

### Chain 5: OutputTaskprecedenceconstraintsAnswerBooleanQuestion

Answers boolean task precedence questions affirmatively, includes `(DATA)`.

---

### Chain 5: OutputTaskprecedenceconstraintsTaskNoExist

Informs user no task found with that ID.

---

### Chain 5: OutputTaskprecedenceconstraintsTaskIsIndependent

Informs user the task is independent (no dependencies).

Two variants:
- target = "*": "the task is independent of other tasks"
- target = specific ID: "the two tasks are independent of each other"

---

### Chain 5: OutputInvalidName

Informs user the file name must contain "input" or "output" but not both.

---

### ExceptionHandler (fallback)

Politely handles errors. Suggests:
1. Rewrite the question more clearly
2. Try again (transient error)
3. Remove format instructions from the question

---

### NoAgentJSONUpload (m=2 mode)

For direct/no-thinking mode. Injects full file content into prompt:
```
The user uploaded a file:
--- filename.json ---
{full JSON content}
--- End of filename.json ---

User Question: ...
```
