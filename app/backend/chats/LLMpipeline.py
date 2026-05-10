from ollama import chat
import json
import os

from LLM_prompts.Chain1 import GibberishClassifier
from LLM_prompts.UnexpectedException import ExceptionHandler
from LLM_prompts.Chain2 import HighLevelClassifier, HighLevelTaskClassifier
from LLM_prompts.Chain3 import ResourceAttributeRetriever, JobAttributeRetriever, TaskAttributeRetriever, TasksuitableresourceAttributeRetriever, TaskprecedencecontraintOrderDependenceClassifier, TaskprecedenceconstraintDependenceAttributeRetriever, TaskprecedenceconstraintOrderAttributeRetriever
from LLM_prompts import StringToDateMonthForm
from LLM_prompts.Chain4 import JobAttributeReturnClassifier, TaskAttributeReturnClassifier, ResourceAttributeReturnClassifier, TasksuitableresourceAttributeReturnResourceClassifier, TasksuitableresourceAttributeReturnTaskClassifier
from LLM_prompts.Chain5 import OutputNoResultsFound, OutputListResultsTaskJobResourceTasksuitableresource, OutputTaskprecedenceconstraintsTaskNoExist, OutputListResultsTaskprecedenceconstraints, OutputTaskprecedenceconstraintsTaskIsIndependent, OutputTaskprecedenceconstraintsClassifyQuestionBoolean, OutputTaskprecedenceconstraintsAnswerBooleanQuestion
from LLM_prompts.FindJSONFile import InstructUploadJSON
from LLM_prompts.UploadJSONFileNoQuestion import UserUploadJSONNoQuestion
from LLM_prompts.UploadJSONFileIrrelevantQuestion import UserUploadJSONIrrelevantQuestion
from LLM_prompts.TitleGeneration import TitleJSONUploadNoQuestion, TitleJSONUploadRelevantQuestion, TitleOnlyQuestionNoJSON, TitlteJSONUploadIrrelevantQuestion, TittleGibberishInput
from LLM_prompts.JSONUploadNoQuestion import JSONUploadNoQuestion
from LLM_prompts.JSONQuestionNoPath import JSONQuestionNoPath

chatdocumentpath = os.environ.get('CHAT_DOCUMENT_PATH')

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

def QueryToInfoNaturalLanguage(query):
    text = ''
    for i in range (0, len(query)):
        text += f'Execute task {query[i]['before']} before task {query[i]['next']}'
        if( i + 1 != len(query)):
            text += '\n'
    return text

def CreateChatConv(db_chat, user_question, file_name = None):

    llm_chat = []

    for conv in db_chat:
        if 'd' in conv:
            if 'q' in conv:
                prompt = f"""User Question:
{conv['q']}

-----------------------
The user has also uploaded a file located at:
{conv['d']['path']}"""
            else:
                prompt = f"""The user has uploaded a file located at:
{conv['d']['path']}"""

            llm_chat += [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': conv['a']}] 
        else:
            llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]

    if file_name == None:
        llm_chat.append({'role': 'user', 'content': user_question})
    else:
        if(user_question == ''):
            llm_chat.append({'role': 'user', 'content': UserUploadJSONNoQuestion.getPrompt(file_name)})
        else:
            llm_chat.append({'role': 'user', 'content': UserUploadJSONIrrelevantQuestion.getPrompt(file_name, user_question)})

    return llm_chat

# Used when could only Upload One File
def GetLastFileFromChat_Old(db_chat, conv_id):
    for i in range(len(db_chat) - 1, -1, -1):
        if 'd' in db_chat[i]:
            return {'id': db_chat[i]['d']['id'], 'name': db_chat[i]['d']['name']}
    return None

def GetLastFileFromChat(db_chat):
    for i in range(len(db_chat) - 1, -1, -1):
        if 'd' in db_chat[i]:
            return [{'id': d['id'], 'name': d['name']} for d in db_chat[i]['d']]
    return None

