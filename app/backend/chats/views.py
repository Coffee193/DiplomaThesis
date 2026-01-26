from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponseBadRequest, HttpResponse
from oauth import VerifyAuthRequest, ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired, VerifyJWT, ValidateAndCreateJWT, ReturnHttpInvalidJWT, CreateResponseNewAccess
from backend.mongo_db_connection import mongo_db
import json
from snowflake_id_gen import GenerateSnowflake
import datetime
from loginregister.models import User
from loginregister.views import PasswordCheck, CheckDataValue, PasswordCompare
import math
import base64
import os

# Create your views here.

chats = mongo_db['Chats']
chatdocumentpath = os.environ.get('CHAT_DOCUMENT_PATH')
development = os.environ.get('development')

@api_view(['GET'])
def getChats(request):
    if(request.method == 'GET'):
        print(request)
        print('LLLLLLLLLLLLLLLLLLLL')
        ver_req_auth = VerifyAuthRequest(request)
        if(ver_req_auth[0] != True):
            return ver_req_auth[1]
        print(ver_req_auth)
        ret = list(chats.aggregate( [{"$match": {"user_id": int(ver_req_auth[1]['iss'])}},
                                     {"$project": {"_id": 1, "name": 1, "date_created": 1}},
                                     {"$sort": {"date_created": 1}}]) ) #sort by date created
        for i in range(0, len(ret)):
            ret[i]["date_created"] = ret[i]["date_created"].timestamp()
            ret[i]["_id"] = str(ret[i]["_id"])
        return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(ret), jwt_r = ver_req_auth)
    else:
        return HttpResponseBadRequest('Http 400 Bad request')
    
@api_view(['POST'])
def createChats_Old(request):
    if(request.method == 'POST'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            data = json.loads(request.body.decode('utf-8'))
            if(data["model"] not in data_models):
                return HttpResponseBadRequest('Http 400 Bad request, model does not exist')
            if(type(data["q"]) != str):
                return HttpResponseBadRequest('Http 400 Bad request, invalid question')
            if(len(data["q"]) == 0):
                return HttpResponseBadRequest('Http 400 Bad Request, question is empty')
                
            chat_id = GenerateSnowflake()
            curr_time = datetime.datetime.now(datetime.timezone.utc)
            chats.insert_one({"_id": chat_id,
                        "name": "Conversation AA",
                        "date_created": curr_time,
                        "user_id": int(ver_req_auth[1]['iss']),
                        "model": data["model"],
                        "chat": [{"q": data["q"], "t": curr_time, "a": "asiojdsi"}]
                        })
            print('^&^&^&')
            print(json.dumps({"_id": chat_id, "name": "Conversation AA", "date_created": curr_time.timestamp()}))
            return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps({"_id": str(chat_id), "name": "Conversation AA", "date_created": curr_time.timestamp()}), jwt_r = ver_req_auth)
        except:
            print('EL GATO')
            return HttpResponseBadRequest('Http 400 Bad request')
    else:
        return HttpResponseBadRequest('Http 400 Bad request, method must be POST')
    
@api_view(['DELETE'])
def deleteChats(request):
    if(request.method == 'DELETE'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            data = json.loads(request.body.decode('utf-8'))
            
            if(type(data["_id"]) != str):
                return HttpResponseBadRequest('Http 400 Bad request, invalid id')
            try:
                data["_id"] = int(data["_id"])
            except:
                return HttpResponseBadRequest('Http 400 Bad Request, id could not be converted to int')
            
            chat_del = chats.delete_one({"_id": data["_id"], "user_id": int(ver_req_auth[1]['iss'])})
            if(chat_del.deleted_count != 1):
                return HttpResponseBadRequest('Http 400 Bad Request, Chat was not found')

            return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps('Chat successfully deleted!'), jwt_r = ver_req_auth)
        except:
            return HttpResponseBadRequest('Http 400 Bad request, something went wrong')
    else:
        return HttpResponseBadRequest('Http 400 Bad request, method must be DELETE')
    
@api_view(['POST'])
def renameChats_old(request):
    if(request.method == 'POST'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            if(type(data["rename"]) != str):
                return HttpResponseBadRequest('Http 400 Bad Request, data type must be str')
            if(len(data["rename"]) > 50):
                return HttpResponseBadRequest('Http 400 Bad Request, conversation name must be 50 characters or less')
            if(len(data["rename"]) < 5):
                return HttpResponseBadRequest('Http 400 Bad Request, conversation name must be more than 5 characters')
            
            # rename
            chat_ret = chats.update_one({"_id": int(data["_id"]), "user_id": int(ver_req_auth[1]['iss'])},
                                        {"$set": {"name": data["rename"]}})
            print(chat_ret)
            if(chat_ret.modified_count == 1):
                return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps('Chat Successfully Renamed'), jwt_r = ver_req_auth)
        except:
            return HttpResponseBadRequest('Http 400 Bad Request, something went wrong')
    else:
        return HttpResponseBadRequest('Http 400 Bad Request, method must be POST')
    
