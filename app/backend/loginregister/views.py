from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import argon2
import hmac
import hashlib
import base64
import os
import datetime
import secrets
import string
from .models import User, Referal
from oauth import CreateJWTPair, VerifyJWT, ReturnResponseWithNewAccessRefreshTockens, GetJWTExpTime, ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired, CreateJWTKeyPair, CreateResponseWithCookies, ValidateAndCreateJWT, ValidateJWT
from snowflake_id_gen import GenerateSnowflake, CreateSnowflake
from django.core.cache import cache
from PIL import Image
import io
import re
from referal.models import Referal
import jwt
from backend.redis_connection import redis_client

pepper_key = str.encode(os.environ.get('pepper_key'))
path_to_img = str.encode(os.environ.get('path_to_img'))
# Remove this once in production
development = str.encode(os.environ.get('development'))

# Logs User in
@api_view(['POST'])
def handleLogin(request):
    if(request.method == 'POST'):
        print('user tesing login..')
        try:
            #data = request.data
            data = json.loads(request.body.decode('utf-8'))
            if(CheckData(data, method = 'l') == 'RE'):
                return HttpResponseBadRequest('Http 400 Bad Request')
            else:
                userfound = Find_User(data)
                print(userfound)
                if(userfound == None):
                    return Response('User not Found')
                if(userfound.status == 'D'):
                    return HttpResponse(json.dumps('User Account has been deleted'), status = 409)
                if(PasswordCheck(data['p'], userfound.password) == True):
                    jwtpair_dict = CreateJWTPair(userfound.id)
                    print(connection.queries)
                    exp_time = GetJWTExpTime(jwtpair_dict)
                    print(exp_time)
                    print('??/')
                    response = ReturnResponseWithNewAccessRefreshTockens(json.dumps('User Successfully Logged In!'),
                                                                         jwt_r = jwtpair_dict, exp_time = exp_time)
                    cookie_name = userfound.name
                    if(cookie_name == None):
                        cookie_name = 'None'
                    response.set_cookie("user_name", cookie_name, httponly=False, secure=True, samesite='None',
                                        max_age = exp_time)
                    print(response)
                    print(response.cookies)
                    return response
                else:
                    # 401: Could not authorize (incorrect credentials)
                    # 403: Was authorized / but does not have permission to that url
                    return HttpResponse(json.dumps('Wrong Password'), status = 401)
        except User.DoesNotExist:
            return HttpResponse(json.dumps('User does not exist!'), status = 401)
        #except:
        #    return HttpResponse(json.dumps('Http 400 Bad Request'), status = 404)
    else:
        # Maybe uneccessary dut to api_view
        return HttpResponseBadRequest('Http 400 Bad Request')


# NOTE: May no need for this since  django is supposedly already handling stuff like that. CHECK IT
# Checks Whether received data are OK
def CheckData(JSONQuery, method = 'r'):
    # e -> email , n -> phone_number , p -> password , RE -> RAISE_EXCEPTION
    # r -> register
    # print(JSONQuery)
    # print(type(JSONQuery))
    if(type(JSONQuery) != dict):
        print('1_')
        return 'RE'
    if( ("e" not in JSONQuery) or ("n" not in JSONQuery) or ("p" not in JSONQuery)):
        print("2_")
        return 'RE'
    if( ( (type(JSONQuery['e']) != str and JSONQuery['e'] != None)) or ( (type(JSONQuery['n']) != str and JSONQuery['n'] != None)) or (type(JSONQuery['p']) != str)):
        print('3_')
        return 'RE'
    if( (JSONQuery['e'] == None) and (JSONQuery['n']) == None ):
        print("4_")
        return 'RE'
    if(JSONQuery['e'] != None):
        if(JSONQuery['e'].find(' ')!= -1):
            print("5_")
            return 'RE'
    if(method == 'r'):
        if(JSONQuery['e'] != None):
            contains_a = JSONQuery['e'].find('@')
            contains_dot = JSONQuery['e'].find('.')
            if( (contains_a == -1) or (contains_dot == -1) or (contains_a + 1 >= contains_dot) or (len(JSONQuery['e']) < 5) or (contains_a == 0) or (contains_dot == len(JSONQuery['e']) - 1 )):
                return 'RE'
        else:
            if(len(JSONQuery['n']) < 5):
                return 'RE'
        if( (len(JSONQuery['p'])<7) or (len(JSONQuery['p'])>30) or (any(char.isdigit() for char in JSONQuery['p']) == False) or (any(char.islower() for char in JSONQuery['p']) == False) or (any(char.isupper() for char in JSONQuery['p']) == False)):
            return 'RE'
    # print('OK')
    return 'OK'

