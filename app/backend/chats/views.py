from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponseBadRequest, HttpResponse
from oauth import ValidateAndCreateJWT, ReturnHttpInvalidJWT, CreateResponseNewAccess, CreateStreamingResponseNewAccess
from backend.mongo_db_connection import mongo_db
import json
from snowflake_id_gen import GenerateSnowflake
import datetime
from .LLMpipeline import PassLLMThink, CreateConversationTitleThink, PassLLMThinkCompletePipeline
from LLM_prompts.NoAgent import NoAgentJSONUpload
from openai import OpenAI

###
# For multiplrocessing to work (i.e. to spawn a process) you must run these two lines of code before importing any models.
# When spawning a Process errors are raises that are due to importing models.
# You must run these 2 lines before impoting a model, in the file that spawns a new Process
import django
django.setup()
###
from loginregister.models import User

from loginregister.views import PasswordCompare
import math
import base64
import os
from ollama import chat
from backend.redis_connection import redis_client
from transformers import AutoTokenizer

import multiprocessing

# Create your views here.

chats = mongo_db['Chats']
chatdocumentpath = os.environ.get('CHAT_DOCUMENT_PATH')
development = os.environ.get('development')
llm_model = os.environ.get('LLM_MODEL')


@api_view(['GET'])
def GetChats(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    ret = list(chats.aggregate( [{"$match": {"user_id": valjwt[3]}},
                                     {"$project": {"_id": 1, "name": 1, "date_created": 1}},
                                     {"$sort": {"date_created": 1}}]) )
    for i in range(0, len(ret)):
        ret[i]["date_created"] = ret[i]["date_created"].timestamp()
        ret[i]["_id"] = str(ret[i]["_id"])
    
    return CreateResponseNewAccess(valjwt[1], ret, 200)

@api_view(['POST'])
def RenameChat(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('id' not in data or 'v' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data['v']) < 5):
        return HttpResponse(json.dumps('Conversation name must be more than 5 characters'), status = 400)
    if(len(data['v']) > 50):
        return HttpResponse(json.dumps('Conversation name must be less than 50 characters'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Conversation ID'), status = 400)

    chat_ret = chats.update_one({"_id": int(data["id"]), "user_id": valjwt[3]},
                                        {"$set": {"name": data["v"]}})
    if(chat_ret.modified_count == 1):
        return CreateResponseNewAccess(valjwt[1], 'Chat successfully renamed', 200)
    else:
        return HttpResponse(json.dumps('Conversation ID does not belong to User'), status = 400)
    
@api_view(['DELETE'])
def DeleteChat(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('id' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Conversation ID'), status = 400)

    path_del = list(chats.find({"_id": int(data["id"]), "chat.d": {"$exists": "true"}}, {"paths": "$chat.d.path"}))
    
    chat_del = chats.delete_one({"_id": int(data["id"]), "user_id": valjwt[3]})
    if(chat_del.deleted_count == 1):
        filepath = chatdocumentpath if development != 'true' else 'D:/Downloads/diplomat/actual_work/app/frontend/components/chatdocuments'
        for i in path_del:
            print(i)
            print('**DEL**')
            for x in i['paths']:
                print(x)
                print('--del--')
                if(os.path.exists(filepath + '/' + x)):
                    os.remove(filepath + '/' + x)
        return CreateResponseNewAccess(valjwt[1], 'Chat successfully deleted', 200)
    else:
        return HttpResponse(json.dumps('Conversation ID does not belong to User'), status = 400)

@api_view(['POST'])
def CreateChat(request):
    content_type = request.headers.get('content-type').split(';')[0]
    print(content_type)
    print('^^^^^^^^^^^^^^^^^^^^')
    if(content_type == 'text/plain'):
        return CreateChatQuestion(request)
    elif(content_type == 'multipart/form-data'):
        return CreateChatDocument(request)
    else:
        return HttpResponse(json.dumps('Invalid Question Headers'), status = 400)

def CreateChatQuestion(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data or 'm' not in data or (data['m'] != 1 and data['m'] != 2 and data['m'] != 3) or (data['m'] == 3 and ('k' not in data))):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data['q']) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)

    chat_id = GenerateSnowflake()
    curr_time = datetime.datetime.now(datetime.timezone.utc)

    redis_client.set("cg_" + str(chat_id), json.dumps({"q": data["q"]}))
    if(data['m'] == 3):
        print(data['k'])
        print('&&&==')
        p = multiprocessing.Process(target = AnswerQuestionCloud, args=[[], data["q"], str(chat_id), None, data['k']])
    elif(data['m'] == 2):
        p = multiprocessing.Process(target = AnswerQuestionLLM, args=[[], data["q"], str(chat_id)])
        #t = multiprocessing.Process(target = CreateChatTitle, args = [str(chat_id), data["q"]])
    else:
        p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[[], data["q"], str(chat_id)])
        #t = multiprocessing.Process(target = CreateChatTitleThink, args = [str(chat_id), data["q"]])
    t = multiprocessing.Process(target = CreateChatTitleThink, args = [str(chat_id), data["q"]])

    p.start()
    chats.insert_one({"_id": chat_id,
                        "name": "New Conversation",
                        "date_created": curr_time,
                        "user_id": valjwt[3],
                        "model_id": data['m'],
                        "chat": []
                        })
    t.start()
    
    return CreateResponseNewAccess(valjwt[1], {"_id": str(chat_id), "name": "New Conversation", "date_created": curr_time.timestamp()}, 200)

def CreateChatDocument(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)

    #request_dict = request.data.dict()
    print(request.data.dict())
    print('***')
    request_dict = request.data.dict()
    request_dict['data'] = json.loads(request_dict['data'])
    request_dict['document'] = json.loads(request_dict['document'])
    print(request_dict)
    #if('data' not in request_dict or 'document' not in request_dict or 'q' not in request_dict['data'] or 'data' not in request_dict['document'] or 'name' not in request_dict['document'] or 'm' not in request_dict['data'] or (request_dict['data']['m'] != 1 and request_dict['data']['m'] != 2 and request_dict['data']['m'] != 3)):
    if('data' not in request_dict or 'document' not in request_dict or 'q' not in request_dict['data'] or 'm' not in request_dict['data'] or (request_dict['data']['m'] != 1 and request_dict['data']['m'] != 2 and request_dict['data']['m'] != 3) or (request_dict['data']['m'] == 3 and 'k' not in request_dict['data']) or (not all('data' in doc and 'name' in doc for doc in request_dict['document']))):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    print('popopo')
    data = request_dict['data']
    file = request_dict['document']

    if(any(len(f['data']) < 30 or f['data'][:29] != 'data:application/json;base64,' or f['name'][-5:] != '.json' for f in file)):
        return HttpResponse(json.dumps('Invalid XML file'), status = 400)

    chat_id = GenerateSnowflake()
    ############ <____________________________HERE !!!!!!!!!!!!!!!!!!!
    file_write = [base64.b64decode(f['data'][29:]) for f in file]
    file_id = GenerateSnowflake()

    document_info = [{"id": file_id + incr, "name": f['name'], "size": str(round(len(f_w)/1024, 1))} for incr, (f, f_w) in enumerate(zip(file, file_write))]
    redis_client.set("cg_" + str(chat_id), json.dumps({"u": [{"id": str(d["id"]), "name": d["name"], "size": d["size"]} for d in document_info], "q": data["q"]}))

    print(file_write)
    print('LLLLLLLLLLLLLLLLLLLLLLLLLLL')

    WriteDocument(file_write, document_info, str(chat_id))

    curr_time = datetime.datetime.now(datetime.timezone.utc)

    if(data['m'] == 3):
        p = multiprocessing.Process(target = AnswerQuestionCloud, args=[[], data["q"], str(chat_id), document_info, [f.decode() for f in file_write], request_dict['data']['k']])
    elif(data['m'] == 2):
        ## <----------- NEED TO CHECK THESE 2 -----------
        p = multiprocessing.Process(target = AnswerQuestionLLM, args=[[], data["q"], str(chat_id), document_info, [f.decode() for f in file_write]])
        #t = multiprocessing.Process(target = CreateChatTitle, args = [str(chat_id), data["q"], document_info["data"], document_info["name"]])
    else:
        p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[[], data["q"], str(chat_id), document_info])
        #t = multiprocessing.Process(target = CreateChatTitleThink, args = [str(chat_id), data["q"], [d["name"] for d in document_info]])
    t = multiprocessing.Process(target = CreateChatTitleThink, args = [str(chat_id), data["q"], [d["name"] for d in document_info]])

    p.start()
    chats.insert_one({"_id": chat_id,
                      "name": "New Conversation",
                      "date_created": curr_time,
                      "user_id": valjwt[3],
                      "model_id": data['m'],
                      "chat": []})
    t.start()

    return CreateResponseNewAccess(valjwt[1], {"_id": str(chat_id), "name": "New Conversation", "date_created": curr_time.timestamp()}, 200)

@api_view(['GET'])
def GetConversation(request, conv_id):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    chat_ret = chats.find_one({"_id": conv_id, "user_id": valjwt[3]}, {"_id": 0, "chat": 1, "model_id": 1})
    if(chat_ret == {}):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    else:
        print('MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')
        print(chat_ret)

        for chat in chat_ret['chat']:
            chat['t'] = chat['t'].timestamp()
            if 'd' in chat:
                for d in chat['d']:
                    d['id'] = str(d['id'])

        chat_ret = {'c': chat_ret['chat'], 'm': chat_ret['model_id']}

        gen_chat = redis_client.get("cg_" + str(conv_id))
        if(gen_chat != None):
            chat_ret['g'] = json.loads(gen_chat) # g -> generation
        return CreateResponseNewAccess(valjwt[1], chat_ret, 200)

@api_view(['POST'])
def AskQuestion(request):
    content_type = request.headers.get('content-type').split(';')[0]
    if(content_type == 'text/plain'):
        return AnswerQuestion(request)
    elif(content_type == 'multipart/form-data'):
        return AnswerQuestionWithDocument(request)
    else:
        return HttpResponse(json.dumps('Invalid Question Headers'), status = 400)

def GetLLMAnswerStream(chat_id, block_time = 110000, with_title = False):
    if(redis_client.exists("cg_" + chat_id) == True):
        stream_id = "cs_" + chat_id
        last_id  = '0-0'
        title_generated = False
        done_generated = False
        yield json.dumps({'v': ''}) + "\n" # Must have this so that COOKIES are instanly returned to user

        # t -> title, d -> done, v -> value, u -> uploaded document, i -> info (q -> query, s -> search), e -> error
        while True:
            x = redis_client.xread(streams = {stream_id: last_id }, count = None, block = block_time)

            if(len(x) == 0):
                yield json.dumps({'e': 'Timed Out'}) + "\n"
                return
            
            for stream_key, messages in x:
                for message_id, message_data in messages:
                    parsed_vals = {}
                    last_id = message_id
                    
                    (key, value), = message_data.items()
                    
                    try:
                        parsed_vals[key] = json.loads(value) # If value if JSON string
                    except:
                        parsed_vals[key] = value # If value is string example: 'Hi'

                    if 'd' in parsed_vals:
                        done_generated = True
                    elif 't' in parsed_vals:
                        title_generated = True
                        yield json.dumps({'t': parsed_vals['t']}) + "\n"
                    elif 'v' in parsed_vals:
                        yield json.dumps({'v': parsed_vals['v']}) + "\n"
                    elif 'i' in parsed_vals:
                        yield json.dumps({'i': parsed_vals['i']}) + "\n"
                    elif 'u' in parsed_vals:
                        yield json.dumps({'u': parsed_vals['u']}) + "\n"

                    if done_generated and (not with_title or title_generated):
                        return

def AnswerQuestion(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data or 'id' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data["q"].replace('\n', '')) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    
    if(redis_client.exists("cg_" + data["id"])):
        return HttpResponse(json.dumps('Cannot ask question. An answer for a previous question is being generated'), status = 409)

    chat_ret = chats.find_one({"_id": int(data["id"]), "user_id": valjwt[3]}, {"_id": 0, "chat.q": 1, "chat.a": 1, "chat.d": 1, "model_id": 1})

    if(chat_ret == {}):
        return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
    else:
        redis_client.set("cg_" + data["id"], json.dumps({"q": data["q"]})) # cg -> chat generation
        if(chat_ret['model_id'] == 2 or chat_ret['model_id'] == 3):
            p = multiprocessing.Process(target = AnswerQuestionLLM, args=[chat_ret['chat'], data["q"], data["id"]])
        else:
            p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[chat_ret['chat'], data["q"], data["id"]])
        p.start()
        return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [data["id"]], 200)

