from ollama import chat
import ollama
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

user_question = "Is there a task to be executed before task with id 483?" #old: pos
user_question = "Is there a task to be executed before task 483?" #old: pos
user_question = "Is there a task to be executed before 183?" #old: pos
user_content = 'Which task should i execute before task 1?' #old: pos
user_content = 'What task can i execute after completing task 1?' #old: pos
user_content = 'Which task can i do after task 1?' #old: pos
user_content = 'Does task 53 require another task to be executed beforehand?' #old: none
user_content = 'Is task 11 independent of other tasks?' #old: none

user_prompt = """"""