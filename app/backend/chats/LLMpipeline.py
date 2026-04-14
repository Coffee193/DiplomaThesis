from ollama import chat
import json

from LLM_prompts.Chain1 import GibberishClassifier
from LLM_prompts.UnexpectedException import ExceptionHandler
from LLM_prompts.Chain2 import HighLevelClassifier, HighLevelTaskClassifier
from LLM_prompts.Chain3 import ResourceAttributeRetriever, JobAttributeRetriever, TaskAttributeRetriever, TasksuitableresourceAttributeRetriever, TaskprecedencecontraintOrderDependenceClassifier, TaskprecedenceconstraintDependenceAttributeRetriever, TaskprecedenceconstraintOrderAttributeRetriever
from LLM_prompts import StringToDateMonthForm
from LLM_prompts.Chain4 import JobAttributeReturnClassifier, TaskAttributeReturnClassifier, ResourceAttributeReturnClassifier, TasksuitableresourceAttributeReturnResourceClassifier, TasksuitableresourceAttributeReturnTaskClassifier

def IntToStrWithSlabInfornt(val):
    if(type(val) != str):
        val = '_' + str(val)
    return val

def LLMOutClean(answer):
    answer = answer.replace('\n', '')
    if('`' in answer):
        answer = answer.replace('`', '')
        if(answer[:4] == 'json'):
            answer = answer[4:]
    return answer

