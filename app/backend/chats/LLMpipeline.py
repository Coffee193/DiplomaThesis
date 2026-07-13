from ollama import chat
import json
import os
import re
import datetime

from LLM_prompts.Chain1 import GibberishClassifier
from LLM_prompts.UnexpectedException import ExceptionHandler
from LLM_prompts.Chain2 import HighLevelClassifier, HighLevelTaskClassifier, HighLevelOutputJSONClassifier, InputMultiOuputJSONClassifier, InputMultiOutputJSONDurationLongestShortestClassifier, InputMultiOutputJSONCompleteDateExtractor, HighLevelPlanClassifier
from LLM_prompts.InvalidDate import InvalidCompleteDateResponse
from LLM_prompts.JobDuration import JobDurationNoInputFile
from LLM_prompts.JobStartEnd import JobStartEndNoFusedPair
from LLM_prompts.JobComplete import JobCompleteNoFusedPair
from LLM_prompts.PlanComparison import PlanComparisonNoOutputFiles
from LLM_prompts.Chain3 import ResourceAttributeRetriever, JobAttributeRetriever, TaskAttributeRetriever, TasksuitableresourceAttributeRetriever, TaskprecedencecontraintOrderDependenceClassifier, TaskprecedenceconstraintDependenceAttributeRetriever, TaskprecedenceconstraintOrderAttributeRetriever
from LLM_prompts import StringToDateMonthForm
from LLM_prompts.Chain4 import JobAttributeReturnClassifier, TaskAttributeReturnClassifier, ResourceAttributeReturnClassifier, TasksuitableresourceAttributeReturnResourceClassifier, TasksuitableresourceAttributeReturnTaskClassifier
from LLM_prompts.Chain5 import OutputNoResultsFound, OutputListResultsTaskJobResourceTasksuitableresource, OutputTaskprecedenceconstraintsTaskNoExist, OutputListResultsTaskprecedenceconstraints, OutputTaskprecedenceconstraintsTaskIsIndependent, OutputTaskprecedenceconstraintsClassifyQuestionBoolean, OutputTaskprecedenceconstraintsAnswerBooleanQuestion, OutputListResultsMultipleDocuments, OutputInvalidName, OutputListResultsPlanComparisonSingle, OutputListResultsPlanComparisonMultiple
from LLM_prompts.FindJSONFile import InstructUploadJSON
from LLM_prompts.UploadJSONFileNoQuestion import UserUploadJSONNoQuestion, UserUploadMultipleJSONNoQuestion
from LLM_prompts.UploadJSONFileIrrelevantQuestion import UserUploadJSONIrrelevantQuestion, UserUploadMultipleJSONIrrelevantQuestion
from LLM_prompts.TitleGeneration import TitleJSONUploadNoQuestion, TitleJSONUploadRelevantQuestion, TitleOnlyQuestionNoJSON, TitlteJSONUploadIrrelevantQuestion, TittleGibberishInput
from LLM_prompts.JSONUploadNoQuestion import JSONUploadNoQuestion, MultipleJSONUploadNoQuestion
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

def CreateChatConv(db_chat, user_question, file_name = None, conv_id = None):
    print('oly$')
    print(file_name)
    print(db_chat)
    llm_chat = []
    ### <--- NEED TO FIX THIS. d is of the form:
    '''
    ... 'd': [{'id': 317270766108037120, 'name': 'OutputJSON_1.json', 'size': '8.0'}, {'id': 317270766108037121, 'name': 'InputJSON_3.json', 'size': '124.8'}, {'id': 317270766108037122, 'name': 'InputJSON_5.json', 'size': '68.9'}], 'q': 'Return all assignments'}, ...
    '''
    for conv in db_chat:
        if 'd' in conv:
            if 'q' in conv:
                prompt = f"""User Question:
{conv['q']}

-----------------------
The user has also uploaded files located at:
{', '.join(chatdocumentpath + '/' + str(conv_id) + '_' + str(d['id']) + '.' + d['name'].split('.')[-1] for d in conv['d'])}"""
            else:
                prompt = f"""The user has uploaded files located at:
{', '.join(chatdocumentpath + '/' + str(conv_id) + '_' + str(d['id']) + '.' + d['name'].split('.')[-1] for d in conv['d'])}"""

            llm_chat += [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': conv['a']}] 
        else:
            llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]
    print('HUANG*')
    if file_name == None:
        llm_chat.append({'role': 'user', 'content': user_question})
    else:
        if(len(file_name) == 1):
            if(user_question == ''):
                llm_chat.append({'role': 'user', 'content': UserUploadJSONNoQuestion.getPrompt(file_name[0]['name'])})
            else:
                llm_chat.append({'role': 'user', 'content': UserUploadJSONIrrelevantQuestion.getPrompt(file_name[0]['name'], user_question)})
        else:
            if(user_question == ''):
                llm_chat.append({'role': 'user', 'content': UserUploadMultipleJSONNoQuestion.getPrompt([f['name'] for f in file_name])})
            else:
                llm_chat.append({'role': 'user', 'content': UserUploadMultipleJSONIrrelevantQuestion.getPrompt([f['name'] for f in file_name], user_question)})
    print('JENG^')
    print('**')
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