@api_view(['GET'])
def getChatConv(request, conv_id):
    if(request.method == 'GET'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            #chat_ret = chats.aggregate({"$match": {"_id": conv_id}},
            #                           {"$match": {"user_id": int(ver_req_auth[1]['iss'])}},
            #                           {"$project": {"chat": 1, "_id": 0}})
            chat_ret = chats.find_one({"_id": conv_id, "user_id": int(ver_req_auth[1]['iss'])}, {"_id": 0, "chat": 1, "model": 1})
            if(chat_ret == {}):
                return HttpResponseBadRequest('Http 400 Bad request, chat could not be found')
            else:
                for i in range(0, len(chat_ret['chat'])):
                    chat_ret['chat'][i]['t'] = chat_ret['chat'][i]['t'].timestamp()
                chat_ret = {'c': chat_ret['chat'], 'm': chat_ret['model']}
                return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(chat_ret), jwt_r = ver_req_auth)
        except:
            return HttpResponseBadRequest('Http 400 Bad Request, something went wrong')
    else:
        return HttpResponseBadRequest('Http 400 Bad Request, method must be GET')
    
@api_view(['POST'])
def answearQuestion_Old(request):
    if(request.method == 'POST'):
        try:
            ver_req_auth = VerifyAuthRequest(request)
            if(ver_req_auth[0] == False):
                return ver_req_auth[1]
            data = json.loads(request.body.decode('utf-8'))
            if(type(data["q"]) != str):
                return HttpResponseBadRequest('Http 400 Bad Request, question type must be string')
            if(len(data["q"]) == 0):
                return HttpResponseBadRequest('Http 400 Bad Request, question is empty')
            curr_time = datetime.datetime.now(datetime.timezone.utc)
            answear = 'YOYOYO'
            chat_ret = chats.update_one({"_id": int(data["c"]), "user_id": int(ver_req_auth[1]['iss'])},
                             {"$push": {"chat": {"q": data["q"], "t": curr_time, "a": answear}}})
            if(chat_ret.modified_count == 1):
                return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps({"a": answear}), jwt_r = ver_req_auth)
            else:
                return HttpResponseBadRequest('Http 400 Bad Request, something went wrong')
        except:
            return HttpResponseBadRequest('Http 400 Bad Request, something went wrong')
    else:
        return HttpResponseBadRequest('Http 400 Bad Request, method must be POST')
    
@api_view(['DELETE'])
def DeleteAllChats_old(request):
    if(request.method == 'DELETE'):
        try:
            if('access' not in request.COOKIES or 'refresh' not in request.COOKIES):
                return HttpResponse(json.dumps('no jwt provided'), status = 401)
            jwt_r = VerifyJWT(request)
            if(jwt_r[0] == False):
                return HttpResponse(json.dumps('not authenticated'), status = 403)
            data = json.loads(request.body.decode('utf-8'))
            if('p' not in data or 'vp' not in data):
                return HttpResponse(json.dumps('Http 400 Bad Request, important values are missing'), status = 400)
            if(type(data['p']) != str or type(data['vp']) != str):
                return HttpResponse(json.loads('Http 400 Bad Request, invalid data types'), status = 400)
            if(data['p'] != data['vp']):
                return HttpResponse(json.dumps('Http 400 Bad Request, passed values are not equal'), status = 400)
            if(CheckDataValue(data['p'], 'password') == False):
                return HttpResponse(json.dumps('Bad Request Passowrd'), status = 400)
            user_password = User.objects.filter(id = int(jwt_r[1]['iss'])).values('password')[0]
            if(PasswordCheck(data['p'], user_password['password']) == False):
                return HttpResponse(json.dumps('Password is incorrect'), status = 409)
            chat_del = chats.delete_many({"user_id": int(jwt_r[1]['iss'])})
            if(math.floor(chat_del.raw_result['ok']) == 1):
                return HttpResponse(json.dumps(chat_del.raw_result['n']), status = 200)
            else:
                return HttpResponse(json.dumps('Http 400 Bad request, something went wrong with deleting chats'), status = 400)
        except:
           return HttpResponse(json.dumps('Http 400 Bad Request, something went wrong'), status = 400)
    else:
        return HttpResponse(json.dumps('Http 400 Bad request, method must be DELETE'), status = 405)
    