# uses email or phone to find if user exists in database
@api_view(['POST'])
def Login_emailPhone_match(request):
    print('GOKUUU')
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body.decode('utf-8'))
            if(CheckData(data, method = 'l') == 'RE'):
                return HttpResponseBadRequest('Http 400 Bad Request')
            else:
                userfound = Find_User(data)
                print(userfound)
                print(data)
                if(userfound == None):
                    return Response('User not Found')
                else:
                    #return Response(json.dumps({'i': userfound.pk}))
                    return Response('User found')
        except:
            return HttpResponseBadRequest('Http 400 Bad Request')
    else:
        return HttpResponseBadRequest('Http 400 Bad Request!')


# Finds if user is in the database. Used by handleLogin function
def Find_User(JSONQuery):
    '''
    ###Variables
    @param: JSONQuery
    ###Description
    find the user (either by email or phone, depending on wht was provided. If both were provided then email will be used) in the database.
    If the user is found then a dictionary of the form {} is returned. If the user is not found then None is returned
    '''
    try:
        if(JSONQuery['e'] != None):
            userfound = User.objects.get(email = JSONQuery['e'])
        elif(JSONQuery['n'] != None):
            userfound = User.objects.get(phone = JSONQuery['n'])
        return userfound
    except:
        return None
    

# Hashes, Peppers, Salts passed password and checks whether its the same as the one in database
def PasswordCheck(password, password_db):
    pass_split = password_db.split('$')
    salt_db = pass_split[2]
    pass_db = pass_split[3]
    # can't do the below because salt param is only available in ver 23.1.0 and i have 21.3.0 of argon2-cffi (run in cmd pip show argon2-cffi)
    # Salting
    salted_pass = argon2.PasswordHasher(encoding = 'utf-8', time_cost=16, memory_cost=4096, parallelism=4,hash_len=32).hash(password = password, salt = base64.b64decode(salt_db))
    # argon2 ver 21.3 method (update argon and replace the below line with the above)
    # salted_pass = argon2.hash_password(password.encode('UTF-8'), time_cost=16, memory_cost= 4096, parallelism=2, hash_len=32, salt = salt_db.encode('UTF-8'), type = argon2.low_level.Type.ID).decode('UTF-8')
    salted_pass = salted_pass.split('$')[5]

    # Peppering
    peppered_pass = hmac.new(pepper_key, salted_pass.encode('UTF-8'), hashlib.sha256).hexdigest()
    # Hashing
    hash_pass = hashlib.sha256(peppered_pass.encode('UTF-8')).hexdigest()

    if(hash_pass == pass_db):
        return True
    else:
        return False
    

# Registers User
@api_view(['POST'])
def handleRegister(request):
    if(request.method == 'POST'):
        #try:
            data = json.loads(request.body.decode('utf-8'))
            if('r' not in data):
                return HttpResponse(json.dumps('Http 400 Bad request'), status = 400)
            if(type(data['r']) != str):
                return HttpResponse(json.dumps('Http 400 Bad request'), status = 400)
            if(len(data['r']) != 10):
                return HttpResponse(json.dumps('Http 400 Bad Request'), status = 400)
            if(CheckData(data) == 'RE'):
                #print('ayo')
                return HttpResponseBadRequest('Http 400 Bad Request')
            referal_ret = list(Referal.objects.filter(value = data['r']).values('date_created', 'date_redeem', 'id'))
            if(len(referal_ret) == 0):
                return HttpResponse(json.dumps('Incorrect Referal Code'), status = 409)
            if(len(referal_ret) > 1):
                referal_ret = [i for i in referal_ret if i['date_redeem'] == None]
            referal_ret = referal_ret[0]
            if(referal_ret['date_redeem'] != None):
                return HttpResponse(json.dumps('Referal Code has already been used'), status = 409)
            exp_date = referal_ret['date_created'] + datetime.timedelta(days = 1)
            if((datetime.datetime.now(datetime.timezone.utc) - exp_date).total_seconds() > 0):
                return HttpResponse(json.dumps('Referal Code has expired'), status = 409)
            
            userfound = Find_User(data)
            if(userfound != None):
                return Response('This account already exists!')
            fin_pass = PasswordSafe(password = data['p'])
            user_id = GenerateSnowflake()
            User.objects.create(email = data['e'], phone = data['n'], password = fin_pass, date_created = datetime.datetime.utcnow(), id = user_id)
            # CHECK FOR THE REFERAL CODE HERE
            Referal.objects.filter(id = referal_ret['id']).update(date_redeem = datetime.datetime.now(datetime.timezone.utc), userid_redeem = user_id)
            print('What???')
            jwtpair_dict = CreateJWTPair(user_id)
            print(connection.queries)
            response = HttpResponse('User Successfully Created!', status = 200)
            response.set_cookie("access", jwtpair_dict["access"], httponly = True, secure=True)
            response.set_cookie("refresh", jwtpair_dict["refresh"], httponly = True, secure=True)

            return response
        #except:
            #return Response('Http 400 Bad Request', status = status.HTTP_400_BAD_REQUEST)
            return HttpResponseBadRequest('Http 400 Bad Request')
    else:
        # Maybe uneccessary due to api_view
        return HttpResponseBadRequest('Http 400 Bad Request')
    