def PassLLMThink(llm_model, user_question, db_chat = [], json_document = None, conv_id = None):
    think_list = []
    print('subemela')
    print(json_document)
    ### Chain 0: Recongise Upload ###
    if(json_document != None and user_question == ''):
        if(len(json_document) == 1):
            return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': JSONUploadNoQuestion.getPrompt(json_document[0]['name'])}], stream = True), 'think': think_list, 'end': 'success_unfinished'}
        else:
            return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': MultipleJSONUploadNoQuestion.getPrompt([doc['name'] for doc in json_document])}], stream = True), 'think': think_list, 'end': 'success_unfinished'}
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
    output_specific = False
    answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': HighLevelClassifier.getPrompt(user_question)}]).message.content) # Word-based search
    print('--Chain 2--')
    print(answer)
    try:
        answer = json.loads(answer)
        think_list.append({'chain': '2', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
        words = answer['words']
        if(len(words) == 0):
            # Check OUTPUT file only: Assignments, Dispatch, Duration
            answer = LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': HighLevelOutputJSONClassifier.getPrompt(user_question)}]).message.content)
            answer = json.loads(answer)
            think_list.append({'chain': '2_outputjson', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
            words = answer['words']

            if('dispatch' in words):
                search = 'dispatch'
            elif('duration' in words):
                search = 'duration'
            elif('assignment' in words):
                search = 'assignment'

            if(len(words) != 0):
                output_specific = True
                #return {'end': 'success_complete', 'think': think_list, 'search': search, 'retrieve_info': None, 'wanted_return': None, 'json_documents': json_document, 'taskprecedenceconstraints_pick': None, 'complex': None, 'complex_utils': {}}
            else:
                # Check for "plan"
                answer = LLMOutClean(chat(llm_model, messages=[{'role': 'user', 'content': HighLevelPlanClassifier.getPrompt(user_question)}]).message.content)
                answer = json.loads(answer)
                think_list.append({'chain': '2_plan', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
                words = answer['words']
                if 'plan' in words:
                    search = 'plan'
                else:
                    # NOT asking about Jobs, Tasks, etc.. So a general, non-json question
                    return {'response_msg': chat(llm_model, messages = CreateChatConv(db_chat, user_question, json_document, conv_id), stream = True), 'think': think_list, 'end': 'success_unfinished'}

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
                    print('2_task &&&')
                    print(answer)
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
    
        # Ouput JSON questions (or Multi File)
        complex = None
        if(search == 'jobs' or search == 'tasks' or search == 'tasksuitableresources'):
            answer = chat(llm_model, messages = [{'role': 'user', 'content': InputMultiOuputJSONClassifier.getPrompt(user_question)}]).message.content
            answer = json.loads(LLMOutClean(answer))
            think_list.append({'chain': '2_multiJSON', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
            print(answer)
            print('haduken--')
            words = ['duration' if w == 'production' else w for w in answer['words']]
            if(len(words) != 0):
                complex = words

        complex_utils = {}
        if(complex != None and 'duration' in complex):
            answer = chat(llm_model, messages = [{'role': 'user', 'content': InputMultiOutputJSONDurationLongestShortestClassifier.getPrompt(user_question)}]).message.content
            answer = json.loads(LLMOutClean(answer))
            think_list.append({'chain': '2_durationExtremum', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
            duration_extremum = answer['pick']
            if duration_extremum == 'None':
                duration_extremum = None
            complex_utils = {'duration_extremum': duration_extremum}

        if(complex != None and 'complete' in complex):
            answer = chat(llm_model, messages = [{'role': 'user', 'content': InputMultiOutputJSONCompleteDateExtractor.getPrompt(user_question)}]).message.content
            answer = json.loads(LLMOutClean(answer))
            think_list.append({'chain': '2_completeDateExtract', 'think': answer['think'] if 'think' in answer else 'Exception No Thinking Return from LLM'})
            date_str = answer['date']
            if(date_str != ''):
                complete_by = json.loads(LLMOutClean(chat(llm_model, messages = [{'role': 'user', 'content': StringToDateMonthForm.getPrompt(date_str)}]).message.content))
                think_list.append({'chain': '2_completeDateConvert', 'think': str(complete_by)})
                complex_utils['complete_by'] = complete_by
                try:
                    datetime.datetime(2001, complete_by['month'], complete_by['day'])
                except (ValueError, KeyError):
                    return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': InvalidCompleteDateResponse.getPrompt(user_question, date_str)}], stream = True), 'think': think_list, 'end': 'success_unfinished'}

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

    ### Chain 2 JobDuration: Check JobDuration QUestion has Both Input AND/OR Output ###
    if search == 'jobs' and complex is not None and 'duration' in complex:
        has_input = any('input' in doc['name'].lower() for doc in json_document)
        if not has_input:
            return {'response_msg': chat(llm_model, messages = [{'role': 'user', 'content': JobDurationNoInputFile.getPrompt(user_question)}], stream = True), 'think': think_list, 'end': 'success_unfinished'}
    ### Chain 2 End ###

    ### Chain 2 JobStartEnd: Check JobStartEnd Question has Fused Pair (Input AND Output) ###
    if search == 'jobs' and complex is not None and ('start' in complex or 'end' in complex):
        doc_names = BuildDocNames(json_document)
        has_fused_pair = any(len(group) >= 2 for group in doc_names)
        if not has_fused_pair:
            return {'response_msg': chat(llm_model, messages=[{'role': 'user', 'content': JobStartEndNoFusedPair.getPrompt(user_question)}], stream=True), 'think': think_list, 'end': 'success_unfinished'}
    ### Chain 2 End ###

    ### Chain 2 JobComplete: Check JobComplete Question has Fused Pair (Input AND Output) ###
    if search == 'jobs' and complex is not None and 'complete' in complex:
        doc_names = BuildDocNames(json_document)
        has_fused_pair = any(len(group) >= 2 for group in doc_names)
        if not has_fused_pair:
            return {'response_msg': chat(llm_model, messages=[{'role': 'user', 'content': JobCompleteNoFusedPair.getPrompt(user_question)}], stream=True), 'think': think_list, 'end': 'success_unfinished'}
    ### Chain 2 End ###

    ### Chain 2 Plan: Check Plan Question has at least 2 Output files ###
    if search == 'plan':
        output_count = sum(1 for doc in json_document if 'output' in doc['name'].lower() and 'input' not in doc['name'].lower())
        if output_count < 2:
            return {'response_msg': chat(llm_model, messages=[{'role': 'user', 'content': PlanComparisonNoOutputFiles.getPrompt(user_question)}], stream=True), 'think': think_list, 'end': 'success_unfinished'}
        return {'end': 'success_complete', 'think': think_list, 'search': search, 'retrieve_info': None, 'wanted_return': None, 'json_documents': json_document, 'taskprecedenceconstraints_pick': None, 'complex': None, 'complex_utils': {}}
    ### Chain 2 Plan End ###

    if output_specific == True:
        return {'end': 'success_complete', 'think': think_list, 'search': search, 'retrieve_info': None, 'wanted_return': None, 'json_documents': json_document, 'taskprecedenceconstraints_pick': None, 'complex': complex, 'complex_utils': complex_utils}


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
    print('&&&&&[]>')
    print(answer)
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
    skip_chain4 = (complex is not None and ('start' in complex or 'end' in complex or 'complete' in complex))

    if skip_chain4:
        wanted_return = None
    else:
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
    return {'end': 'success_complete', 'think': think_list, 'search': search, 'retrieve_info': retrieve_info, 'wanted_return': wanted_return, 'json_documents': json_document, 'taskprecedenceconstraints_pick': None if search != 'tasksprecedenceconstraints' else taskprecedenceconstraints_pick, 'complex': complex, 'complex_utils': complex_utils}

def BuildDocNames(json_documents):
    seen = set()
    unique_docs = []
    for doc in json_documents:
        if doc['name'] not in seen:
            seen.add(doc['name'])
            unique_docs.append(doc)

    input_groups = {}
    output_groups = {}
    for doc in unique_docs:
        name_lower = doc['name'].lower()
        match = re.search(r'(input|output)[a-z]*_(\d+)', name_lower)
        if match:
            io_type = match.group(1)
            x = match.group(2)
            if io_type == 'input':
                input_groups.setdefault(x, []).append(doc)
            else:
                output_groups.setdefault(x, []).append(doc)

    doc_names = []
    for x, inp_docs in input_groups.items():
        out_docs = output_groups.get(x, [])
        for inp in inp_docs:
            if out_docs:
                for out in out_docs:
                    doc_names.append([inp['name'], out['name']])
            else:
                doc_names.append([inp['name']])

    return doc_names

def LLMGetFinalQuery(conv_id, search, json_documents, retrieve_info, llm_model, wanted_return, complex = None, complex_utils = {}):
    if search == 'plan':
        return LLMGetFinalQueryPlan(conv_id, json_documents)

    if search == 'jobs' and complex is not None and 'duration' in complex:
        doc_names = BuildDocNames(json_documents)
        doc_by_name = {doc['name']: doc for doc in json_documents}
        return LLMGetFinalQueryJobDuration(conv_id, doc_names, doc_by_name, complex_utils)

    if search == 'jobs' and complex is not None and ('start' in complex or 'end' in complex):
        doc_names = BuildDocNames(json_documents)
        doc_by_name = {doc['name']: doc for doc in json_documents}
        return LLMGetFinalQueryJobStartEnd(conv_id, doc_names, doc_by_name, complex, retrieve_info)

    if search == 'jobs' and complex is not None and 'complete' in complex and 'complete_by' in complex_utils:
        doc_names = BuildDocNames(json_documents)
        doc_by_name = {doc['name']: doc for doc in json_documents}
        return LLMGetFinalQueryJobComplete(conv_id, doc_names, doc_by_name, complex_utils, retrieve_info)

    fetched_list = []
    for doc in json_documents:
        json_name = doc['name'].lower()

        has_input = 'input' in json_name
        has_output = 'output' in json_name

        if has_input and not has_output:
            if(complex != None and (complex_utils != {} or 'start' in complex or 'end' in complex or 'complete' in complex)):
                fetched_list.append(LLMGetFinalQueryInputMultiJSON(conv_id, search, doc, complex, complex_utils))
            else:
                fetched_list.append(LLMGetFinalQueryInputJSON(conv_id, search, doc, retrieve_info, llm_model, wanted_return))
        elif has_output and not has_input:
            if(complex != None):
                fetched_list.append(LLMGetFinalQueryOutputMultiJSON(conv_id, search, doc, complex, complex_utils, retrieve_info))
            else:
                fetched_list.append(LLMGetFinalQueryOutputJSON(conv_id, search, doc))
        else:
            fetched_list.append({"query": [], "json_data": [], "doc": doc})

    return fetched_list

def LLMGetFinalQueryOutputMultiJSON(conv_id, search, json_document, complex, complex_utils = {}, retrieve_info = None):
    ### Get JSON Data ###
    ''' Retrieves the JSON data '''
    with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(json_document['id']) + '.' + json_document['name'].split('.')[-1], encoding = 'utf-8') as file:
        json_data = file.read()
        json_data = json.loads(json_data)
    ### Get JSON Data End ###

    if(search == 'tasksuitableresources' and 'duration' in complex):
        query = [{'task': q['task']['id'], 'durationinmilliseconds': q['durationinmilliseconds'], 'idx': i + 1} for i, q in enumerate(json_data['assignments']['assignment'])]
        if(complex_utils.get('duration_extremum') == 'A' and len(query) > 0):
            query = [max(query, key = lambda x: x['durationinmilliseconds'])]
        elif(complex_utils.get('duration_extremum') == 'B' and len(query) > 0):
            query = [min(query, key = lambda x: x['durationinmilliseconds'])]

    elif(search == 'tasksuitableresources' and 'start' in complex and 'end' in complex):
        query = []
        for i, q in enumerate(json_data['assignments']['assignment']):
            start_dt = datetime.datetime(q['timeofdispatch']['year'], q['timeofdispatch']['month'], q['timeofdispatch']['day'], q['timeofdispatch']['hour'], q['timeofdispatch']['minutes'], q['timeofdispatch']['seconds'])
            end_dt = start_dt + datetime.timedelta(milliseconds=q['durationinmilliseconds'])
            query.append({
                'task': q['task']['id'],
                'dispatch_start': {'year': start_dt.year, 'month': start_dt.month, 'day': start_dt.day, 'hour': start_dt.hour, 'minute': start_dt.minute, 'second': start_dt.second},
                'dispatch_end': {'year': end_dt.year, 'month': end_dt.month, 'day': end_dt.day, 'hour': end_dt.hour, 'minute': end_dt.minute, 'second': end_dt.second},
                'idx': i + 1
            })
    elif(search == 'tasksuitableresources' and 'start' in complex):
        query = [{'task': q['task']['id'], 'dispatch_start': {'year': q['timeofdispatch']['year'], 'month': q['timeofdispatch']['month'], 'day': q['timeofdispatch']['day'], 'hour': q['timeofdispatch']['hour'], 'minute': q['timeofdispatch']['minutes'], 'second': q['timeofdispatch']['seconds']}, 'idx': i + 1} for i, q in enumerate(json_data['assignments']['assignment'])]
    elif(search == 'tasksuitableresources' and 'end' in complex):
        query = []
        for i, q in enumerate(json_data['assignments']['assignment']):
            start_dt = datetime.datetime(q['timeofdispatch']['year'], q['timeofdispatch']['month'], q['timeofdispatch']['day'], q['timeofdispatch']['hour'], q['timeofdispatch']['minutes'], q['timeofdispatch']['seconds'])
            end_dt = start_dt + datetime.timedelta(milliseconds=q['durationinmilliseconds'])
            query.append({
                'task': q['task']['id'],
                'dispatch_end': {'year': end_dt.year, 'month': end_dt.month, 'day': end_dt.day, 'hour': end_dt.hour, 'minute': end_dt.minute, 'second': end_dt.second},
                'idx': i + 1
            })

    elif(search == 'tasksuitableresources' and 'complete' in complex and 'complete_by' in complex_utils):
        query = []
        complete_by = complex_utils['complete_by']
        for i, q in enumerate(json_data['assignments']['assignment']):
            start_dt = datetime.datetime(q['timeofdispatch']['year'], q['timeofdispatch']['month'], q['timeofdispatch']['day'], q['timeofdispatch']['hour'], q['timeofdispatch']['minutes'], q['timeofdispatch']['seconds'])
            end_dt = start_dt + datetime.timedelta(milliseconds=q['durationinmilliseconds'])
            deadline = datetime.datetime(end_dt.year, complete_by['month'], complete_by['day'])
            if end_dt <= deadline:
                query.append({
                    'task': q['task']['id'],
                    'dispatch_end': {'year': end_dt.year, 'month': end_dt.month, 'day': end_dt.day, 'hour': end_dt.hour, 'minute': end_dt.minute, 'second': end_dt.second},
                    'idx': i + 1
                })

    else:
        query = []

    if ('start' in complex or 'end' in complex) and retrieve_info is not None and retrieve_info.get('attribute') == True:
        know = retrieve_info.get('know', {})
        if know.get('info') == 'task' and know.get('key') == 'id':
            target_id = IntToStrWithSlabInfornt(know['value'])
            query = [q for q in query if q['task'] == target_id]

    return {"query": query, "json_data": json_data, "doc": json_document}

def LLMGetFinalQueryPlan(conv_id, json_documents):
    fetched_list = []
    for doc in json_documents:
        json_name = doc['name'].lower()
        has_input = 'input' in json_name and 'output' not in json_name
        has_output = 'output' in json_name and 'input' not in json_name

        if has_input:
            fetched_list.append({"query": [], "json_data": [], "doc": doc})
        elif has_output:
            with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(doc['id']) + '.' + doc['name'].split('.')[-1], encoding='utf-8') as file:
                json_data = json.loads(file.read())

            assignments = json_data['assignments']['assignment']

            if len(assignments) == 0:
                fetched_list.append({"query": [], "json_data": json_data, "doc": doc})
                continue

            earliest_start = None
            latest_end = None

            for q in assignments:
                start_dt = datetime.datetime(q['timeofdispatch']['year'], q['timeofdispatch']['month'], q['timeofdispatch']['day'], q['timeofdispatch']['hour'], q['timeofdispatch']['minutes'], q['timeofdispatch']['seconds'])
                end_dt = start_dt + datetime.timedelta(milliseconds=q['durationinmilliseconds'])

                if earliest_start is None or start_dt < earliest_start:
                    earliest_start = start_dt
                if latest_end is None or end_dt > latest_end:
                    latest_end = end_dt

            duration_ms = int((latest_end - earliest_start).total_seconds() * 1000)

            query = [{
                'dispatch_start': {'year': earliest_start.year, 'month': earliest_start.month, 'day': earliest_start.day, 'hour': earliest_start.hour, 'minute': earliest_start.minute, 'second': earliest_start.second},
                'dispatch_end': {'year': latest_end.year, 'month': latest_end.month, 'day': latest_end.day, 'hour': latest_end.hour, 'minute': latest_end.minute, 'second': latest_end.second},
                'durationinmilliseconds': duration_ms,
            }]
            fetched_list.append({"query": query, "json_data": json_data, "doc": doc})
        else:
            fetched_list.append({"query": [], "json_data": [], "doc": doc})

    return fetched_list

def LLMGetFinalQueryOutputJSON(conv_id, search, json_document):
    ### Get JSON Data ###
    ''' Retrieves the JSON data '''
    with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(json_document['id']) + '.' + json_document['name'].split('.')[-1], encoding = 'utf-8') as file:
        json_data = file.read()
        json_data = json.loads(json_data)
    ### Get JSON Data End ###

    ### Query Form Based on Chain 2 ###
    ''' Classifies if user asks about: Assignments, Dispatch, Duration'''
    assignments = json_data['assignments']['assignment']
    if(search == 'assignment'):
        query = [(i + 1, q) for i, q in enumerate(assignments)]
    elif(search == 'tasks'):
        query = [(i + 1, q['task']) for i, q in enumerate(assignments)]
    elif(search == 'resources'):
        query = [(i + 1, q['resource']) for i, q in enumerate(assignments)]
    elif(search == 'dispatch'):
        query = [(i + 1, q['timeofdispatch']) for i, q in enumerate(assignments)]
    elif(search == 'duration'):
        query = [(i + 1, q['durationinmilliseconds']) for i, q in enumerate(assignments)]
    else:
        query = []
    ### End Chain 2 Query ###

    ### Query Clean Form ###
    if(search == 'assignment'):
        query = [{'task': q['task']['id'], 'resource': q['resource']['id'], 'dispatch': {'year': q['timeofdispatch']['year'], 'month': q['timeofdispatch']['month'], 'day': q['timeofdispatch']['day'], 'hour': q['timeofdispatch']['hour'], 'minute': q['timeofdispatch']['minutes'], 'second': q['timeofdispatch']['seconds']}, 'durationinmilliseconds': q['durationinmilliseconds'], 'idx': idx} for idx, q in query]
    elif(search == 'tasks'):
        query = [{'task': q['id'], 'idx': idx} for idx, q in query]
    elif(search == 'resources'):
        query = [{'resource': q['id'], 'idx': idx} for idx, q in query]
    elif(search == 'dispatch'):
        query = [{'dispatch': {'year': q['year'], 'month': q['month'], 'day': q['day'], 'hour': q['hour'], 'minute': q['minutes'], 'second': q['seconds']}, 'idx': idx} for idx, q in query]
    elif(search == 'duration'):
        query = [{'durationinmilliseconds': q, 'idx': idx} for idx, q in query]
    ### End Query Clean Form###

    return {"query": query, "json_data": json_data, "doc": json_document}

def LLMGetFinalQueryInputMultiJSON(conv_id, search, json_document, complex, complex_utils = {}):
    print('??//??')
    print(complex)
    print(complex_utils)
    print(type(complex_utils))
    ### Get JSON Data ###
    with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(json_document['id']) + '.' + json_document['name'].split('.')[-1], encoding = 'utf-8') as file:
        json_data = file.read()
        json_data = json.loads(json_data)
    ### Get JSON Data End ###

    if(search == 'tasksuitableresources' and 'duration' in complex):
        raw = json_data['tasksuitableresources']['tasksuitableresource']
        if(complex_utils.get('duration_extremum') == 'A' and len(raw) > 0):
            pick = max(raw, key = lambda x: x['operationtimeperbatchinseconds'])
        elif(complex_utils.get('duration_extremum') == 'B' and len(raw) > 0):
            pick = min(raw, key = lambda x: x['operationtimeperbatchinseconds'])
        else:
            pick = None

        if pick:
            res_id = pick['resourcereference']['refid']
            res_name = [r['name'] for r in json_data['resources']['resource'] if r['id'] == res_id][0]
            task_id = pick['taskreference']['refid']
            task_name = [t['name'] for t in json_data['tasks']['task'] if t['id'] == task_id][0]
            query = [{'resource': {'id': res_id, 'name': res_name}, 'tasks': [{'id': task_id, 'operation_time': pick['operationtimeperbatchinseconds'], 'name': task_name}]}]
        elif len(raw) > 0:
            groups = {}
            for entry in raw:
                res_id = entry['resourcereference']['refid']
                if res_id not in groups:
                    res_name = [r['name'] for r in json_data['resources']['resource'] if r['id'] == res_id][0]
                    groups[res_id] = {'resource': {'id': res_id, 'name': res_name}, 'tasks': []}
                task_id = entry['taskreference']['refid']
                task_name = [t['name'] for t in json_data['tasks']['task'] if t['id'] == task_id][0]
                groups[res_id]['tasks'].append({'id': task_id, 'operation_time': entry['operationtimeperbatchinseconds'], 'name': task_name})
            query = list(groups.values())
        else:
            query = []
    else:
        query = []

    return {"query": query, "json_data": json_data, "doc": json_document}

def LLMGetFinalQueryJobDuration(conv_id, doc_names, doc_by_name, complex_utils):
    results = []

    for group in doc_names:
        input_name = group[0]
        input_doc = doc_by_name[input_name]

        with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(input_doc['id']) + '.' + input_doc['name'].split('.')[-1], encoding='utf-8') as file:
            input_data = json.loads(file.read())

        jobs = input_data['jobs']['job']
        tsr = input_data['tasksuitableresources']['tasksuitableresource']
        group_query = []

        if len(group) == 1:
            for job in jobs:
                task_refs = [t['refid'] for t in job['jobtaskreference']]
                total_duration = 0
                for task_ref in task_refs:
                    for entry in tsr:
                        if entry['taskreference']['refid'] == task_ref:
                            total_duration += entry['operationtimeperbatchinseconds']
                            break
                group_query.append({
                    'name': job['name'],
                    'id': job['id'],
                    'task': task_refs,
                    'duration': total_duration
                })
        else:
            output_name = group[1]
            output_doc = doc_by_name[output_name]

            with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(output_doc['id']) + '.' + output_doc['name'].split('.')[-1], encoding='utf-8') as file:
                output_data = json.loads(file.read())

            assignments = output_data['assignments']['assignment']

            for job in jobs:
                task_refs = [t['refid'] for t in job['jobtaskreference']]
                total_duration = 0
                assignment_indices = []
                all_found = True

                for ref in task_refs:
                    ref_stripped = ref.lstrip('_')
                    found = False
                    for i, a in enumerate(assignments):
                        if a['task']['id'].lstrip('_') == ref_stripped:
                            total_duration += a['durationinmilliseconds'] / 1000
                            assignment_indices.append(i + 1)
                            found = True
                            break
                    if not found:
                        all_found = False
                        break

                if all_found:
                    group_query.append({
                        'name': job['name'],
                        'id': job['id'],
                        'task': task_refs,
                        'duration': total_duration,
                        'assignments': assignment_indices
                    })
                else:
                    group_query.append({
                        'name': job['name'],
                        'id': job['id'],
                        'task': [],
                        'duration': None,
                        'assignments': []
                    })

        if complex_utils.get('duration_extremum') == 'A':
            valid = [q for q in group_query if q['duration'] is not None]
            if valid:
                group_query = [max(valid, key=lambda x: x['duration'])]
        elif complex_utils.get('duration_extremum') == 'B':
            valid = [q for q in group_query if q['duration'] is not None]
            if valid:
                group_query = [min(valid, key=lambda x: x['duration'])]

        results.append({"query": group_query, "doc_fuse": group, "json_data": []})

    return results

def LLMGetFinalQueryJobStartEnd(conv_id, doc_names, doc_by_name, complex, retrieve_info):
    results = []

    for group in doc_names:
        if len(group) < 2:
            continue

        input_name = group[0]
        output_name = group[1]
        input_doc = doc_by_name[input_name]
        output_doc = doc_by_name[output_name]

        with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(input_doc['id']) + '.' + input_doc['name'].split('.')[-1], encoding='utf-8') as file:
            input_data = json.loads(file.read())

        with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(output_doc['id']) + '.' + output_doc['name'].split('.')[-1], encoding='utf-8') as file:
            output_data = json.loads(file.read())

        jobs = input_data['jobs']['job']
        assignments = output_data['assignments']['assignment']
        group_query = []

        for job in jobs:
            task_refs = [t['refid'] for t in job['jobtaskreference']]
            matching_assignments = []
            assignment_indices = []
            all_found = True

            for ref in task_refs:
                ref_stripped = ref.lstrip('_')
                found = False
                for i, a in enumerate(assignments):
                    if a['task']['id'].lstrip('_') == ref_stripped:
                        matching_assignments.append(a)
                        assignment_indices.append(i + 1)
                        found = True
                        break
                if not found:
                    all_found = False
                    break

            if not all_found:
                group_query.append({
                    'name': job['name'],
                    'id': job['id'],
                    'task': [],
                    'assignments': []
                })
                continue

            job_entry = {
                'name': job['name'],
                'id': job['id'],
                'task': task_refs,
                'assignments': assignment_indices
            }

            if 'start' in complex:
                earliest = None
                for a in matching_assignments:
                    tod = a['timeofdispatch']
                    dt = datetime.datetime(tod['year'], tod['month'], tod['day'], tod['hour'], tod['minutes'], tod['seconds'])
                    if earliest is None or dt < earliest:
                        earliest = dt
                job_entry['dispatch_start'] = {
                    'year': earliest.year, 'month': earliest.month, 'day': earliest.day,
                    'hour': earliest.hour, 'minute': earliest.minute, 'second': earliest.second
                }

            if 'end' in complex:
                latest = None
                for a in matching_assignments:
                    tod = a['timeofdispatch']
                    start_dt = datetime.datetime(tod['year'], tod['month'], tod['day'], tod['hour'], tod['minutes'], tod['seconds'])
                    end_dt = start_dt + datetime.timedelta(milliseconds=a['durationinmilliseconds'])
                    if latest is None or end_dt > latest:
                        latest = end_dt
                job_entry['dispatch_end'] = {
                    'year': latest.year, 'month': latest.month, 'day': latest.day,
                    'hour': latest.hour, 'minute': latest.minute, 'second': latest.second
                }

            group_query.append(job_entry)

        if retrieve_info is not None and retrieve_info.get('attribute') == True:
            if retrieve_info.get('key') == 'id':
                group_query = [q for q in group_query if q['id'] == IntToStrWithSlabInfornt(retrieve_info['value'])]
            elif retrieve_info.get('key') == 'name':
                group_query = [q for q in group_query if q['name'].upper() == retrieve_info['value'].upper()]

        results.append({"query": group_query, "doc_fuse": group, "json_data": []})

    return results

def LLMGetFinalQueryJobComplete(conv_id, doc_names, doc_by_name, complex_utils, retrieve_info):
    results = []
    complete_by = complex_utils['complete_by']

    for group in doc_names:
        if len(group) < 2:
            continue

        input_name = group[0]
        output_name = group[1]
        input_doc = doc_by_name[input_name]
        output_doc = doc_by_name[output_name]

        with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(input_doc['id']) + '.' + input_doc['name'].split('.')[-1], encoding='utf-8') as file:
            input_data = json.loads(file.read())

        with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(output_doc['id']) + '.' + output_doc['name'].split('.')[-1], encoding='utf-8') as file:
            output_data = json.loads(file.read())

        jobs = input_data['jobs']['job']
        assignments = output_data['assignments']['assignment']
        group_query = []

        for job in jobs:
            task_refs = [t['refid'] for t in job['jobtaskreference']]
            matching_assignments = []
            assignment_indices = []
            all_found = True

            for ref in task_refs:
                ref_stripped = ref.lstrip('_')
                found = False
                for i, a in enumerate(assignments):
                    if a['task']['id'].lstrip('_') == ref_stripped:
                        matching_assignments.append(a)
                        assignment_indices.append(i + 1)
                        found = True
                        break
                if not found:
                    all_found = False
                    break

            if not all_found:
                continue

            latest = None
            for a in matching_assignments:
                tod = a['timeofdispatch']
                start_dt = datetime.datetime(tod['year'], tod['month'], tod['day'], tod['hour'], tod['minutes'], tod['seconds'])
                end_dt = start_dt + datetime.timedelta(milliseconds=a['durationinmilliseconds'])
                if latest is None or end_dt > latest:
                    latest = end_dt

            deadline = datetime.datetime(latest.year, complete_by['month'], complete_by['day'])
            if latest <= deadline:
                group_query.append({
                    'name': job['name'],
                    'id': job['id'],
                    'task': task_refs,
                    'assignments': assignment_indices,
                    'dispatch_end': {
                        'year': latest.year, 'month': latest.month, 'day': latest.day,
                        'hour': latest.hour, 'minute': latest.minute, 'second': latest.second
                    }
                })

        if retrieve_info is not None and retrieve_info.get('attribute') == True:
            if retrieve_info.get('key') == 'id':
                group_query = [q for q in group_query if q['id'] == IntToStrWithSlabInfornt(retrieve_info['value'])]
            elif retrieve_info.get('key') == 'name':
                group_query = [q for q in group_query if q['name'].upper() == retrieve_info['value'].upper()]

        results.append({"query": group_query, "doc_fuse": group, "json_data": []})

    return results