@api_view(['GET'])
def GetChats(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    ret = list(chats.aggregate( [{"$match": {"user_id": valjwt[3]}},
                                     {"$project": {"_id": 1, "name": 1, "date_created": 1}},
                                     {"$sort": {"date_created": 1}}]) ) #sort by date created
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
            for x in i['paths']:
                if(os.path.exists(filepath + '/' + x)):
                    os.remove(filepath + '/' + x)
        return CreateResponseNewAccess(valjwt[1], 'Chat successfully deleted', 200)
    else:
        return HttpResponse(json.dumps('Conversation ID does not belong to User'), status = 400)
    
@api_view(['POST'])
def CreateChat(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    data = json.loads(request.body.decode('utf-8'))

    if('q' not in data):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    if(len(data['q']) == 0):
        return HttpResponse(json.dumps('Question is empty'), status = 400)
    
    chat_id = GenerateSnowflake()
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    chats.insert_one({"_id": chat_id,
                        "name": "New Conversation",
                        "date_created": curr_time,
                        "user_id": valjwt[3],
                        "chat": [{"q": data["q"], "t": curr_time, "a": "asiojdsi"}]
                        })
    
    return CreateResponseNewAccess(valjwt[1], {"_id": str(chat_id), "name": "New Conversation", "date_created": curr_time.timestamp()}, 200)

@api_view(['GET'])
def GetConversation(request, conv_id):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    chat_ret = chats.find_one({"_id": conv_id, "user_id": valjwt[3]}, {"_id": 0, "chat": 1, "model": 1})
    if(chat_ret == {}):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    else:
        for i in range(0, len(chat_ret['chat'])):
            chat_ret['chat'][i]['t'] = chat_ret['chat'][i]['t'].timestamp()
        chat_ret = {'c': chat_ret['chat']}
        return CreateResponseNewAccess(valjwt[1], chat_ret, 200)

@api_view(['POST'])
def AskQuestion(request):
    content_type = request.headers.get('content-type').split(';')[0]
    if(content_type == 'text/plain'):
        return AnswearQuestion(request)
    elif(content_type == 'multipart/form-data'):
        return AnswearQuestionWithDocument(request)
    else:
        return HttpResponse(json.dumps('Invalid Question Headers'), status = 400)


def AnswearQuestion(request):
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
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    answear = 'YOYOYO'
    chat_ret = chats.update_one({"_id": int(data["id"]), "user_id": valjwt[3]},
                        {"$push": {"chat": {"q": data["q"], "t": curr_time, "a": answear}}})
    if(chat_ret.modified_count == 1):
        return CreateResponseNewAccess(valjwt[1], {"a": answear}, 200)
    else:
        return HttpResponse(json.dumps('Conversation does not belong to User'), status = 400)
    
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
    
def AnswearQuestionWithDocument(request):
    valjwt = ValidateAndCreateJWT(request)
    if(valjwt[0] == False):
        return ReturnHttpInvalidJWT(valjwt)
    
    request_dict = request.data.dict()
    if('data' not in request_dict or 'document' not in request_dict or 'q' not in request_dict['data'] or 'id' not in request_dict['data'] or 'data' not in request_dict['document'] or 'name' not in request_dict['document']):
        return HttpResponse(json.dumps('Bad Request'), status = 400)
    data = json.loads(request_dict['data'])
    file = json.loads(request_dict['document'])
    
    if(data['id'].isdigit() == False):
        return HttpResponse(json.dumps('Invalid Id'), status = 400)
    if(len(file['data']) < 22 or file['data'][:21] != 'data:text/xml;base64,' or file['name'][-4:] != '.xml'):
        return HttpResponse(json.dumps('Invalid XML file'), status = 400)
    
    file_write = base64.b64decode(file['data'][21:])
    file_id = GenerateSnowflake()

    curr_time = datetime.datetime.now(datetime.timezone.utc)
    answear = 'YOYOYO'
    chat_val = {"d": {"name": file['name'], "path": data['id'] + str(file_id) + '.xml', "size": str(round(len(file_write)/1024, 1))}, "t": curr_time, "a": answear}
    if(len(data["q"].replace('\n', '')) != 0):
        chat_val["q"] = data["q"]
    chat_ret = chats.update_one({"_id": int(data["id"]), "user_id": valjwt[3]},
                        {"$push": {"chat": chat_val}})
    
    if(chat_ret.modified_count == 1):
        filepath = chatdocumentpath if development != 'true' else 'D:/Downloads/diplomat/actual_work/app/frontend/components/chatdocuments'
        with open(filepath + '/' + data['id'] + str(file_id) + '.xml', 'wb') as file:
            file.write(file_write)
        return CreateResponseNewAccess(valjwt[1], {"a": answear}, 200)
    else:
        return HttpResponse(json.dumps('Conversation does not belong to User'), status = 400)