def PassLLMThink(llm_model, user_question, db_chat = [], json_document = None):
    think_list = []
    print('subemela')
    print(json_document)
    ### Chain 0: Recongise Upload ###
    if(json_document != None and user_question == ''):
        if(len(json_document) == 1):
            return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': JSONUploadNoQuestion.getPrompt(json_document[0]['name'])}], stream = True), 'think': think_list, 'end': 'success_unfinished'}
        else:
            asokdasoi
    ### Recognise Upload End ###

    ### Chain 1: Gibberish Classifier ###
    ''' Classifies if Question is Gibberish or Not'''
    answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': GibberishClassifier.getPrompt(user_question)}]).message.content)
    print('--Chain 1--')
    print(answer)
    try:
        answer = json.loads(answer)
        think_list.append({'chain': '1', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
        if(answer['gibberish'] == True):
            return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'success_unfinished'}
    except:
        return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'fail_error'}
    ### Chain 1 End ###

    ### Chain 2: High Level Classifier (Tasks, Jobs, Resources, TaskSuitableResources, TaskPrepost) ###
    ''' Classifies if user asks about: Jobs, Resources, Tasks, Tasksuitableresources, Taskprecedenceconstraints'''
    answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': HighLevelClassifier.getPrompt(user_question)}]).message.content) # Word-based search
    print('--Chain 2--')
    print(answer)
    try:
        answer = json.loads(answer)
        think_list.append({'chain': '2', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
        words = answer['words']
        if(len(words) == 0):
            # NOT asking about Jobs, Tasks, etc.. So a general, non-json question
            if(json_document == None or len(json_document) == 1):
                return {'response_msg': chat(llm_model, messages = CreateChatConv(db_chat, user_question, json_document[0]['name'] if json_document != None else None), stream = True), 'think': think_list, 'end': 'success_unfinished'}
            else:
                saopdksaoop
        else:
            if('job' in words):
                search = 'jobs'
            elif('resource' in words and 'task' in words):
                search = 'tasksuitableresources'
            elif(len(words) == 1):
                if('resource' in words):
                    search = 'resources'
                elif('task' in words):
                    answer = chat(llm_model, messages = [{'role': 'user', 'content': HighLevelTaskClassifier.getPrompt(user_question)}]).message.content # Meaning-search
                    answer = json.loads(LLMOutClean(answer))
                    think_list.append({'chain': '2_task', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
                    if(answer['pick'] == 1):
                        search = 'tasksuitableresources'
                    elif(answer['pick'] == 2):
                        search = 'tasksprecedenceconstraints'
                    elif(answer['pick'] == 3):
                        search = 'tasks'
                    else:
                        return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'fail_error'}
            else:
                return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'fail_error'}
    except:
        return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'fail_error'}
    ### Chain 2 End ###
    print('--Chain 2 End--')
    print(answer)
    print(search)
    ### Get File If None Provided ###
    '''User asks file related question without providing a file. Searches chat for last provided file'''
    if(json_document == None):
        json_document = GetLastFileFromChat(db_chat)
        if(json_document == None):
            return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': JSONQuestionNoPath.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'success_unfinished', 'search': search}
    ### Get File If None Provided End ###
    print('--Get File If None--')
    print(json_document)
    ### Chain 3: Retrieval Classifier ###
    ''' Classifies if user filters based on some specific attribute. Example: 'Get all tasks with id _578' -> finds 'id' and _578'''
    if(search == 'resources'):
        prompt = ResourceAttributeRetriever.getPrompt(user_question)
    elif(search == 'jobs'):
        prompt = JobAttributeRetriever.getPrompt(user_question)
    elif(search == 'tasks'):
        prompt = TaskAttributeRetriever.getPrompt(user_question)
    elif(search == 'tasksuitableresources'):
        prompt = TasksuitableresourceAttributeRetriever.getPrompt(user_question)
    elif(search == 'tasksprecedenceconstraints'):
        answer = chat(llm_model, messages = [{'role': 'user', 'content': TaskprecedencecontraintOrderDependenceClassifier.getPrompt(user_question)}]).message.content
        try:
            answer = json.loads(LLMOutClean(answer))
            taskprecedenceconstraints_pick = answer["pick"]
            think_list.append({'chain': '3_taskprecon_orderdepend', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
            if(answer["pick"] == "order"):
                prompt = TaskprecedenceconstraintOrderAttributeRetriever.getPrompt(user_question)
            elif(answer["pick"] == "dependence"):
                prompt = TaskprecedenceconstraintDependenceAttributeRetriever.getPrompt(user_question)
        except:
            return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'fail_error', 'search': search}
    else:
        return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'fail_error', 'search': search}

    answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': prompt}]).message.content)
    
    # JSON Retrieve Information #
    try:
        retrieve_info = json.loads(answer)
        think_list.append({'chain': '3', 'think': retrieve_info['think'] if 'think' in retrieve_info else 'Exception No Thinking Return from LLM'})
    except:
        retrieve_info = None

    if retrieve_info == None or 'attribute' not in retrieve_info:
        return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'fail_error', 'search': search}
    # End JSON Retrieve Information #
    ### Chain 3 End ###
    print('--Chain 3--')
    print(answer)
    print(retrieve_info)
    ### Chain 4: Wanted Returned Value Classifier ###
    ''' Classifies what value the user wants returned. Example: 'Return the ids of all tasks named ROLLING' -> finds ids'''
    if(search == 'jobs'):
        prompt = JobAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'tasks'):
        prompt = TaskAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'resources'):
        prompt = ResourceAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'tasksuitableresources'):
        if(retrieve_info['attribute'] == True):
            if(retrieve_info['search']['info'] == 'resource'):
                prompt = TasksuitableresourceAttributeReturnResourceClassifier.getPrompt(user_question)
            elif(retrieve_info['search']['info'] == 'task'):
                prompt = TasksuitableresourceAttributeReturnTaskClassifier.getPrompt(user_question)
    wanted_return = None
    if(search != 'tasksprecedenceconstraints'):
        answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': prompt}]).message.content)

    if(search != 'tasksprecedenceconstraints'):
        try:
            wanted_return = json.loads(answer)
            think_list.append({'chain': '4', 'think': wanted_return['think'] if 'think' in wanted_return else 'Exception No Thinking Return from LLM'})
        except:
            wanted_return = None

        if wanted_return == None or 'attribute' not in wanted_return:
            return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'fail_error', 'search': search, 'retrieve_info': retrieve_info}
    ### Chain 4 End ###
    print('Chain 4 Finished')
    print(answer)
    return {'end': 'success_complete', 'think': think_list, 'search': search, 'retrieve_info': retrieve_info, 'wanted_return': wanted_return, 'json_documents': json_document, 'taskprecedenceconstraints_pick': None if search != 'tasksprecedenceconstraints' else taskprecedenceconstraints_pick}