# Hashed, Peppers, Salts password
def PasswordSafe(password):
    '''
    # Variables
    @param: password (str)
    # Description
    Salts Peppers Hashes the password
    # Returns
    The salted, peppered, hashed password (str)
    '''

    # Salting
    salt_urandom = os.urandom(16)
    salted_pass = argon2.PasswordHasher(encoding='utf-8', time_cost=16, memory_cost=4096, parallelism=4,hash_len=32).hash(password, salt = salt_urandom)
    salt = base64.b64encode(salt_urandom).decode('utf-8')

    # Peppering
    peppered_pass = hmac.new(pepper_key, salted_pass[54:].replace('$','').encode('UTF-8'), hashlib.sha256).hexdigest()

    # Hashing
    hash_pass = hashlib.sha256(peppered_pass.encode('UTF-8')).hexdigest()

    final_password = '$SHA256$' + salt + '$' + hash_pass
    # Final password is of the form ${hash}${salt}${password_value} # Obviously there was peppering too, but don't want to put any info
    # about it in the db
    return final_password


# Create Referal
@api_view(['POST'])
def CreateReferalCode(request):
    '''
    # Variables
    @param: admin_key (str)
    # Description
    This function can be accessed via python manage.py runserver and on chrome writing the url: http://127.0.0.1:8000/loginregister/create_referal/
    In the Content box pass the ADMIN_KEY you posses. The admin key should NOT be enclosed in " " as is done with json strings.
    basically request.body should be something like: b"kosaojdosa"
    # Returns
    '''
    if(request.method == 'POST'):
        print('*****************************')
        print(request.body.decode('utf-8'))
        print(type(request.body.decode('utf-8')))
        print(json.loads(request.body.decode('utf-8')))
        print(type(json.loads(request.body.decode('utf-8'))))
        # {"first_name":"C","last_name":"D","key":b'isadm'}
        if(CheckAdminKey(request.body.decode('utf-8')) == 'OK'):
            #Referal.objects.create(referal_code = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10)),
            #                       )
            return Response('HADUKEN')
    else:
        return HttpResponseBadRequest('Http 400 Bad Request')
    


def CheckAdminKey(admin_key):
    '''
    # Variables
    @param: admin_key (str)
    # Description
    Checks if passed admin_key is valid
    # Returns
    'OK' if admin_key is valid
    'RE' if admin_key is NOT valid
    '''
    if(type(admin_key) != str):
        return 'RE'
    admin_keys_list = os.environ.get('ADMIN_KEYS').split('$')[:-1]
    if(admin_key in admin_keys_list):
        return 'OK'
    return 'RE'

@api_view(['DELETE'])
def Logout_OLDDEPRECATED(request):
    if(request.method == 'DELETE'):
        jwt_r = VerifyJWT(request)
        print(jwt_r)
        if(jwt_r[0] == False):
            return HttpResponseBadRequest('Http 400 Bad Request')
        cache.delete('rt_' + jwt_r[1]['iss'])
        response = Response('Logged out successfully')
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        response.delete_cookie('user_name')
        return response
    else:
        return HttpResponse(json.dumps('Bad Method'), status = 405)
    