def LLMGetFinalQueryInputJSON(conv_id, search, json_document, retrieve_info, llm_model, wanted_return):

    ### Get JSON Data ###
    ''' Retrieves the JSON data '''
    with open(chatdocumentpath + '/' + str(conv_id) + '_' + str(json_document['id']) + '.' + json_document['name'].split('.')[-1], encoding = 'utf-8') as file:
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
    else:
        return {"query": [], "json_data": json_data, "doc": json_document}
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
        print('7779')
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
            
            elif(search == 'tasksuitableresources' and retrieve_info != None and retrieve_info['attribute'] != False):
                print(retrieve_info)
                print('LLOOPP')
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
    print(query)
    return {"query": query, "json_data": json_data, "doc": json_document}


# Handles Only Input JSON.
def LLMGetFinalQuery_Old(conv_id, search, json_documents, retrieve_info, llm_model, wanted_return):

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
    if search == 'plan':
        return PassLLMFinalAnswerPlan(search, user_question, query, json_document, llm_model, think_list)
    if(len(json_document) == 1):
        return PassLLMFinalAnswerSingleDocument(search, user_question, query, retrieve_info, json_data, llm_model, think_list, taskprecedenceconstraints_pick, json_document[0]['name'])
    else:
        return PassLLMFinalAnswerMultipleDocument(search, user_question, query, llm_model, think_list)