def AnswerQuestionLLM(db_chat, user_question, chat_id, document_dict = None, document_data = None):
    llm_chat = []
    total_answer = ''

    print(document_data)
    print('???????????????????????')

    for conv in db_chat:
        if 'd' in conv:
            data_temp = []
            for doc in conv['d']:
                with open(chatdocumentpath + '/' + chat_id + '_' + str(doc['id']) + '.' + doc['name'].split('.')[-1], encoding = 'utf-8') as file:
                    file_data = file.read()
                    data_temp.append(file_data)
            llm_chat += [{'role': 'user', 'content': NoAgentJSONUpload.getPrompt(conv['q'] if 'q' in conv else '', [{'name': d['name'], 'data': data} for d, data in  zip(conv['d'], data_temp)])}, {'role': 'assistant', 'content': conv['a']}] 

        else:
            llm_chat += [{'role': 'user', 'content': conv['q']}, {'role': 'assistant', 'content': conv['a']}]
    
    if(document_dict == None):
        llm_chat.append({'role': 'user', 'content': user_question})
    else:
        llm_chat.append({'role': 'user', 'content': NoAgentJSONUpload.getPrompt(user_question, [{'name': d['name'], 'data': data} for d, data in  zip(document_dict, document_data)])})

    print(llm_chat)
    print('>!<')

    try:
        llm_answer = chat(llm_model, messages = llm_chat, stream = True)
    except:
        redis_client.delete("cg_" + chat_id)
        return

    for chunk in llm_answer:
        
        if(chunk.done == True):
            redis_client.delete("cg_" + chat_id)
            redis_client.xadd("cs_" + chat_id, {"d": 1}) # d -> done # cs_ -> chat stream
            redis_client.expire("cs_" + chat_id, 3)
            if(document_dict == None):
                lololo = chats.update_one({"_id": int(chat_id)},
                                            {"$push": {"chat": {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer}}})
            else:
                push_val = {"t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer, "d": document_dict}
                if(user_question != ''):
                    push_val['q'] = user_question
                chats.update_one({"_id": int(chat_id)},
                                {"$push": {"chat": push_val}})
            return

        total_answer += chunk.message.content
        redis_client.xadd("cs_" + chat_id, {"v": chunk.message.content})

@api_view(['GET'])
def ResumeAnswerStream(request, conv_id):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [str(conv_id), 110000, True if request.GET.get('t') == '' else False], 200)