def PassLLMThink(user_question, json_path):

    ### Chain 1: Gibberish Classifier ###
    ''' Classifies if Question is Gibberish or Not'''
    answer = LLMOutClean(chat('llama3.1', messages = [{'role': 'user', 'content': GibberishClassifier.getPrompt(user_question)}]).message.content)

    try:
        answer = json.loads(answer)
        if(answer['gibberish'] == True):
            return chat('llama3.1', messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}]).message.content
    except:
        return chat('llama3.1', messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}]).message.content
    ### Chain 1 End ###


    ### Chain 2: High Level Classifier (Tasks, Jobs, Resources, TaskSuitableResources, TaskPrepost) ###
    ''' Classifies if user asks about: Jobs, Resources, Tasks, Tasksuitableresources, Taskprecedenceconstraints'''
    answer = LLMOutClean(chat('llama3.1', messages = [{'role': 'user', 'content': HighLevelClassifier.getPrompt(user_question)}]).message.content) # Word-based search

    try:
        answer = json.loads(answer)
        words = answer['words']
        if(len(words) == 0):
            return chat('llama3.1', messages = [{'role': 'user', 'content': user_question}]).message.content
        else:
            if('job' in words):
                search = 'jobs'
            elif('resource' in words and 'task' in words):
                search = 'tasksuitableresources'
            elif(len(words) == 1):
                if('resource' in words):
                    search = 'resources'
                elif('task' in words):
                    answer = chat('llama3.1', messages = [{'role': 'user', 'content': HighLevelTaskClassifier.getPrompt(user_question)}]).message.content # Meaning-search
                    answer = json.loads(LLMOutClean(answer))
                    if(answer['pick'] == 1):
                        search = 'tasksuitableresources'
                    elif(answer['pick'] == 2):
                        search = 'tasksprecedenceconstraints'
                    elif(answer['pick'] == 3):
                        search = 'tasks'
                    else:
                        return chat('llama3.1', messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}]).message.content
    except:
        return chat('llama3.1', messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}]).message.content
    ### Chain 2 End ###


    ### Get JSON Data ###
    ''' Retrieves the JSON data '''
    with open(json_path, encoding = 'utf-8') as file:
        json_data = file.read()
        json_data = json.loads(json_data)
    ### Get JSON Data End ###

    ### Chain 3: Retrieval Classifier ###
    ''' Classifies if user filters based on some specific attribute. Example: 'Get all tasks with id _578' -> finds 'id' and _578'''
    if(search == 'resources'):
        query = json_data["resources"]["resource"]
        prompt = ResourceAttributeRetriever.getPrompt(user_question)
    elif(search == 'jobs'):
        query = json_data["jobs"]["job"]
        prompt = JobAttributeRetriever.getPrompt(user_question)
    elif(search == 'tasks'):
        query = json_data["tasks"]["task"]
        prompt = TaskAttributeRetriever.getPrompt(user_question)
    elif(search == 'tasksuitableresources'):
        query = json_data["tasksuitableresources"]["tasksuitableresource"]
        prompt = TasksuitableresourceAttributeRetriever.getPrompt(user_question)
    elif(search == 'tasksprecedenceconstraints'):
        query = json_data["taskprecedenceconstraints"]["taskprecedenceconstraint"]
        answer = chat('llama3.1', messages = [{'role': 'user', 'content': TaskprecedencecontraintOrderDependenceClassifier.getPrompt(user_question)}]).message.content
        answer = json.loads(LLMOutClean(answer))
        if("order" in answer):
            prompt = TaskprecedenceconstraintOrderAttributeRetriever.getPrompt(user_question)
        elif("dependence" in answer):
            prompt = TaskprecedenceconstraintDependenceAttributeRetriever.getPrompt(user_question)
    else:
        return chat('llama3.1', messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}]).message.content

    answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
    asnwer = LLMOutClean(answer)
    ### Chain 3 End ###


    ### JSON Data Extraction based on Chain 3 ###
    ''' Keeps only the relevant JSON Data based on what was decided from Chain 3 '''
    try:
        retrieve_info = json.loads(answer)
    except:
        retrieve_info = None

    if retrieve_info == None:
        prompt = ExceptionHandler.getPrompt(user_question)
        return chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
    else:
        if(retrieve_info['attribute'] == True):
            
            if(search == 'resources' or search == 'tasks'):
                if(retrieve_info['key'] == 'id'):
                    query = [q for q in query if q[retrieve_info['key']] == IntToStrWithSlabInfornt(retrieve_info['value'])]
                elif(retrieve_info['key'] == 'name'):
                    query = [q for q in query if q[retrieve_info['key']].upper() == retrieve_info['value'].upper()]

            elif(search == 'jobs'):
                if(retrieve_info['key'] == 'id'):
                    query = [q for q in query if q[retrieve_info['key']] == IntToStrWithSlabInfornt(retrieve_info['value'])]
                elif(retrieve_info['key'] == 'name'):
                    query = [q for q in query if q[retrieve_info['key']].upper() == retrieve_info['value'].upper()]
                elif(retrieve_info['key'] == 'task'):
                    query = [q for q in query if any(t.get('refid') == IntToStrWithSlabInfornt(retrieve_info['value']) for t in q.get('jobtaskreference', []))]
                elif(retrieve_info['key'] == 'arrivaldate' or retrieve_info['key'] == 'duedate'):
                    retrieve_info['value'] = json.loads(chat('llama3.1', messages = [{'role': 'user', 'content': StringToDateMonthForm.getPrompt(retrieve_info['value'])}]).message.content)
                    query = [q for q in query if ( q[retrieve_info['key']]['day'] == retrieve_info['value']['day'] and q[retrieve_info['key']]['month'] == retrieve_info['value']['month'])]
            
            elif(search == 'tasksuitableresources'):
                val_get = None
                if(retrieve_info['know']['key'] == 'name'):
                    val_get = [d['id'] for d in json_data[retrieve_info['know']['info'] + 's'][retrieve_info['know']['info']] if d['name'].upper() == retrieve_info['know']['value'].upper()]
                if(val_get != None):
                    query = [q for q in query if q[retrieve_info['know']['info'] + 'reference']['refid'] in val_get] # Fix this <---
                else:
                    query = [q for q in query if q[retrieve_info['know']['info'] + 'reference']['refid'] == IntToStrWithSlabInfornt(retrieve_info['know']['value'])]

            elif(search == 'tasksprecedenceconstraints'):
                if("before" in retrieve_info):
                    if(retrieve_info["before"] != "*"):
                        query = [q for q in query if q['preconditiontaskreference']['refid'] == IntToStrWithSlabInfornt(retrieve_info["before"])]
                    if(retrieve_info["after"] != "*"):
                        query = [q for q in query if q['postconditiontaskreference']['refid'] == IntToStrWithSlabInfornt(retrieve_info["after"])]

                elif("reference" in retrieve_info):
                    if(retrieve_info['target'] == "*"):
                        query = [q for q in query if IntToStrWithSlabInfornt(retrieve_info['reference']) in (q['preconditiontaskreference']['refid'], q['postconditiontaskreference']['refid'])]
                    else:
                        query = [q for q in query if {q['preconditiontaskreference']['refid'], q['postconditiontaskreference']['refid']} == {IntToStrWithSlabInfornt(retrieve_info['reference']), IntToStrWithSlabInfornt(retrieve_info['target'])}]

    ### JSON Data Extraction End ####

    ### Chain 4: Wanted Returned Value Classifier ###
    ''' Classifies what value the user wants returned. Example: 'Return the ids of all tasks named ROLLING' -> finds ids'''
    if(search == 'jobs'):
        prompt = JobAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'tasks'):
        prompt = TaskAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'resources'):
        prompt = ResourceAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'tasksuitableresources'):
        if(retrieve_info['search']['info'] == 'resource'):
            prompt = TasksuitableresourceAttributeReturnResourceClassifier.getPrompt(user_question)
        elif(retrieve_info['search']['info'] == 'task'):
            prompt = TasksuitableresourceAttributeReturnTaskClassifier.getPrompt(user_question)

    if(search != 'tasksprecedenceconstraints'):
        answer = chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
        asnwer = LLMOutClean(answer)
    ### Chain 4 End ###


    ### Data Final Clean Form ###
    if(search == 'jobs'):
        query = [{'name': q['name'], 'arrivaldate': q['arrivaldate'], 'duedate': q['duedate'], 'task': [r['refid'] for r in q['jobtaskreference']], 'workcenter': q['jobworkcenterreference']['refid'], 'id': q['id']} for q in query]
        ### ###
    elif(search == 'tasks'):
        query = [{'name': q['name'], 'id': q['id']} for q in query]
    elif(search == 'resources'):
        query = [{'name': q['name'], 'nonworkingperiods': [{'fromdate': r['fromdate'], 'todate': r['todate']} for r in q['resourceavailability']['nonworkingperiods']['period']], 'id': q['id']} for q in query]
    elif(search == 'tasksuitableresources'):
        taskres_list = []
        for i in range(0, len(query)):
            if(len(taskres_list) == 0 or (not any(fl['resource']['id'] == query[i]['resourcereference']['refid'] for fl in taskres_list)) ):
                taskres_list.append({'resource': {'id': query[i]['resourcereference']['refid'], 'name': [r['name'] for r in json_data['resources']['resource'] if r['id'] == query[i]['resourcereference']['refid']][0]}, 'tasks': [{'id': query[i]['taskreference']['refid'], 'operation_time': query[i]['operationtimeperbatchinseconds'], 'name': [t['name'] for t in json_data['tasks']['task'] if t['id'] == query[i]['taskreference']['refid']][0]}]})
            else:
                next(item for item in taskres_list if item['resource']['id'] == query[i]['resourcereference']['refid'])['tasks'].append({'id': query[i]['taskreference']['refid'], 'operation_time': query[i]['operationtimeperbatchinseconds'], 'name': [t['name'] for t in json_data['tasks']['task'] if t['id'] == query[i]['taskreference']['refid']][0]})
    elif(search == 'tasksprecedenceconstraints'):
        query = [{'before': q['preconditiontaskreference']['refid'], 'next': q['postconditiontaskreference']['refid']} for q in query]
    ### End ###


    ### JSON Data Extraction based on Chain 4 ###
        if(search != 'tasksprecedenceconstraints'):
            try:
                wanted_return = json.loads(answer)
            except:
                wanted_return = None

            if wanted_return == None:
                prompt = ExceptionHandler.getPrompt(user_question)
                return chat('llama3.1', messages = [{'role': 'user', 'content': prompt}]).message.content
            else:
                if(wanted_return['attribute'] == True):
                    if(search != 'tasksuitableresources'):
                        if(wanted_return['return'] == 'name'):
                            query = [{'id': q['id'], 'name': q['name']} for q in query]
                        if(wanted_return['return'] == 'id'):
                            query = [{'id': q['id']} for q in query]
                        elif(wanted_return['return'] == 'task'):
                            query = [{'id': q['id'], 'task': q['task']} for q in query]
                        elif(wanted_return['return'] == 'arrivaldate'):
                            query = [{'id': q['id'], 'arrivaldate': q['arrivaldate']} for q in query]
                        elif(wanted_return['return'] == 'duedate'):
                            query = [{'id': q['id'], 'duedate': q['duedate']} for q in query]
                        elif(wanted_return['return'] == 'period'):
                            query = [{'id': q['id'], 'nonworkingperiods': q['nonworkingperiods']} for q in query]

                    elif(search == 'tasksuitableresources'):
                        if(retrieve_info['search']['info'] == 'resource'):
                            if 'value' not in wanted_return:
                                if wanted_return['key'] == 'id':
                                    for item in taskres_list: item['resource'] = {'id': item['resource']['id']}
                                elif wanted_return['key'] == 'period':
                                    for item in taskres_list: item['resource']['no_work_period'] = [rp['resourceavailability']['nonworkingperiods']['period'] for rp in json_data['resources']['resource'] if rp['id'] == item['resource']['id']][0]
                            
                            else:
                                wanted_return['value'] = IntToStrWithSlabInfornt(wanted_return['value'])
                                fin_list = [item for item in taskres_list if item['resource'][wanted_return['key']].upper() == wanted_return['value'].upper()]
                        elif(retrieve_info['search']['info'] == 'task'):
                            if 'value' not in wanted_return:
                                if wanted_return['key'] == 'id':
                                    for item in taskres_list: item['tasks'] = [{'id': t['id']} for t in item['tasks']]
                                elif wanted_return['key'] == 'name':
                                    for item in taskres_list: item['tasks'] = [{'id': t['id'], 'name': t['name']} for t in item['tasks']]
                                elif wanted_return['key'] == 'time':
                                    for item in taskres_list: item['tasks'] = [{'id': t['id'], 'operation_time': t['operation_time']} for t in item['tasks']]
                            else:
                                wanted_return['value'] = IntToStrWithSlabInfornt(wanted_return['value'])
                                fin_list = [{'resource': item['resource'], 'tasks': [t for t in item['tasks'] if t[wanted_return['key']].upper() == wanted_return['value'].upper()]}  for item in taskres_list if any(t[wanted_return['key']].upper() == wanted_return['value'].upper() for t in item['tasks'])]
    ### JSON Data Extraction End###