def LLMGetFinalQuery(conv_id, search, json_documents, retrieve_info, llm_model, wanted_return):

    fetched_results = []
    print(json_documents)
    print('*********')
    for doc in json_documents:
        ### Get JSON Data ###
        ''' Retrieves the JSON data '''
        with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(doc['id']) + '.' + doc['name'].split('.')[-1], encoding = 'utf-8') as file:
            json_data = file.read()
            json_data = json.loads(json_data)
        ### Get JSON Data End ###

        ### Query Form Based on Chain 2 ###
        ''' Classifies if user asks about: Jobs, Resources, Tasks, Tasksuitableresources, Taskprecedenceconstraints'''
        if(search == 'resources'):
            query = json_data["resources"]["resource"]
        elif(search == 'jobs'):
            query = json_data["jobs"]["job"]
        elif(search == 'tasks'):
            query = json_data["tasks"]["task"]
        elif(search == 'tasksuitableresources'):
            query = json_data["tasksuitableresources"]["tasksuitableresource"]
        elif(search == 'tasksprecedenceconstraints'):
            query = json_data["taskprecedenceconstraints"]["taskprecedenceconstraint"]
        ### End Chain 2 Query ###
        print('==Chain 2==')
        print(query)
        ### Query Form Based on Chain 3 ###
        ''' Classifies if user filters based on some specific attribute. Example: 'Get all tasks with id _578' -> finds 'id' and _578'''
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
                    retrieve_info['value'] = json.loads(chat(llm_model, messages = [{'role': 'user', 'content': StringToDateMonthForm.getPrompt(retrieve_info['value'])}]).message.content)
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

        ### End Chain 3 Query ###

        ### Data Final Clean Form ###
        if(search == 'jobs'):
            query = [{'name': q['name'], 'arrivaldate': q['arrivaldate'], 'duedate': q['duedate'], 'task': [r['refid'] for r in q['jobtaskreference']], 'workcenter': q['jobworkcenterreference']['refid'], 'id': q['id']} for q in query]
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
            query = taskres_list
        elif(search == 'tasksprecedenceconstraints'):
            query = [{'before': q['preconditiontaskreference']['refid'], 'next': q['postconditiontaskreference']['refid']} for q in query]
        ### End Data Final Clean Form ###

        ###  Query Form Based on Chain 4 ###
        if(search != 'tasksprecedenceconstraints'):
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
                            query = taskres_list
                        else:
                            wanted_return['value'] = IntToStrWithSlabInfornt(wanted_return['value'])
                            query = [item for item in taskres_list if item['resource'][wanted_return['key']].upper() == wanted_return['value'].upper()]
                    elif(retrieve_info['search']['info'] == 'task'):
                        if 'value' not in wanted_return:
                            if wanted_return['key'] == 'id':
                                for item in taskres_list: item['tasks'] = [{'id': t['id']} for t in item['tasks']]
                            elif wanted_return['key'] == 'name':
                                for item in taskres_list: item['tasks'] = [{'id': t['id'], 'name': t['name']} for t in item['tasks']]
                            elif wanted_return['key'] == 'time':
                                for item in taskres_list: item['tasks'] = [{'id': t['id'], 'operation_time': t['operation_time']} for t in item['tasks']]
                            query = taskres_list
                        else:
                            wanted_return['value'] = IntToStrWithSlabInfornt(wanted_return['value'])
                            query = [{'resource': item['resource'], 'tasks': [t for t in item['tasks'] if t[wanted_return['key']].upper() == wanted_return['value'].upper()]}  for item in taskres_list if any(t[wanted_return['key']].upper() == wanted_return['value'].upper() for t in item['tasks'])]
        ### End Chain 4 Query ###

        fetched_results.append({"query": query, "json_data": json_data, "doc": doc})
    
    print('fetched res >>>')
    print(fetched_results)
    return fetched_results

