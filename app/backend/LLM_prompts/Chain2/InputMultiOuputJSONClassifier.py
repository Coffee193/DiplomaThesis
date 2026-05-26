def getPrompt(user_question):
    prompt = """You are a text analysis assistant. Your task is to examine a user-provided question and detect whether it contains any of the following target words:

- complete
- start
- end
- duration
- production
- finish
- done

Critical Instruction:

Treat each target word as a pure string pattern (a key) with no semantic meaning.
    - Do NOT interpret, infer, or reason about the meaning of the sentence.
    - Do NOT use context to guess intent.
    - Your job is strictly pattern detection, not understanding.

Matching Rules:

- Words may appear in singular or plural form (e.g., "assignments").
- Words may appear in conjugated, or derived forms (e.g. "completed", "ended", "completion").
- Words may be capitalized in any way (e.g., "dURation", "COMPLETE", "End").
- Words may contain minor spelling mistakes, repeated letters, or extra characters (e.g., "stat", "compllete", "dur ation").
- Words may include non-alphabetic noise such as symbols or typos within them (e.g., "s_tart*", "furation").

Important Constraints:

- Only return words that are clearly present in the input.
- Do NOT assume intent if a word is not actually present.
- Do NOT “correct” a word into a target unless it clearly resembles it.
- If multiple target words are found, return all of them.
- If none are found, return: [].

Output Format:

1. Return ONLY a valid JSON object and nothing else.
2. The JSON object must have exactly two fields:
    - "words": an array containing zero or more of the following strings: "complete", "start", "end", "duration", "production" (all lowercase). It cannot contain a different word from these five
    - "think": an explanation of how the matches were identified based strictly on visible patterns.
    
Do NOT include any text outside the JSON object.
The words key can ONLY contain one or more of these strings: "complete", "start", "end", "duration", "production". It CANNOT have any  other string
Do NOT EVER put the plural form of these strings in the words key. The strings in the word key should ALWAYS be in singular form.
NEVER make assumptions of what a different word might infer to! Search for matches ONLY character-based, character-similarity
NEVER include a word more than one time

Examples:

---------------
Input: "When did job 96 fully complete?"
Output: { "words": ["complete"], "think": "<Your thinking process>" }
---------------
Input: "Which task has the longest duration?"
Output: { "words": ["duration"], "think": "<Your thinking process>" }
---------------
Input: "Which job has the shortest duraation"
Output: { "words": ["duration"], "think": "<Your thinking process>" }
---------------
Input: "By November 31 how many jobs will be completed"
Output: { "words": ["complete"], "think": "<Your thinking process>" }
--------------
Input: "Hello world"
Output: { "words": [], "think": "<Your thinking process>" }
--------------
Input: "When did task 199 start and end"
Output: { "words": ["start", "end"], "think": "<Your thinking process>" }
--------------
Input: "when did job 25 start"
Output: { "words": ["start"], "think": "<Your thinking process>" }
--------------
Input: "How much time did job 59 spend in production?"
Output: { "words": ["production"], "think": "<Your thinking process>" }
---------------
Input: "How many jobs are done before march 15?"
Output: { "words": ["done"], "think": "<Your thinking process>" }
---------------
Input: "By 28-2 how many tasks will finish?"
Output: { "words": ["finish"], "think": "<Your thinking process>" }"""

    prompt += f"""


___________________
User Question:
{user_question}"""

    return prompt