def AnswerQuestionWithDocument_OLD(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    request_dict = request.data.dict()
    if('data' not in request_dict or 'document' not in request_dict or 'q' not in request_dict['data'] or 'id' not in request_dict['data'] or 'data' not in request_dict['document'] or 'name' not in request_dict['document']):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    data = json.loads(request_dict['data'])
    file = json.loads(request_dict['document'])
    print('*********')
    print(data)
    print(file)
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    if(len(file['data']) < 30 or file['data'][:29] != 'data:application/json;base64,' or file['name'][-5:] != '.json'):
        return HttpResponse(json.dumps('Invalid XML file'), status = 400)
    
    if(redis_client.exists("cg_" + data["id"])):
        return HttpResponse(json.dumps('Cannot ask question. An answer for a previous question is being generated'), status = 409)
    
    chat_ret = chats.find_one({"_id": int(data["id"]), "user_id": valjwt[3]}, {"_id": 0, "chat.q": 1, "chat.a": 1, "chat.d": 1, "model_id": 1})

    if(chat_ret == {}):
        return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
    else:
        file_write = base64.b64decode(file['data'][29:])
        file_id = GenerateSnowflake()

        document_info = {"id": file_id, "name": file['name'], "size": str(round(len(file_write)/1024, 1)), "data": file_write.decode('utf-8')}
        redis_client.set("cg_" + data["id"], json.dumps({"u": {"id": str(document_info["id"]), "name": document_info["name"], "size": document_info["size"]}, "q": data["q"]}))

        WriteDocument(file_write, {"id": str(document_info['id']), "name": document_info['name'], "size": document_info['size']} , data['id'])

        if(chat_ret['model_id'] == 2 or chat_ret['model_id'] == 3):
            p = multiprocessing.Process(target = AnswerQuestionLLM, args=[chat_ret['chat'], data["q"], data["id"], document_info])
        else:
            document_info = {"id": document_info["id"], "name": document_info["name"], "size": document_info["size"]}
            p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[chat_ret['chat'], data["q"], data["id"], document_info])

        p.start()

        return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [data["id"]], 200)