@api_view(['POST'])
def UpdateValue(request):
    if(request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        if('access' not in request.COOKIES or 'refresh' not in request.COOKIES):
            return HttpResponse(json.dumps('no jwt provied'), status = 401)
        jwt_r = VerifyJWT(request)
        if('k' not in data or 'v' not in data or 'p' not in data):
            return HttpResponse(json.dumps('Bad Request'), status = 400)
        if(jwt_r[0] == False):
            return HttpResponse(json.dumps('Not authenticated'), status = 403)
        uservals = User.objects.filter(id = int(jwt_r[1]['iss'])).values('email', 'phone', 'name', 'password')[0]
        if(CheckDataValue(data['p'], 'password') == False):
            return HttpResponse(json.dumps('Bad Request Password'), status = 400)
        if(PasswordCheck(data['p'], uservals['password']) == False):
            return HttpResponse(json.dumps('Password is incorrect'), status = 409)
        user_info = None
        
        if(data['v'] == ''):
            data['v'] = None
        if(data['k'] == 'email'):
            if(data['v'] == None and uservals['phone'] == None):
                return HttpResponse(json.dumps('Either Email or Phone Number must have a value'), status = 409)
        elif(data['k'] == 'phone'):
            if(data['v'] == None and uservals['email'] == None):
                return HttpResponse(json.dumps('Either Email or Phone Number must have a value'), status = 409)
        
        if data['k'] == 'email':
            if(CheckDataValue(data['v'], 'email') == False):
                return HttpResponse(json.dumps('Bad Request Email'), status = 400)
            user_info = User.objects.filter(id = int(jwt_r[1]['iss'])).update(email = data['v'])
        elif data['k'] == 'password':
            # pn = password new
            if(CheckDataValue(data['v'], 'password') == False):
                return HttpResponse(json.dumps('Bad Request New Password'), status = 400)
            fin_password = PasswordSafe(password = data['v'])
            user_info = User.objects.filter(id = int(jwt_r[1]['iss'])).update(password = fin_password)
        elif data['k'] == 'phone':
            # ph = phone number
            if(CheckDataValue(data['v'], 'phone') == False):
                return HttpResponse(json.dumps('Bad Request Phone'), status = 400)
            user_info = User.objects.filter(id = int(jwt_r[1]['iss'])).update(phone = data['v'])
        elif data['k'] == 'name':
            if(CheckDataValue(data['v'], 'name') == False):
                return HttpResponse(json.dumps('Bad Request Name'), status = 400)
            user_info = User.objects.filter(id = int(jwt_r[1]['iss'])).update(name = data['v'])
        else:
            return HttpResponse(json.dumps('Bad Request'), status = 400)
        if(user_info != 1):
            return HttpResponse(json.dumps('Something went wrong'), status = 500)
        return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps('value successfully updated'),
                                                                         jwt_r = jwt_r)
    else:
        return HttpResponse(json.dumps('Bad Method'), status = 405)
    