def PassLLMFinalAnswerMultipleDocument(search, user_question, query, llm_model, think_list):
    return [chat(llm_model, messages = [{'role': 'user', 'content': OutputListResultsMultipleDocuments.getPrompt(user_question)}], stream = True), think_list, query, search]

def PassLLMFinalAnswerPlan(search, user_question, query, json_documents, llm_model, think_list):
    best_duration = None
    best_doc_names = []

    for i, doc in enumerate(json_documents):
        doc_name = doc['name'].lower()
        if 'output' in doc_name and 'input' not in doc_name:
            if len(query[i]) > 0 and 'durationinmilliseconds' in query[i][0]:
                dur = query[i][0]['durationinmilliseconds']
                if best_duration is None or dur < best_duration:
                    best_duration = dur
                    best_doc_names = [doc['name']]
                elif dur == best_duration:
                    best_doc_names.append(doc['name'])

    if len(best_doc_names) == 0:
        return [chat(llm_model, messages=[{'role': 'user', 'content': ExceptionHandler.getPrompt(user_question)}], stream=True), think_list, query, search]

    if len(best_doc_names) == 1:
        return [chat(llm_model, messages=[{'role': 'user', 'content': OutputListResultsPlanComparisonSingle.getPrompt(user_question, best_doc_names[0])}], stream=True), think_list, query, search]
    else:
        return [chat(llm_model, messages=[{'role': 'user', 'content': OutputListResultsPlanComparisonMultiple.getPrompt(user_question, best_doc_names)}], stream=True), think_list, query, search]

