from ollama import chat
import ollama
import requests

def getweather(city: str):
    """
    Return weather information for a given city

    Args:
        city: The name of the city to get the wheater for
    """
    print(f'Tool called on {city}\n-----\n')
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    return response.json()

#try:
#llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': 'What is the weather in Patras?'}], tools = [getweather]) # llm_answer.message.content = '', llm_answer.message.tool_calls = [... list of function names and arguments] # name='getweather', arguments={'city': 'Patras'}
#llm_answer = chat('llama3.1', messages = [{'role': 'user', 'content': 'Ho how are you?'}], tools = [getweather]) # llm_answer.message.content = '', llm_answer.message.tool_calls = [... list of function names and arguments] # name='getweather', arguments={'city': 'a non-existing city'}
#except ollama._types.ResponseError:
#    print('agugu')

print(llm_answer)
print('*****')
print(llm_answer.message.content)

####
# NOT THE WAY TO GO. IT DOESN'T AUTOMATICALLY DO THE JOB
# USE LANGCHAIN OR CREATE AN AGENT YOURSELF
####