@api_view(['POST'])
def UpdateImg(request, max_size_mb = 10):
    if request.method == 'POST':
        if('access' not in request.COOKIES or 'refresh' not in request.COOKIES):
            return HttpResponse(json.dumps('no jwt provided'), status = 401)
        jwt_r = VerifyJWT(request)
        if(jwt_r[0] == False):
            return HttpResponse(json.dumps('not authenticated'), status = 403)

        data = json.loads(request.data.get('data'))
        req_img = request.data.get('img')
        print('&&&NNN')
        print(req_img)
        print(type(req_img))
        print(req_img[:9])
        if('p' not in data):
            return HttpResponse(json.dumps('Http 400 Bad Request, important values are missing'), status = 400)
        if(CheckDataValue(data['p'], 'password') == False):
            return HttpResponse(json.dumps('Bad Request Password'), status = 400)
        passwuser = User.objects.filter(id = int(jwt_r[1]['iss'])).values('password')[0]
        if(PasswordCheck(data['p'], passwuser['password']) == False):
            return HttpResponse(json.dumps('Password is incorrect'), status = 409)
        
        if(type(req_img) != str):
            return HttpResponse(json.dumps('Bad Request Image'), status = 400)
        if(len(req_img)/1024/1024 > max_size_mb):
            return HttpResponse(json.dumps('Image must be smaller than 10MB'), status = 413)
        
        if(len(req_img) < 10):
            return HttpResponse(json.dumps('Http 400 Bad Request, Invalid image'), status = 400)
        if(req_img[:10] != 'data:image'):
            del_path = ''
            if(development.decode('utf-8') == 'true'):
                del_path = 'D:/Downloads/diplomat/actual_work/app/frontend/components/dev_images/' + jwt_r[1]['iss'] + '.JPEG'
            else:
                del_path = path_to_img.decode('utf-8') + '/' + jwt_r[1]['iss'] + '.JPEG'
            if(os.path.exists(del_path) == False):
                return HttpResponse(json.dumps('Http 400 Bad Request, Image deletion path does not exist'), status = 400)
            os.remove(del_path)
            user_info = User.objects.filter(id = int(jwt_r[1]['iss'])).update(img = False)
            return HttpResponse(json.dumps('Image successfully deleted'), status = 200)

        req_img = re.sub('^data:image/.+;base64,', '', req_img)
        with Image.open(io.BytesIO(base64.b64decode(req_img))) as im:
            if(im.format != 'JPEG'):
                return HttpResponse(json.dumps('Image Type not supported (only JPEG are supported)'), status = 415)
            if(im.width > 10000 or im.height > 10000):
                return HttpResponse(json.dumps('Image width or height exceed 10000 pixels'), status = 413)
            
            if(development.decode('utf-8') == 'true'):
                save_path = 'D:/Downloads/diplomat/actual_work/app/frontend/components/dev_images/' + jwt_r[1]['iss'] + '.' + im.format
            else:
                save_path = path_to_img.decode('utf-8') + '/' + jwt_r[1]['iss'] + '.' + im.format
            if im.format == 'JPEG':
                im.save(save_path, quality = 'keep')
            else:
                im.save(save_path, quality = 95)
            user_info = User.objects.filter(id = int(jwt_r[1]['iss'])).update(img = True)
            if(user_info != 1):
                return HttpResponse(json.dumps('Something went wrong'), status = 500)
            return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(json.dumps(save_path)), jwt_r = jwt_r)
    else:
        return HttpResponse(json.dumps('Bad Method'), status = 405)
    
@api_view(['GET'])
def GetUserInfo(request):
    if request.method == 'GET':
        if('access' not in request.COOKIES or 'refresh' not in request.COOKIES):
            return HttpResponse(json.dumps('no jwt provided'), status = 401)
        jwt_r = VerifyJWT(request)
        if(jwt_r[0] == False):
            return HttpResponse(json.dumps('Not authenticated'), status = 403)
        user_info = User.objects.filter(id = int(jwt_r[1]['iss']))
        user_ret = user_info.values('email', 'phone', 'name', 'img', 'is_admin')[0]
        if(user_ret['img'] == True):
            user_ret['img'] = jwt_r[1]['iss']
        return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(user_ret),
                                                                         jwt_r = jwt_r)
    else:
        return HttpResponse(json.dumps('Bad Method'), status = 405)
# Check Above 2 funcs. Create a GetUserData func

def CheckDataValue(val, valtype, allownone = True):
    if(valtype == 'password'):
        if(type(val) != str):
            return False
        if( (len(val)<7) or (len(val)>30) or (any(char.isdigit() for char in val) == False) or (any(char.islower() for char in val) == False) or (any(char.isupper() for char in val) == False)):
            return False
    elif(valtype == 'email'):
        if(allownone == True):
            if(val == None):
                return True
        if(type(val) != str):
            return False
        contains_a = val.find('@')
        contains_dot = val.find('.')
        count_a = val.count('@')
        count_dot = val.count('.')
        if( (contains_a == -1) or (contains_dot == -1) or (contains_a + 1 >= contains_dot) or (len(val) < 5) or (contains_a == 0) or (contains_dot == (len(val) - 1)) or (len(val)>255) or (count_a != 1) or (count_dot != 1)):
            return False
    elif(valtype == 'phone'):
        if(allownone == True):
            if(val == None):
                return True
        if(type(val) != str):
            return False
        if( (len(val)<5) or (len(val)>25)):
            return False
        if(val.count(' ') != 1):
            return False
        valsplit = val.split(' ')
        if((len(valsplit[0]) < 2) or (valsplit[0][0] != '+') or (valsplit[0][1:].isdigit() == False) or (valsplit[1].isdigit() == False) or (len(valsplit[0]) > 6) or (len(valsplit[1]) < 5) ):
            return False
    elif(valtype == 'name'):
        if(allownone == True):
            if(val == None):
                return True
        if(type(val) != str):
            return False
        if( (len(val)>7) or (len(val) == 0)):
            return False
    else:
        return False
    return True