def PassLLMFinalAnswer(json_document, search, user_question, query, retrieve_info, json_data, llm_model, think_list, taskprecedenceconstraints_pick):
    print('Fin AA**')
    print(json_document)
    if(len(json_document) == 1):
        return PassLLMFinalAnswerSingleDocument(search, user_question, query, retrieve_info, json_data, llm_model, think_list, taskprecedenceconstraints_pick)
    else:
        afasddsad

def PassLLMFinalAnswerSingleDocument(search, user_question, query, retrieve_info, json_data, llm_model, think_list, taskprecedenceconstraints_pick):
    print('Single___')
    print(taskprecedenceconstraints_pick)
    print(retrieve_info)
    print(query)
    print('ppppppppppppp')
    ### Chain 5: Final Answer ###
    if(search != 'tasksprecedenceconstraints'):
        if(len(query[0]) == 0):
            prompt = OutputNoResultsFound.getPrompt(user_question)
        else:
            prompt = OutputListResultsTaskJobResourceTasksuitableresource.getPrompt(user_question, len(query[0]))
    else:
        print('Chain5 aa')
        print(taskprecedenceconstraints_pick)
        print(retrieve_info)
        print(query)
        if(taskprecedenceconstraints_pick == "dependence"):
            if(len(query[0]) == 0):
                if(IntToStrWithSlabInfornt(retrieve_info['reference']) not in [q['id'] for q in json_data["tasks"]["task"]]):
                    prompt = OutputTaskprecedenceconstraintsTaskNoExist.getPrompt(user_question)
                else:
                    prompt = OutputTaskprecedenceconstraintsTaskIsIndependent.getPrompt(user_question, retrieve_info['target'])
            else:
                if(len(query[0]) == 1):
                    print(QueryToInfoNaturalLanguage(query[0]))
                    print('ooooooooooooo')
                    prompt = OutputListResultsTaskprecedenceconstraints.getPrompt(user_question, QueryToInfoNaturalLanguage(query[0]))
                else:
                    prompt = OutputListResultsTaskJobResourceTasksuitableresource.getPrompt(user_question, len(query[0]))
        elif(taskprecedenceconstraints_pick == "order"):
            if(len(query[0]) == 0):
                prompt = OutputNoResultsFound.getPrompt(user_question)
            else:
                bool_classify = chat(llm_model, messages = [{'role': 'user', 'content': OutputTaskprecedenceconstraintsClassifyQuestionBoolean.getPrompt(user_question)}]).message.content
                bool_classify = LLMOutClean(bool_classify)
                try:
                    bool_classify = json.loads(bool_classify)
                    think_list.append({'chain': '5_taskprecon_boolquestion', 'think': bool_classify['think'] if 'think' in bool_classify else 'Exception No Thinking Return from LLM'})
                    if(bool_classify['attribute'] == True):
                        prompt = OutputTaskprecedenceconstraintsAnswerBooleanQuestion.getPrompt(user_question, len(query[0]))
                    else:
                        print(QueryToInfoNaturalLanguage(query[0]))
                        print('oooooooooooooooo')
                        prompt = OutputListResultsTaskprecedenceconstraints.getPrompt(user_question, QueryToInfoNaturalLanguage(query[0]))
                except:
                    prompt = ExceptionHandler.getPrompt(user_question)
    ### Chain 5 End ###
    print('Chain 5 Finished')
    print(prompt)
    print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
    print(query)
    print(search)
    print(think_list)

    return [chat(llm_model, messages = [{'role': 'user', 'content': prompt}], stream = True), think_list, query, search]