def PassLLMFinalAnswerSingleDocument(search, user_question, query, retrieve_info, json_data, llm_model, think_list, taskprecedenceconstraints_pick, doc_name):
    print('Single___')
    print(taskprecedenceconstraints_pick)
    print(retrieve_info)
    print(query)
    print('ppppppppppppp')
    ### Chain 5: Final Answer ###
    doc_name = doc_name.lower()
    if( ('input' in doc_name and 'output' in doc_name) or ('input' not in doc_name and 'output' not in doc_name)):
        return [chat(llm_model, messages = [{'role': 'user', 'content': OutputInvalidName.getPrompt(user_question)}], stream = True), think_list, query, search]
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
    llm_res = PassLLMThink(llm_model, user_question, db_chat, json_document, conv_id)
    print(llm_res)
    print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
    '''
    Example: When did job 95 complete?
    jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
    {'end': 'success_complete', 'think': [{'chain': '1', 'think': "The question is asking for a specific event or completion time related to job 95. It includes context and meaningful words, so it's not gibberish."}, {'chain': '2', 'think': "The words 'job' and its variations were identified through character-based pattern matching. The string 'job' was found in the input question without any corrections or assumptions made."}, {'chain': '2_multiJSON', 'think': "The word 'complete' is present in the input due to a strict character match."}, {'chain': '3', 'think': 'The user is asking about a specific job with id 95 and I assume they want to know its completion date, which would be the duedate.'}, {'chain': '4', 'think': "The user is asking about a specific job (job 95) and the completion date is related to the duedate attribute of a job. So, I'm assuming they want the entire job object returned."}], 'search': 'jobs', 'retrieve_info': {'attribute': True, 'key': 'id', 'value': 95, 'think': 'The user is asking about a specific job with id 95 and I assume they want to know its completion date, which would be the duedate.'}, 'wanted_return': {'attribute': False, 'think': "The user is asking about a specific job (job 95) and the completion date is related to the duedate attribute of a job. So, I'm assuming they want the entire job object returned."}, 'json_documents': [{'id': 319120913054060545, 'name': 'InputJSON_1.json'}, {'id': 319120913054060546, 'name': 'OutputJSON_1.json'}], 'taskprecedenceconstraints_pick': None, 'multijson': ['complete']}
    
    '''
    if(llm_res['end'] != 'success_complete'):
        return [llm_res['response_msg'], llm_res['think'], None, None if 'search' not in llm_res else llm_res['search'], None]
    else:
        fetched_results = LLMGetFinalQuery(conv_id, llm_res['search'], llm_res['json_documents'], llm_res['retrieve_info'], llm_model, llm_res['wanted_return'], llm_res['complex'], llm_res['complex_utils'])
        doc_fuse = [fr["doc_fuse"] for fr in fetched_results] if any("doc_fuse" in fr for fr in fetched_results) else None
    print('ooii')
    #print(fetched_results)
    result = PassLLMFinalAnswer(llm_res['json_documents'], llm_res['search'], user_question, [fr["query"] for fr in fetched_results], llm_res['retrieve_info'], [fr["json_data"] for fr in fetched_results], llm_model, llm_res['think'], llm_res['taskprecedenceconstraints_pick'])
    result.append(doc_fuse)
    return result

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
# Deprecated DO NOT USE/READ
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
                    #return chat(llm_model, messages = [{'role': 'user', 'content': TitlteJSONUploadIrrelevantQuestion.getPrompt(user_question, file_name)}]).message.content
                    return chat(llm_model, messages = [{'role': 'user', 'content': TitleOnlyQuestionNoJSON.getPrompt(user_question)}]).message.content
                else:
                    return chat(llm_model, messages = [{'role': 'user', 'content': TitleJSONUploadRelevantQuestion.getPrompt(user_question)}]).message.content
            except:
                return None
    else:
        return chat(llm_model, messages = [{'role': 'user', 'content': TitleOnlyQuestionNoJSON.getPrompt(user_question)}]).message.content
    ### Chain 2 End ###