@api_view(['GET'])
def GetUserImg(request):
    if request.method == 'GET':
        if 'access' not in request.COOKIES or 'refresh' not in request.COOKIES:
            return HttpResponse(json.dumps('no jwt provided'), status = 401)
        jwt_r = VerifyJWT(request)
        if(jwt_r[0] == False):
            return HttpResponse(json.dumps('Not authenticated'), status = 403)
        userimg = User.objects.filter(id = int(jwt_r[1]['iss'])).values('img')[0]
        if(userimg['img'] == True):
            userimg = jwt_r[1]['iss']
        else:
            userimg = False
        return ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(json.dumps(userimg), jwt_r = jwt_r)
    else:
        return HttpResponse(json.dumps('Bad Method'), status = 405)
    
@api_view(['DELETE'])
def DeleteUser(request):
    if request.method == 'DELETE':
        if 'access' not in request.COOKIES or 'refresh' not in request.COOKIES:
            return HttpResponse(json.dumps('no jwt provided'), status = 401)
        jwt_r = VerifyJWT(request)
        if(jwt_r[0] == False):
            return HttpResponse(json.dumps('Not authenticated'), status = 403)
        data = json.loads(request.body.decode('utf-8'))
        if('p' not in data or 'vp' not in data):
            return HttpResponse(json.dumps('Important values are missing'), status = 400)
        if(type(data['p']) != str or type(data['p']) != str):
            return HttpResponse(json.dumps('Invalid data types'), status = 400)
        if(data['p'] != data['vp']):
            return HttpResponse(json.dumps('Passed values are not equal'), status = 400)
        if(CheckDataValue(data['p'], 'password') == False):
            return HttpResponse(json.dumps('Bad Request Password'), status = 400)
        userfound = User.objects.filter(id = int(jwt_r[1]['iss'])).values('is_admin', 'status', 'password')
        if(userfound.count() == 0):
            return HttpResponse(json.dumps('User not found'), status = 409)
        if(userfound[0]['is_admin'] == True):
            return HttpResponse(json.dumps('User is admin. Admin Users cannot be deleted'), status = 409)
        if(userfound[0]['status'] == 'D'):
            return HttpResponse(json.dumps('User is already deleted'), status = 409)
        if(PasswordCheck(data['p'], userfound[0]['password']) == False):
            return HttpResponse(json.dumps('Password is incorrect'), status = 409)

        userdel = User.objects.filter(id = int(jwt_r[1]['iss'])).update(status = 'D')
        if(userdel == 0):
            return HttpResponse(json.dumps('Something went wrong. User could not be deleted'), status = 409)
        elif(userdel == 1):
            response_ret = HttpResponse(json.dumps('User succesffully deleted'), status = 200)
            response_ret.delete_cookie('access')
            response_ret.delete_cookie('refresh')
            response_ret.delete_cookie('user_name')
            return response_ret
        
    else:
        return HttpResponse(json.dumps('Bad Method'), status = 405)

@api_view(['DELETE'])
def TestDelete(request):
    print('**********8')
    print(request)
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    print(data['id'])
    print(type(data['id']))
    '''
    userfound = User.objects.filter(id = data['id']).values('is_admin', 'status')
    print(userfound)
    print(type(userfound))
    print('###########')
    print(userfound.count())
    print(type(userfound.count()))
    print(userfound[0])
    print(type(userfound[0]))
    print(userfound[0]['is_admin'])
    '''
    userdel = User.objects.filter(id = data['id']).update(status = 'D')
    print(userdel) # 0 NOT FOUND |||||| OR 1 WHEN FOUND
    print(type(userdel)) # int

@api_view(['POST'])
def findUser(request):
    # c -> l: login, r: register
    data = json.loads(request.body.decode('utf-8'))
    if("v" not in data or "t" not in data or "c" not in data):
        return HttpResponse(json.dumps('Important data are missing'), status = 400)
    if( (CheckDataValue(data["v"], data["t"], False) == False) or ( (data["c"] != "l") and (data["c"] != "r") )):
        return HttpResponse(json.dumps('Invalid data passed'), status = 400)
    matchuser = matchUserEmailPhone(data["v"], data["t"], False)
    if(data["c"] == 'l'):
        if(matchuser[0] == False):
            return HttpResponse(json.dumps(matchuser[1]), status = 404)
        else:
            return HttpResponse(json.dumps('User Found'), status = 200)
    else:
        if( (matchuser[0] == True) or (matchuser[1] == 'Account Deleted')):
            return HttpResponse(json.dumps('Email / Phone already in use'), status = 409)
        else:
            return HttpResponse(json.dumps('Valid Email / Phone'), status = 200)