def PassLLMThinkCompletePipeline(llm_model, user_question, conv_id, db_chat = [], json_document = None):
    print('sk')
    llm_res = PassLLMThink(llm_model, user_question, db_chat, json_document)
    print(llm_res)
    print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
    if(llm_res['end'] != 'success_complete'):
        return [llm_res['response_msg'], llm_res['think'], None, None if 'search' not in llm_res else llm_res['search']]
    else:
        fetched_results = LLMGetFinalQuery(conv_id, llm_res['search'], llm_res['json_documents'], llm_res['retrieve_info'], llm_model, llm_res['wanted_return'])
    return PassLLMFinalAnswer(llm_res['json_documents'], llm_res['search'], user_question, [fr["query"] for fr in fetched_results], llm_res['retrieve_info'], [fr["json_data"] for fr in fetched_results], llm_model, llm_res['think'], llm_res['taskprecedenceconstraints_pick'])

''' #!!!###
YOU NEED TO TEST:
GetLastFileFromChat
PassLLMThink
LLMGetFinalQuery
PassLLMFinalAnswer
PassLLMFinalAnswerSingleDocument
PassLLMThinkCompletePipeline

ERROR in LLMGetFinalQuery:: ---> CREATES THIS: [[...]] AND I WANT IT TO CREATE THIS: [...]

CHANGE AnswerQuestionLLMThink of views, so that it uploads list to mongodb. Also it uploads appropriate fetched items
'''