def AnswerQuestionWithDocument(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    request_dict = request.data.dict()
    if('data' not in request_dict or 'document' not in request_dict or 'q' not in request_dict['data'] or 'id' not in request_dict['data']):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    data = json.loads(request_dict['data'])
    file = json.loads(request_dict['document'])
    print('*********')
    print(data)
    print(file)
    ###<______HERE !!!
    if(data['id'].isdigit() == False or type(data['q']) != str or type(file) != list):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    for f in file:
        if('name' not in f or 'data' not in f or type(f['name']) != str or type(f['data']) != str or len(f['data']) < 30 or f['data'][:29] != 'data:application/json;base64,' or f['name'][-5:] != '.json'):
            return HttpResponse(json.dumps('Invalid XML file'), status = 400)
    
    if(redis_client.exists("cg_" + data["id"])):
        return HttpResponse(json.dumps('Cannot ask question. An answer for a previous question is being generated'), status = 409)
    
    chat_ret = chats.find_one({"_id": int(data["id"]), "user_id": valjwt[3]}, {"_id": 0, "chat.q": 1, "chat.a": 1, "chat.d": 1, "model_id": 1})

    if(chat_ret == {}):
        return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
    else:
        file_write = [base64.b64decode(f['data'][29:]) for f in file]
        file_id = GenerateSnowflake()

        document_info = [{"id": file_id + incr, "name": f['name'], "size": str(round(len(f_w)/1024, 1))} for incr, (f, f_w) in enumerate(zip(file, file_write))]
        redis_client.set("cg_" + data["id"], json.dumps({"u": [{"id": str(d["id"]), "name": d["name"], "size": d["size"]} for d in document_info], "q": data["q"]}))

        WriteDocument(file_write, document_info, data['id'])

        if(chat_ret['model_id'] == 2 or chat_ret['model_id'] == 3):
            p = multiprocessing.Process(target = AnswerQuestionLLM, args=[chat_ret['chat'], data["q"], data["id"], document_info, [f.decode() for f in file_write]])
        else:
            p = multiprocessing.Process(target = AnswerQuestionLLMThink, args=[chat_ret['chat'], data["q"], data["id"], document_info])

        p.start()

        return CreateStreamingResponseNewAccess(valjwt[1], GetLLMAnswerStream, [data["id"]], 200)

def WriteDocument_OldSingle(file_data, document_info, conv_id):
    file_type = document_info['name'].split(".")[-1]
    file_path = chatdocumentpath + '/' + conv_id + '_' + document_info['id'] + '.' + file_type
    with open(file_path, 'wb') as file:
        file.write(file_data)

    redis_client.xadd("cs_" + conv_id, {"u": json.dumps(document_info)})

def WriteDocument(file_data, document_info, conv_id):
    print('&&&&&&&&')
    for i in range(0, len(document_info)):
        file_path = chatdocumentpath + '/' + conv_id + '_' + str(document_info[i]['id']) + '.' + document_info[i]['name'].split(".")[-1]
        with open(file_path, 'wb') as file:
            file.write(file_data[i])
    print({"u": json.dumps([{k: v for k, v in d.items() if k != "data"} for d in document_info])})
    redis_client.xadd("cs_" + conv_id, {"u": json.dumps([{k: v for k, v in d.items() if k != "data"} for d in document_info])})

@api_view(['DELETE'])
def DeleteAllChats(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('v' not in data or 't' not in data or data['t'] != 'password'):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    
    user_password = User.objects.filter(id = valjwt[3]).values('password')[0]
    if(PasswordCompare(data['v'], user_password['password']) == False):
        return CreateResponseNewAccess(valjwt[1], 'Password is incorrect', 409)
    
    path_del = list(chats.find({"user_id": valjwt[3], "chat.d": {"$exists": "true"}}, {"paths": "$chat.d.path"}))

    chat_del = chats.delete_many({"user_id": valjwt[3]})
    if(math.floor(chat_del.raw_result['ok']) == 1):
        filepath = chatdocumentpath if development != 'true' else 'D:/Downloads/diplomat/actual_work/app/frontend/components/chatdocuments'
        for i in path_del:
            for x in i['paths']:
                if(os.path.exists(filepath + '/' + x)):
                    os.remove(filepath + '/' + x)
        return CreateResponseNewAccess(valjwt[1], chat_del.raw_result['n'], 200)
    else:
        return HttpResponse(json.dumps('Could not delete the Chats'), status = 400)
    
## CreateChatTitle is Deprecated. Only CreateChatTitlteThink will now be used. Regardless of whether agent is ON or OFF
def CreateChatTitle(chat_id, user_question = "", document_content = None, document_name = None, max_doc_token_len = 3000):
    llm_classify = 2
    if(document_content != None and user_question == ""):
        llm_classify = 1
    elif(document_content != None):

        prompt_classify = f"""You are an AI assistant that generates titles for conversations involving uploaded files.

Your first task is to determine the type of user request.

CLASSIFY THE REQUEST INTO ONE OF TWO CATEGORIES:

1. GENERAL FILE REQUEST
Use this when:
- The user uploads a file and asks nothing
- The user question makes no sense, is a random string
- The user asks general questions such as:
- "What is this file about?"
- "What are the contents of this file?"
- "Explain this file"
- "Summarize this document"
- "Describe this file"


2. SPECIFIC FILE INFORMATION REQUEST

Use this when the user asks about specific information inside the file, such as:
- requesting data
- asking questions about particular fields
- requesting extraction or explanation of specific content
- referring to specific sections, values, or records
- The user input contains gibberish, random characters, meaningless text, or input that cannot be interpreted (e.g., "asdjkl123!@#", "??!!aa", random symbols, or nonsensical strings). These should default to this category.

--------
Return only the number 1 or 2 and nothing else

User Question:
{user_question}
"""
        llm_chat = [{'role': 'user', 'content': prompt_classify}]
        try:
            llm_classify = int(chat(llm_model, messages = llm_chat).message.content)
        except:
            return
        
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
    tokens = tokenizer.tokenize(document_content)
    if(len(tokens) > max_doc_token_len):
        document_content = tokenizer.convert_tokens_to_string(tokens[0 : max_doc_token_len])

    if(llm_classify == 1):
        title_prompt = f"""You are an AI assistant that analyzes uploaded files.
Your task is to generate ONLY a short descriptive title for the file.

Rules:
1. Output ONLY the title.
2. Do NOT include explanations, sentences, or bullet points.
3. Do NOT include extra text before or after the title.
4. Use simple, clear wording.
5. Avoid complex or technical vocabulary.

Examples of valid outputs:
PDF File Analysis
XML File Breakdown
JSON File Overview
CSV Data Summary
Schedule Planning File Contents
Text Document Overview

The response must contain exactly one short title.
{f"\nUser Question:\n{user_question}" if user_question != "" else ""}
--- File: {document_name} ---
{document_content}
--- End of {document_name} ---"""
    else:
        title_prompt = f"""You are an AI assistant that creates concise, descriptive titles for chat conversations.

Given the conversation below, generate a short title (max 5-7 words) that clearly captures the main topic or purpose of the discussion.

Guidelines:
- Be specific and informative, not vague
- Avoid unnecessary filler words
- Do not include punctuation like quotes or periods at the end
- Use title case (capitalize major words)
- Focus on the core intent of the conversation
- If the input doesn't make sense, simply output one of the following: Unclear Input | Unclear Request | Incomplete Input
- If the input is friendly and general, don't make the title too complicated
- focus solely on the core intent of the conversation and avoid adding unnecessary, extra words. Do not be verbose
- Avoid adding the words 'Needed' 'Description', especially at the end of the title
- If asked about certain information, avoid assuming where that information comes from (Database, File, USB device) unless mentioned

User Question:
{user_question}
"""
        if document_content != None:
            title_prompt += f"""
--- File: {document_name} ---
{document_content}
--- End of {document_name} ---"""

    llm_chat = [{'role': 'user', 'content': title_prompt}]
    try:
        llm_title = chat(llm_model, messages = llm_chat)
    except:
        return
    
    llm_title = llm_title.message.content
    chats.update_one({"_id": int(chat_id)},
                     {"$set": {"name": llm_title}})
    
    redis_client.xadd("cs_" + chat_id, {"t":llm_title})

def AnswerQuestionLLMThink(db_chat, user_question, chat_id, document_dict = None):

    total_answer = ''
    print('vrum vrum')
    print(document_dict)
    #try:
    llm_answer, think_stages, fetched_items, search = PassLLMThinkCompletePipeline(llm_model, user_question, chat_id, db_chat, document_dict)
    #except:
    #    print('opopop')
    #    redis_client.delete("cg_" + chat_id)
    #    return
    print('SKAAAAAAA')
    if(fetched_items != None):
        redis_client.xadd("cs_" + chat_id, {"i": json.dumps({"q": fetched_items, "s": search})}) # i -> items

    for chunk in llm_answer:
        
        if(chunk.done == True):
            redis_client.delete("cg_" + chat_id)
            redis_client.xadd("cs_" + chat_id, {"d": 1}) # d -> done # cs_ -> chat stream
            redis_client.expire("cs_" + chat_id, 3)
            if(document_dict == None):
                push_val = {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer, "think": think_stages}
                if(fetched_items != None):
                    push_val["i"] = fetched_items
                    push_val["s"] = search
                chats.update_one({"_id": int(chat_id)},
                                {"$push": {"chat": push_val}})
            else:
                push_val = {"t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer, "d": document_dict, "think": think_stages}
                if(user_question != ''):
                    push_val['q'] = user_question
                if(fetched_items != None):
                    push_val['i'] = fetched_items
                    push_val['s'] = search
                chats.update_one({"_id": int(chat_id)},
                                {"$push": {"chat": push_val}})
            return

        total_answer += chunk.message.content
        redis_client.xadd("cs_" + chat_id, {"v": chunk.message.content})

def CreateChatTitleThink(chat_id, user_question = '', file_name = None):
    llm_title = CreateConversationTitleThink(llm_model, user_question, file_name)
    if(llm_title != None):
        chats.update_one({"_id": int(chat_id)},
                     {"$set": {"name": llm_title}})
    
    redis_client.xadd("cs_" + chat_id, {"t":llm_title})

def AnswerQuestionCloud(db_chat, user_question, chat_id, document_dict = None, gpt_apikey = ''):
    total_answer = ''
    conversations = []

    client = OpenAI(api_key = gpt_apikey)

    # Collect past uploaded files
    for conv in db_chat:
        user_content = []
        
        if conv.get("q"):
            user_content.append({
                "type": "input_text",
                "text": conv["q"]
            })
        
        for doc in conv.get("d", []):
            user_content.append({
                "type": "input_file",
                "file_id": doc["cloud_id"]
            })
        
        conversations.append({
            "role": "user",
            "content": user_content
        })

        if conv.get("a"):
            conversations.append({
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": conv["a"]
                    }
                ]
            })

    # Handle new document uploads
    new_upload_docs = []

    if(document_dict != None):
        for doc in document_dict:

            # Upload new file
            uploaded_file = client.files.create(
                file=open(chatdocumentpath + '/' + chat_id + '_' + str(doc['id']) + '.' + doc['name'].split('.')[-1], "rb"),
                purpose="assistants"
            )

            doc["cloud_id"] = uploaded_file.id

            new_upload_docs.append(doc)

    # Add new message
    new_content = []
    
        # New Question
    if user_question != '':
        new_content.append({
            "type": "input_text",
            "text": user_question
        })

        # New file uploads
    if document_dict != None:
        for doc in document_dict:
            new_content.append({
                "type": "input_file",
                "file_id": doc["cloud_id"]
            })
        if(user_question == ''):
            new_content.append({
                "type": "input_text",
                "text": "Please analyze the uploaded file."
            })

    conversations.append({
        "role": "user",
        "content": new_content
    })

    # Trim history
    conversations = conversations[-20:]

    # Send request
    stream = client.responses.create(
        model="gpt-4.1",
        input=conversations,
        stream=True
    )

    # Stream response
    for event in stream:
        if event.type == "response.output_text.delta":
            total_answer += event.delta
            redis_client.xadd("cs_" + chat_id, {"v": event.delta})

    # Streaming Done
    redis_client.delete("cg_" + chat_id)
    redis_client.xadd("cs_" + chat_id, {"d": 1}) # d -> done # cs_ -> chat stream
    redis_client.expire("cs_" + chat_id, 3)
    if(document_dict == None):
        push_val = {"q": user_question, "t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer}
        chats.update_one({"_id": int(chat_id)},
                        {"$push": {"chat": push_val}})
    else:
        push_val = {"t": datetime.datetime.now(datetime.timezone.utc), "a": total_answer, "d": document_dict}
        if(user_question != ''):
            push_val['q'] = user_question
        chats.update_one({"_id": int(chat_id)},
                        {"$push": {"chat": push_val}})