def matchUserEmailPhone(val, valtype, returninfo = False):
    '''
    # Variables
    @param: val (str)
                must be the value of the email address or the value of the phone number. Example: 'test@testmail.com' or '1555333'
            valtype (str: 'email', 'phone')
                what is the val. An email address or a phone number
            returninfo (bool)
                Set to True to return additional information. Specifically the User's password, name, id
    # Description
    Searches the database to find a User based on the passed values. Specifically if valtype='email', searches the db for a user
    with email=val. If valtype='phone', searches the db for a user with phone=val. Note that if the user in the db has status='D'
    (Deleted), then the User will not be found
    # Returns
    A list. If the User is not found (either val did not match with email, phone OR user's status='D') in the db, then the list
    is of the form: [False (bool), message (str)]. If the User is found list is of the form:
    [True (bool), '' (str), '' (str), '' (str)] if returninfo=False OR
    [True (bool). userpassword (str), username (str), userid (int)] if returninfo=True
    '''
    userfound = None
    if(returninfo == False):
        if(valtype == 'email'):
            userfound = User.objects.filter(email = val).values('status')
        elif(valtype == 'phone'):
            userfound = User.objects.filter(phone = val).values('status')
        else:
            return [False, 'Invalid data type']
    elif(returninfo == True):
        if(valtype == 'email'):
            userfound = User.objects.filter(email = val).values('status', 'password', 'name', 'id')
        elif(valtype == 'phone'):
            userfound = User.objects.filter(phone = val).values('status', 'password', 'name', 'id')
    else:
        return [False, 'Something went wrong with the server']
    
    if(userfound.count() == 0):
        return [False, 'User Not Found']
    elif(userfound.count() == 1):
        if(userfound[0]['status'] == 'D'):
            return [False, 'Account Deleted']
    else:
        return [False, 'Something went wrong with the server']
    
    if(returninfo == False):
        return [True, '', '', '']
    else:
        return [True, userfound[0]['password'], userfound[0]['name'], userfound[0]['id']]
    

@api_view(['POST'])
def Login(request):
    data = json.loads(request.body.decode('utf-8'))
    if("v" not in data or "t" not in data or "p" not in data or "k" not in data):
        return HttpResponse(json.dumps('Important data are missing'), status = 400)
    if( ((data["t"] != 'email') and (data["t"] != 'phone')) or (CheckDataValue(data["v"], data["t"]) == False) or (CheckDataValue(data["p"], 'password') == False) or ((data["k"] != False) and (data["k"] != True)) ):
        return HttpResponse(json.dumps('Invalid data passed'), status = 400)
    
    matchuser = matchUserEmailPhone(data["v"], data["t"], True)
    if(matchuser[0] == False):
        return HttpResponse(json.dumps(matchuser[1]), status = 404)
    if(PasswordCompare(data["p"] ,matchuser[1]) == False):
        return HttpResponse(json.dumps('Incorrect Password'), status = 401)
    
    return CreateResponseWithCookies(matchuser[3], response_msg = 'User successfully logged in', username_cookie = matchuser[2] if matchuser[2] != None else 'None', rememberme = data["k"])
    
def PasswordCompare(password, password_db):
    password_split = password_db.split('$')
    salt_db = password_split[2]
    pass_db = password_split[3]

    salted_pass = argon2.PasswordHasher(encoding='utf-8', time_cost=16, memory_cost=4096, parallelism=4,hash_len=32).hash(password=password, salt=base64.b64decode(salt_db))
    salted_pass = salted_pass.split('$')[5]
    peppered_pass = hmac.new(pepper_key, salted_pass.encode('UTF-8'), hashlib.sha256).hexdigest()
    hash_pass = None
    if(password_split[1] == 'SHA256'):
        hash_pass = hashlib.sha256(peppered_pass.encode('UTF-8')).hexdigest()
    else:
        return False

    if(hash_pass == pass_db):
        return True
    else:
        return False
    
#############################3