# Query creation and LLM thinking happen simultaniously. Need to separate these two processes
def PassLLMThink_Old(llm_model, user_question, conv_id, db_chat = [], json_document = None):

    think_list = []

    ### Recongise Upload ###
    if(json_document != None and user_question == ''):
        return [chat(llm_model, messages = [{'role': 'user', 'content': JSONUploadNoQuestion.getPrompt(json_document['name'])}], stream = True), think_list, None, None]
    ### Recognise Upload End ###

    ### Chain 1: Gibberish Classifier ###
    ''' Classifies if Question is Gibberish or Not'''
    answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': GibberishClassifier.getPrompt(user_question)}]).message.content)

    try:
        answer = json.loads(answer)
        think_list.append({'chain': '1', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
        if(answer['gibberish'] == True):
            return [chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), think_list, None, None]
    except:
        return [chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), think_list, None, None]
    ### Chain 1 End ###
  
    ### Chain 2: High Level Classifier (Tasks, Jobs, Resources, TaskSuitableResources, TaskPrepost) ###
    ''' Classifies if user asks about: Jobs, Resources, Tasks, Tasksuitableresources, Taskprecedenceconstraints'''
    answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': HighLevelClassifier.getPrompt(user_question)}]).message.content) # Word-based search

    try:
        answer = json.loads(answer)
        think_list.append({'chain': '2', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
        words = answer['words']
        if(len(words) == 0):
            return [chat(llm_model, messages = CreateChatConv(db_chat, user_question, json_document['name'] if json_document != None else None), stream = True), think_list, None, None]
        else:
            if('job' in words):
                search = 'jobs'
            elif('resource' in words and 'task' in words):
                search = 'tasksuitableresources'
            elif(len(words) == 1):
                if('resource' in words):
                    search = 'resources'
                elif('task' in words):
                    answer = chat(llm_model, messages = [{'role': 'user', 'content': HighLevelTaskClassifier.getPrompt(user_question)}]).message.content # Meaning-search
                    answer = json.loads(LLMOutClean(answer))
                    think_list.append({'chain': '2_task', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
                    if(answer['pick'] == 1):
                        search = 'tasksuitableresources'
                    elif(answer['pick'] == 2):
                        search = 'tasksprecedenceconstraints'
                    elif(answer['pick'] == 3):
                        search = 'tasks'
                    else:
                        return [chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), think_list, None, None]
    except:
        return [chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), think_list, None, None]
    ### Chain 2 End ###

    ### Get File If None Provided ###
    '''User asks file related question without providing a file. Searches chat for last provided file'''
    if(json_document == None):
        json_document = GetLastFileFromChat(db_chat, conv_id)
        if(json_document == None):
            return [chat(llm_model, messages = [{'role': 'user', 'content': JSONQuestionNoPath.getPrompt(user_question)}], stream = True), think_list, None, search]
    ### Get File If None Provided End ###

    ### Get JSON Data ###
    ''' Retrieves the JSON data '''
    with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(json_document['id']) + '.' + json_document['name'].split('.')[-1], encoding = 'utf-8') as file:
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
        answer = chat(llm_model, messages = [{'role': 'user', 'content': TaskprecedencecontraintOrderDependenceClassifier.getPrompt(user_question)}]).message.content
        try:
            answer = json.loads(LLMOutClean(answer))
            taskprecedenceconstraints_pick = answer["pick"]
            think_list.append({'chain': '3_taskprecon_orderdepend', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
            if(answer["pick"] == "order"):
                prompt = TaskprecedenceconstraintOrderAttributeRetriever.getPrompt(user_question)
            elif(answer["pick"] == "dependence"):
                prompt = TaskprecedenceconstraintDependenceAttributeRetriever.getPrompt(user_question)
        except:
            return [chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream = True), think_list, None, search]
    else:
        return [chat(llm_model, messages = [{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}]).message.content, think_list, None, search]

    answer = chat(llm_model, messages = [{'role': 'user', 'content': prompt}]).message.content
    answer = LLMOutClean(answer)
    ### Chain 3 End ###
    print('Chain 3 Finished')
    print(answer)
    print(search)
    ### JSON Data Extraction based on Chain 3 ###
    ''' Keeps only the relevant JSON Data based on what was decided from Chain 3 '''
    try:
        retrieve_info = json.loads(answer)
        think_list.append({'chain': '3', 'think': retrieve_info['think'] if 'think' in retrieve_info else 'Exception No Thinking Return from LLM'})
    except:
        retrieve_info = None

    if retrieve_info == None:
        prompt = ExceptionHandler.getPrompt(user_question)
        return [chat(llm_model, messages = [{'role': 'user', 'content': prompt}]).message.content, think_list, None, search]
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
                    retrieve_info['value'] = json.loads(chat(llm_model, messages = [{'role': 'user', 'content': StringToDateMonthForm.getPrompt(retrieve_info['value'])}]).message.content)
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
    print(query)
    ### Chain 4: Wanted Returned Value Classifier ###
    ''' Classifies what value the user wants returned. Example: 'Return the ids of all tasks named ROLLING' -> finds ids'''
    if(search == 'jobs'):
        prompt = JobAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'tasks'):
        prompt = TaskAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'resources'):
        prompt = ResourceAttributeReturnClassifier.getPrompt(user_question)
    elif(search == 'tasksuitableresources'):
        if(retrieve_info['attribute'] == True):
            if(retrieve_info['search']['info'] == 'resource'):
                prompt = TasksuitableresourceAttributeReturnResourceClassifier.getPrompt(user_question)
            elif(retrieve_info['search']['info'] == 'task'):
                prompt = TasksuitableresourceAttributeReturnTaskClassifier.getPrompt(user_question)

    if(search != 'tasksprecedenceconstraints'):
        answer = chat(llm_model, messages = [{'role': 'user', 'content': prompt}]).message.content
        asnwer = LLMOutClean(answer)
    ### Chain 4 End ###
    print('Chain 4 Finished')
    print(answer)
    ### Data Final Clean Form ###
    if(search == 'jobs'):
        query = [{'name': q['name'], 'arrivaldate': q['arrivaldate'], 'duedate': q['duedate'], 'task': [r['refid'] for r in q['jobtaskreference']], 'workcenter': q['jobworkcenterreference']['refid'], 'id': q['id']} for q in query]
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
        query = taskres_list
    elif(search == 'tasksprecedenceconstraints'):
        query = [{'before': q['preconditiontaskreference']['refid'], 'next': q['postconditiontaskreference']['refid']} for q in query]
    ### End ###
    print('Cleaned data')
    print(query)
    ### JSON Data Extraction based on Chain 4 ###
    if(search != 'tasksprecedenceconstraints'):
        try:
            wanted_return = json.loads(answer)
            think_list.append({'chain': '4', 'think': wanted_return['think'] if 'think' in wanted_return else 'Exception No Thinking Return from LLM'})
        except:
            wanted_return = None

        if wanted_return == None:
            prompt = ExceptionHandler.getPrompt(user_question)
            return [chat(llm_model, messages = [{'role': 'user', 'content': prompt}]).message.content, think_list, None, search]
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
                            query = taskres_list
                        else:
                            wanted_return['value'] = IntToStrWithSlabInfornt(wanted_return['value'])
                            query = [item for item in taskres_list if item['resource'][wanted_return['key']].upper() == wanted_return['value'].upper()]
                    elif(retrieve_info['search']['info'] == 'task'):
                        if 'value' not in wanted_return:
                            if wanted_return['key'] == 'id':
                                for item in taskres_list: item['tasks'] = [{'id': t['id']} for t in item['tasks']]
                            elif wanted_return['key'] == 'name':
                                for item in taskres_list: item['tasks'] = [{'id': t['id'], 'name': t['name']} for t in item['tasks']]
                            elif wanted_return['key'] == 'time':
                                for item in taskres_list: item['tasks'] = [{'id': t['id'], 'operation_time': t['operation_time']} for t in item['tasks']]
                            query = taskres_list
                        else:
                            wanted_return['value'] = IntToStrWithSlabInfornt(wanted_return['value'])
                            query = [{'resource': item['resource'], 'tasks': [t for t in item['tasks'] if t[wanted_return['key']].upper() == wanted_return['value'].upper()]}  for item in taskres_list if any(t[wanted_return['key']].upper() == wanted_return['value'].upper() for t in item['tasks'])]
    ### JSON Data Extraction End###
    print('Chain 4 Finished')
    print(query)
    ### Chain 5: Final Answer ###
    if(search != 'tasksprecedenceconstraints'):
        if(len(query) == 0):
            prompt = OutputNoResultsFound.getPrompt(user_question)
        else:
            prompt = OutputListResultsTaskJobResourceTasksuitableresource.getPrompt(user_question, len(query))
    else:
        print('Chain5 aa')
        print(taskprecedenceconstraints_pick)
        print(retrieve_info)
        print(QueryToInfoNaturalLanguage(query))
        if(taskprecedenceconstraints_pick == "dependence"):
            if(len(query) == 0):
                if(IntToStrWithSlabInfornt(retrieve_info['reference']) not in [q['id'] for q in json_data["tasks"]["task"]]):
                    prompt = OutputTaskprecedenceconstraintsTaskNoExist.getPrompt(user_question)
                else:
                    prompt = OutputTaskprecedenceconstraintsTaskIsIndependent.getPrompt(user_question, retrieve_info['target'])
            else:
                if(len(query) == 1):
                    prompt = OutputListResultsTaskprecedenceconstraints.getPrompt(user_question, QueryToInfoNaturalLanguage(query))
                else:
                    prompt = OutputListResultsTaskJobResourceTasksuitableresource.getPrompt(user_question, len(query))
        elif(taskprecedenceconstraints_pick == "order"):
            if(len(query) == 0):
                prompt = OutputNoResultsFound.getPrompt(user_question)
            else:
                bool_classify = chat(llm_model, messages = [{'role': 'user', 'content': OutputTaskprecedenceconstraintsClassifyQuestionBoolean.getPrompt(user_question)}]).message.content
                bool_classify = LLMOutClean(bool_classify)
                try:
                    bool_classify = json.loads(bool_classify)
                    think_list.append({'chain': '5_taskprecon_boolquestion', 'think': bool_classify['think'] if 'think' in bool_classify else 'Exception No Thinking Return from LLM'})
                    if(bool_classify['attribute'] == True):
                        prompt = OutputTaskprecedenceconstraintsAnswerBooleanQuestion.getPrompt(user_question, len(query))
                    else:
                        prompt = OutputListResultsTaskprecedenceconstraints.getPrompt(user_question, QueryToInfoNaturalLanguage(query))
                except:
                    prompt = ExceptionHandler.getPrompt(user_question)
    ### Chain 5 End ###
    print('Chain 5 Finished')
    print(prompt)

    return [chat(llm_model, messages = [{'role': 'user', 'content': prompt}], stream = True), think_list, query, search]

