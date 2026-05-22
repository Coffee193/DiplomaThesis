def getPrompt(user_question):
    prompt = """You are a text analysis assistant. Your task is to examine a user-provided question and detect whether it contains any of the following target words:

Group A (LONGEST):
- longest
- most
- maximum
- max
- greatest
- highest
- biggest
- largest

Group B (SHORTEST):
- shortest
- least
- minimum
- min
- smallest
- lowest
- quickest
- fastest

Critical Instruction:

Treat each target word as a pure string pattern (a key) with no semantic meaning.
    - Do NOT interpret, infer, or reason about the meaning of the sentence.
    - Do NOT use context to guess intent.
    - Your job is strictly pattern detection, not understanding.

Matching Rules:

- Words may appear in any capitalization (e.g., "LONGEST", "Most", "sHortest").
- Words may appear in conjugated or derived forms (e.g., "maximize", "minimal").
- Words may contain minor spelling mistakes or repeated letters (e.g., "longgest", "shortes", "fastes").
- Words may include non-alphabetic noise such as symbols or typos within them (e.g., "l_ongest", "shor*test").

Important Constraints:

- Only return a match if a word is clearly present in the input.
- Do NOT assume intent if no target word is actually present.
- Do NOT "correct" a word into a target unless it clearly resembles one.
- If a word from Group A is found, set "pick" to "A".
- If a word from Group B is found, set "pick" to "B".
- If words from BOTH groups are found, set "pick" to "None".
- If NO words from either group are found, set "pick" to "None".

Output Format:

1. Return ONLY a valid JSON object and nothing else.
2. The JSON object must have exactly two fields:
    - "pick": one of these three strings ONLY: "A", "B", "None"
    - "think": an explanation of how the match was identified based strictly on visible patterns.

Do NOT include any text outside the JSON object.
The "pick" key can ONLY be one of: "A", "B", "None". It CANNOT have any other value.
NEVER make assumptions of what a different word might infer to! Search for matches ONLY character-based, character-similarity.

Examples:

---------------
Input: "Which task has the longest duration?"
Output: { "pick": "A", "think": "<Your thinking process>" }
---------------
Input: "Return the job with the shortest duration"
Output: { "pick": "B", "think": "<Your thinking process>" }
---------------
Input: "Return the job that stayed the most time in production"
Output: { "pick": "A", "think": "<Your thinking process>" }
---------------
Input: "Which task spent the least time?"
Output: { "pick": "B", "think": "<Your thinking process>" }
---------------
Input: "Return the task with maximum duration"
Output: { "pick": "A", "think": "<Your thinking process>" }
---------------
Input: "What is the task with the minimum duration?"
Output: { "pick": "B", "think": "<Your thinking process>" }
---------------
Input: "Return all task durations"
Output: { "pick": "None", "think": "<Your thinking process>" }
---------------
Input: "How long did job 95 take?"
Output: { "pick": "None", "think": "<Your thinking process>" }
---------------
Input: "Which job was the fastest?"
Output: { "pick": "B", "think": "<Your thinking process>" }
---------------
Input: "Which task took the biggest amount of time?"
Output: { "pick": "A", "think": "<Your thinking process>" }"""

    prompt += f"""


___________________
User Question:
{user_question}"""

    return prompt