@api_view(['POST'])
def Register(request):
    data = json.loads(request.body.decode('utf-8'))
    if("v" not in data or "t" not in data or "p" not in data or "r" not in data):
        return HttpResponse(json.dumps('Important data are missing'), status = 400)
    if( ((data["t"] != 'email') and (data["t"] != 'phone')) or (CheckDataValue(data["v"], data["t"], False) == False) or (CheckDataValue(data["p"], 'password', False) == False) or (type(data["r"]) != str) or (len(data["r"]) != 10) ):
        return HttpResponse(json.dumps('Invalid data passed'), status = 400)
    
    referal_find = FindReferal(data["r"])
    if(referal_find[0] == False):
        return HttpResponse(json.dumps(referal_find[1]), status = referal_find[2])
    
    userfound = matchUserEmailPhone(data["v"], data["t"], True)
    if( (userfound[0] == True) or (userfound[1] == 'Account Deleted')):
            return HttpResponse(json.dumps('Email / Phone already in use'), status = 409)
    
    userid = GenerateSnowflake()

    if(data["t"] == 'email'):
        User.objects.create(email = data["v"], password = PasswordSafe(data["p"]), date_created = datetime.datetime.now(datetime.timezone.utc), id = userid)
    elif(data["t"] == 'phone'):
        User.objects.create(phone = data["v"], password = PasswordSafe(data["p"]), date_created = datetime.datetime.now(datetime.timezone.utc), id = userid)
    else:
        return HttpResponse(json.dumps('Something went wrong with the server'), status = 500)
    Referal.objects.filter(id = referal_find[1]).update(userid_redeem = userid)

    return CreateResponseWithCookies(userid, response_msg='User successfully created')


def FindReferal(referal_value):
    referal_ret = Referal.objects.filter(value = referal_value).values('date_created', 'userid_redeem', 'id')
    if(referal_ret.count() >= 1):
        referal_ret = referal_ret.filter(userid_redeem = None)
        if(referal_ret.count() == 0):
            return [False, 'Referal Code has already been used', 409]
        for i in range(0, referal_ret.count()):
            exp_date = referal_ret[i]['date_created'] + datetime.timedelta(days = 1)
            if( (datetime.datetime.now(datetime.timezone.utc) - exp_date).total_seconds() < 0):
                return [True, referal_ret[i]['id'], 200]
        return [False, 'Referal Code has expired', 409]
    return [False, 'Incorrect Referal Code', 409]


@api_view(['DELETE'])
def Logout(request):
    cookies = request.COOKIES
    if "access" not in cookies:
        return LogoutResponse('Access Cookie Missing', 400)
    
    jwt_info = jwt.decode(cookies["access"], options={"verify_signature":False})
    if('alg' not in jwt_info):
        return LogoutResponse('Invalid Access Key', 400)
    jwtval = ValidateJWT(cookies["access"], "access", jwt_info)
    if(jwtval[2] == 200 or ("refresh" in cookies and jwtval[2] == 498)):
        if('iss' not in jwt_info):
            return LogoutResponse('Invalid Access Key', 400)
        if "refresh" not in cookies:
            access_list = redis_client.lrange('ut_' + jwt_info['iss'], 0, -1)
            if(access_list == []):
                return LogoutResponse('Cookie Expired', 498)
            else:
                if(cookies["access"] not in access_list):
                    return LogoutResponse('Something went wrong with the server', 500)
                elif('iat' not in jwt_info):
                    return LogoutResponse('Invalid Access Key', 400)
                elif( int(jwt_info['iat']) + int(os.environ.get('JWT_ACCESS_TIME')) < int(datetime.datetime.now(datetime.timezone.utc).timestamp()) ):
                    return LogoutResponse('Cookie Expired', 498)
        else:
            refreshcookie = redis_client.get('ur_' + jwt_info['iss'])
            if(refreshcookie != cookies["refresh"]):
                return LogoutResponse('Invalid Refresh Key', 400)
            elif(refreshcookie == None):
                return LogoutResponse('Cookie Expired', 498)

    elif(jwtval[2] != 200):
        return LogoutResponse(jwtval[1], jwtval[2])

    redis_client.delete('ur_' + jwt_info['iss'], 'ut_' + jwt_info['iss'])
    
    return LogoutResponse('Logged Out Successfully', 200)

def LogoutResponse(response, status):
    response = HttpResponse(json.dumps(response), status = status)
    response.delete_cookie('userinfo')
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response