def CreateConversationTitleThink(llm_model, user_question = '', file_name = None):
    
    ### Chain 1: Gibberish Classifier ###
    ''' Classifies if Question is Gibberish or Not'''
    if(user_question != ''):
        answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': GibberishClassifier.getPrompt(user_question)}]).message.content)

        try:
            answer = json.loads(answer)
            if(answer['gibberish'] == True):
                return chat(llm_model, messages = [{'role': 'user', 'content': TittleGibberishInput.getPrompt()}]).message.content
        except:
            return None
    ### Chain 1 End ###

    ### Chain 2: Title Generation ###
    if(file_name != None):
        if(user_question == ''):
            return chat(llm_model, messages = [{'role': 'user', 'content': TitleJSONUploadNoQuestion.getPrompt()}]).message.content
        else:
            answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': HighLevelClassifier.getPrompt(user_question)}]).message.content)
            try:
                answer = json.loads(answer)
                words = answer['words']
                if(len(words) == 0):
                    return chat(llm_model, messages = [{'role': 'user', 'content': TitlteJSONUploadIrrelevantQuestion.getPrompt(user_question, file_name)}]).message.content
                else:
                    return chat(llm_model, messages = [{'role': 'user', 'content': TitleJSONUploadRelevantQuestion.getPrompt(user_question)}]).message.content
            except:
                return None
    else:
        return chat(llm_model, messages = [{'role': 'user', 'content': TitleOnlyQuestionNoJSON.getPrompt(user_question)}]).message.content
    ### Chain 2 End ###