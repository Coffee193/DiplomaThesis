from django.shortcuts import render, HttpResponse

# Create your views here.

import datetime
import time
import secrets
import jwt
from rest_framework.decorators import api_view
import json
from django.core.cache import cache
import string
import os
from backend.redis_connection import redis_client

secret_jwt_key = "DpfBxh575Q"
secret_jwt_key_refresh = "Q71sIzsD0X"

# RS algos (also called RSA) need a private and a public key with a specific pattern
# a private is dependent on public and every 64 characters a newline is necessary
# just do a secrets.token_urlsafe(64) and then pass it on an online RSA key generator
secret_rsa_private_key ="""
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCvJlimNX8VynabcTLJFrKa6/TpC9ApC7qyP4uxVMWZ9Wqg7KQr
r7ebdqCeTpGXMMkHtQwxfbD4bGySqouMqkdo1hP7Wa4qkisj6EeryuR3R/2yOZRu
FnNu94XOR9ABNQNcGwuyrnVwBTHvo6gkh9qEycR1mKEgSllMM3flNbBw0QIDAQAB
AoGBAI4RBnrajZh5PrdanBzrojdzCJY3FMMWVnrafE58OkNlAvZAu/ELeFxLXoDJ
reH6mjT8L0W9c9ws5ewZFVQlkgEoFpzCybN1KcMjBg24BEn3Sr4Wh2LVseUFqdHh
3DJViquKpGXrxL2W1w+pYPajrYEWXkYdMLphneEAOQ45C/uBAkEA6E9ZHgyEQHWy
W/aScMutWzf6myUMS/uiQn38bFSz1aM3nM0bJWvEinRAuCWGe3/ddDuv8ZNNXpbC
t0sv2J8MmQJBAMECyGMISJRkfOtYwKxBQGCKoUblOn0OBXCVeY5IkkJtdTqj4DSV
i0EBcIsOREwdc0t7XMuSvjEislUbvD10sPkCQQDI0Zb7J9zHkDbP0rXCtf805I5J
wVwA7xTUH+6ugwY2fvKbJJ772U48VcSAq0e2yNDaIqK01R5Dz1Whd2hz/QG5AkBr
u8boaEZC9jg4EYkyXRW3DYpqDSdxiDMHHZgFEIL7KyfFPJW4JETfWxNbuvHqXoHt
fwVT6CvbN1e9Y8bVst3ZAkAbHqjaEeAvfGm+qcDLEiEuBDmldBaxuXeFcG3pLOnq
Bcez6CcbNi8x+4+RUq7GmfAVQ7YdqTkQoUnqrsYEmtZF
-----END RSA PRIVATE KEY-----
"""

secret_rsa_public_key = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCvJlimNX8VynabcTLJFrKa6/Tp
C9ApC7qyP4uxVMWZ9Wqg7KQrr7ebdqCeTpGXMMkHtQwxfbD4bGySqouMqkdo1hP7
Wa4qkisj6EeryuR3R/2yOZRuFnNu94XOR9ABNQNcGwuyrnVwBTHvo6gkh9qEycR1
mKEgSllMM3flNbBw0QIDAQAB
-----END PUBLIC KEY-----
"""

secret_ec_private_key = """
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIGdikX1bFNBCXBPpETXcyrhnPWhbxykc24gZkgFv2ioloAcGBSuBBAAK
oUQDQgAEWRVX4h2UrqTyETqZp0kmFQpE0S1+6T++7CFlosaiUYS3/n7JztpoQsLV
4BNm0DUb2irCnIAiy3Yac3iwJbvZqA==
-----END EC PRIVATE KEY-----
"""

secret_ec_public_key = """
-----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEWRVX4h2UrqTyETqZp0kmFQpE0S1+6T++
7CFlosaiUYS3/n7JztpoQsLV4BNm0DUb2irCnIAiy3Yac3iwJbvZqA==
-----END PUBLIC KEY-----
"""

secret_ed_private_key = "30770201010420ef330acd5a0fbb71d210f846e2ef47271768bd81dff65f78b8"

# https://8gwifi.org/eth-keygen.jsp
# https://8gwifi.org/jwsgen.jsp
# Here where i got keys from. For ED for some reason does not work

secret_ps_private_key = """
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAoIQL0csT2NrC2HULUR45YCXzB6sjHulPR4uRERGWuBwOUoQq
kPSAVkfv1d6i/eKFN/llPzf8TAmm4TmdsdNu+jZWuq59Sn/VzxzHU3ytOH+RHThG
utpUEowVqBR6cW7frmjSSxTOp7z5KRdXEKZx6LJC/4ls/G+ZyK9VcoQqjkHNiV2X
zOqtQld/0eHplkEJyvfaj33HuUVjR9nEs8cjrecrND5suSvUdGAKXqgQWPKdYuqX
SORYCkfBV7+cHsdcjjrYG87qCq+dENAUCs8GkwEQ3j7Xtac5RyLW1DBWzpowINW3
HE75CwusX3LaZbMLlasgmGFf8hrEJ0kkb7vc8QIDAQABAoH/OJlqzJjsl+NQbsfq
ZuFLRkNWeKKujmkFC3o08cX9BrNUCsSjeNv5KdXRY1OKOUqI/cdy9eGWqMMNRknt
H9DuH67OXFQDUBB0wDqDIjIZMSt7bCrYKFmsmkAZ2Plfle6zyXNnx0zT4IzLxOK6
7ho46N5Bctmp2VlZYJuGVIJZujGbnHljkAis8SJKCaUE9Zyy2IpEanmqP+UZ84hI
MdHeHHNkeXQQQIl+xpd2Wr1lS9HFxmGkeYtAT50+taWPrU3MF0tYEd63VbM5w/cq
NCKf72d3pKbdi32RzPdWSO50P4RfGqSS3RNp5kBsm2XvbiGDxDXkSbuo83lMwj5y
S9FfAoGBANtOnTJ40PDECkjKNM3vfCFc7jviT6eNaxDyjkPLpFGuZYSvd2g9d3H1
7rYq1+BHbPLGRUfKFC3OVyyi5+y+w5FySRJ/TDhztNOXeuNOyB5t3vlxStehtMV0
wbJ7s6dryeO+VTumB+IYJkaVlfWbqKhBFUEWntESC7PrGfLgBUN3AoGBALtfRv6V
i+rPVuvvikKfojXGQczUvcQ8zr742yYOyYd6L52RikOZvgunwQrWoooQCht0nV01
272R8g7vLYXhiubk7c+0ViS89Q2GiMMt7Fe/ZJOjJyHg+y5jPU1M7VYyywz+4BLX
JiBKV43ki2dLN1/NyLCbzWUfYSPdDjdWdmzXAoGBAIh+HD5ujXRcPx5go47Mj9Bf
+3JP/02EKe/pVvwBAatIxKxZXRMGtpG6BDFi5usS6U8McdAliHud4gnI9loVvLiI
jcwyaGj2MsRCklxpCwpNTaqohXFBlrYSXf/NF9qKrqPNMVUnl95zM1dZAHVVxRm7
MBRLlNsAxUHcgFD2drAvAoGBALIFMfSLrSXo3JLJQblO5dTlinrL3YhmpZ933O7p
ubuH8Vlpf83+cjuspJJhnohB+Phg8Wov05jm4u4hfETpJwl8lB11HytEhCbXnXSj
Wxt7cll696EOmldWXlXlMtFk7NpqBgagd07SkyDy9SespO3XHEf/n0PmbmqeifU1
psp9AoGASq/hUo/JoZbYJSebCROKIjAlBS3V9j18/pst+v7XV3Msd817ANEMBRhJ
2MhG4CTBkhIVL4BQmSt2oZwkVWUg+EWx/eYUCau6k8nkcJstJOm5ufXyBCiDgQ+/
nW0KjP/bq5TT+O1QPYNqX1akzRPMn8DDkKyMz7whqkJO/XPbhF8=
-----END RSA PRIVATE KEY-----
"""

secret_ps_public_key = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoIQL0csT2NrC2HULUR45
YCXzB6sjHulPR4uRERGWuBwOUoQqkPSAVkfv1d6i/eKFN/llPzf8TAmm4TmdsdNu
+jZWuq59Sn/VzxzHU3ytOH+RHThGutpUEowVqBR6cW7frmjSSxTOp7z5KRdXEKZx
6LJC/4ls/G+ZyK9VcoQqjkHNiV2XzOqtQld/0eHplkEJyvfaj33HuUVjR9nEs8cj
recrND5suSvUdGAKXqgQWPKdYuqXSORYCkfBV7+cHsdcjjrYG87qCq+dENAUCs8G
kwEQ3j7Xtac5RyLW1DBWzpowINW3HE75CwusX3LaZbMLlasgmGFf8hrEJ0kkb7vc
8QIDAQAB
-----END PUBLIC KEY-----
"""

jwt_algos = ['HS256', 'HS384', 'HS512', 'ES256', 'ES256K', 'ES384', 'ES512', 'RS256', 'RS384', 'RS512',
                         'PS256', 'PS384', 'PS512'] #EdDSA not supported as i cannot get it to work or some reason

encrypt_algos = ['PS256', 'HS256', 'RS256']

# Cant Get ES256 to Work. Probelm is in validation. It gets validated Both by public AND private key


secret_rsa_private_key_refresh = """
-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCg1VX1uTFUmRKZLC+aP6FcBuwRIlndn8q69JZ1li1GfW1OuE/W
KT85bpw/DSHtzLAiGSVbWSz7xej9tO1JVo2uFoDk6qC6fkQJ95Dsui3LonVw3LKQ
6cgUES1Uh52I58+p0RKTKmemESK3jtoBPQ3B/J5t0ctbO7FRxy/XYFUZfwIDAQAB
AoGAF0+0nOARyVxCeNcRsz7DyY3rS3R6KAhQHxbyc+qnd08Yt885KyZhVpa0qOLj
Zw9C/D4+zuW3AmsmIRfHSNj1welsI3pbVWWp5i20G7X3jfyMO7spXrTSyvbOFrqG
MkaF+Ai6gLgC00wqYLBoNjm5YhKD2MkBu6WjRN9dMUWmpSkCQQDqXiW3jxrVw2kI
v7Wsx/+XbvxC4EsibDj9IuUsw8pncjG7fdC327+kSJI0A8OZXZtn0vmhcxM0ga5E
0kR3TKbtAkEAr62mom6irTzaZsPPQ9ta50Ghb3PzTk/eYIYmJEBgPLaow7gGe50x
ndRUHoZlsGtMZSYiGjtRuFvndemrvFMomwJANx5fNnVUdVOYvzL/EhyTMtUqRLwl
T3ouSPJM/aMqVfvYUGT9kk//GS7sG4mLFeWa5+cJSHwc1ytshckByyDe3QJAWo5S
lOweotn5YnuQvVO2+fnUs1S7mCSHZo3/3zPn56PoPmr/vHx89PRcIBf7FwNYL9OG
RKtLJpMJLriys7LR/QJANEzzkVG/J4FeWKjMnYIDtNqyBMfYKW8ujKQF+z5fi9/h
sHv1a1GD/OFOhOYHdk+86fIQXcChajYDrBNriDrPvw==
-----END RSA PRIVATE KEY-----"""

secret_rsa_public_key_refresh = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCg1VX1uTFUmRKZLC+aP6FcBuwR
Ilndn8q69JZ1li1GfW1OuE/WKT85bpw/DSHtzLAiGSVbWSz7xej9tO1JVo2uFoDk
6qC6fkQJ95Dsui3LonVw3LKQ6cgUES1Uh52I58+p0RKTKmemESK3jtoBPQ3B/J5t
0ctbO7FRxy/XYFUZfwIDAQAB
-----END PUBLIC KEY-----"""

secret_ec_private_key_refresh = """
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIPdS6O8mrao0fqVzeBkwOMPXf0ONEcdaEcwnsZskwLgroAcGBSuBBAAK
oUQDQgAEds0XN0Vl5dPj4cX4V7AET1OALnkxiRWyjQCkDOM46G3+c95JMvJjSLEV
kJrqC+oY5VB2N6xXm9YK3C48k4JV8A==
-----END EC PRIVATE KEY-----"""

secret_ec_public_key_refresh = """
-----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEds0XN0Vl5dPj4cX4V7AET1OALnkxiRWy
jQCkDOM46G3+c95JMvJjSLEVkJrqC+oY5VB2N6xXm9YK3C48k4JV8A==
-----END PUBLIC KEY-----"""

secret_ps_private_key_refresh = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA6Q5r/MoW3SVzRVjzSUu9KNzE4JxLurvP8E5DVadcD4PKLJ4w
TN9BBJLvWcTGyBalQV6/1TJtXe31/uc5nwZP5IOyxaQDxeIa3xKQPKElfSbG5d5o
Pm/qAfHn9IJpI1q82EDBIeo5g5Hyd3hxpMtbe9BFavA8jmqO4dnvzyKt6tCdOr3J
iVwjV626m531e+Vg3srYZ6xWwcePiw1A9EQhur+focl5wnHDK3ryQTbmIuJVm+UV
RCBMC7DDnxejSA1VT2q4LRjS8JIuR/g0yzIriAvk792OHQExSuuI7FjFKjxQ+suq
g3Zlth9Mdu9zbmS124vEUeIMlIRxTBhVVsiOowIDAQABAoIBACluLWdOe7sLlc7d
rb45byKtAHjXgCTtj10uZIz9CAIgERhWdMqto47PGiqwrw/R6sXQtLSPVt7sVx9d
9qHdCuXaPbUh36PVeqZuU+LbWOFDO/eQTqLO3WBEI1KVvmARGOIuvMatL1VC5EI1
0KoVlqlPkI+ern041zayOg3uIdHMtlYyXg5ywYcw7pm+iCm9Z+2M3J8CZoH+Vmys
WyhW+Bub7wI7IMbm+NLzkmtHxu99WDq8XoqHgzfj5A8SutxeT+9TyuQ9ZrjTU8vg
9LsentJnbj3JAui4LOoOSE80wv5w5HHuYN2Raeri16XlSI/7Q0LCzq+tWgUZICCo
9dY0I20CgYEA9WHfoIiU8qPvogXsegJPvjOvRWP2V8tPgULMh9jwBqXhVnMKIMvq
BPKGLEP9nSvRJUb3pbt+KVkuNytjfgBgWKEJNaCvVOYltzC/x4FL1nQ3uSfJuZ63
loDQljyb82r8Imlik+0OyZtCd+RExr1J3VP5IQOYutT5YQD7sOQra/cCgYEA8yQD
FKu5Ogq8Wo5DblnU4cQE4hD4qZ7rc03kz/zWeXz0dyALV45ZbelncaXahTiV29qF
5DE2G/yRjrocXdCs7OmJ/a+pbK1ES5nbbvfMvBZ4lUVJay5hNkdLOe9nVrmd92s8
WuSJIWCfRXo+sAxD1OoZgA+bUcKjZOU1cHdcT7UCgYEAqEwRidRDfEvN7m1rrJ7r
PIPMYaZW7g4moHxFNaMntReOfrF2L9pLzkrclX2oc2T7FDshXU1EEW32EaaznVb6
va7tVxe3SV50XbmUv2vBrPuWwGo2pBXkytfcuD4npAMrnRp0nwqHCuVu6DXqqfhn
seKHSwphdTrfM5XuCnvkAC8CgYAiaPdSppb5QumzOy0J4gbByNcUE2jNwKL714tJ
cDP+T5PdhBh21LuNVZoBOIK7le2Hht6qE9jfjxgehfJbyJugj9CqqYCl08O1m1m1
07YS7G82WO7yD0dMwjxAP8R1PqG/kVqiVnOd2KnR0GIs0h+Lc3IWcJ7/rDcpoVK1
zv6ufQKBgQDWa87w6xefIZr9BY1Ex++eWhRNyU6pQJVZBOq8RdXicsR6jjYh2gsb
dQg/fl3PJAxFGNPpJuNnV5QKoDbsIXVT0v2rhjvU1Zzbk6dfVf0avUfEtk1My4am
cZC7E/OumnVmFbjgmCYNKGb4mkv8GXR/50uOUk3eecNUrPoSwOjhPA==
-----END RSA PRIVATE KEY-----
"""

secret_ps_public_key_refresh = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6Q5r/MoW3SVzRVjzSUu9
KNzE4JxLurvP8E5DVadcD4PKLJ4wTN9BBJLvWcTGyBalQV6/1TJtXe31/uc5nwZP
5IOyxaQDxeIa3xKQPKElfSbG5d5oPm/qAfHn9IJpI1q82EDBIeo5g5Hyd3hxpMtb
e9BFavA8jmqO4dnvzyKt6tCdOr3JiVwjV626m531e+Vg3srYZ6xWwcePiw1A9EQh
ur+focl5wnHDK3ryQTbmIuJVm+UVRCBMC7DDnxejSA1VT2q4LRjS8JIuR/g0yzIr
iAvk792OHQExSuuI7FjFKjxQ+suqg3Zlth9Mdu9zbmS124vEUeIMlIRxTBhVVsiO
owIDAQAB
-----END PUBLIC KEY-----"""

'''
VerifyJWT returns a tuple
1st -> bool: True if verified successfully
2nd -> dict: The JWT values (iat, exp, iss etc)
3rd -> dict: if acces token was refreshed then the dict holds two values {"access":,"refresh":}. These are the new 
            access token and the new rotated refresh token. Otherwise its empty
'''

# https://8gwifi.org/jwsgen.jsp -> to generate keys

public_rsa_access = os.environ.get('PUBLIC_RSA_KEY_ACCESS')
private_rsa_access = os.environ.get('PRIVATE_RSA_KEY_ACCESS')
public_rsa_refresh = os.environ.get('PUBLIC_RSA_KEY_REFRESH')
private_rsa_refresh = os.environ.get('PRIVATE_RSA_KEY_REFRESH')
public_ps_access = os.environ.get('PUBLIC_PS_KEY_ACCESS')
private_ps_access = os.environ.get('PRIVATE_PS_KEY_ACCESS')
public_ps_refresh = os.environ.get('PUBLIC_PS_KEY_REFRESH')
private_ps_refresh = os.environ.get('PRIVATE_PS_KEY_REFRESH')
hs_access = os.environ.get('HS_KEY_ACCESS')
hs_refresh = os.environ.get('HS_KEY_REFRESH')
public_es_access = os.environ.get('PUBLIC_ES_KEY_ACCESS')
private_es_access = os.environ.get('PRIVATE_ES_KEY_ACCESS')
public_es_refresh = os.environ.get('PUBLIC_ES_KEY_REFRESH')
private_es_refresh = os.environ.get('PRIVATE_ES_KEY_REFRESH')

def AppendNewRefreshAccessTokens(response, jwt_r):
    if(jwt_r[2] != {}):
        response.set_cookie("access", jwt_r[2]["access"], httponly = True, secure=True, samesite=True)
        response.set_cookie("refresh", jwt_r[2]["refresh"], httponly = True, secure=True, samesite=True)
    return response

def ReturnResponseWithNewAccessRefreshTockens_IfAccessExpired(response_content, response_status = 200, jwt_r = {}, exp_time = 'Auto'):
    response = HttpResponse(response_content, status = response_status)
    print(jwt_r)
    print(jwt_r[2])
    print('&&&')
    if(jwt_r[2] != {}):
        jwt_r = jwt_r[2]
        if(exp_time == 'Auto'):
            exp_time = int(jwt.decode(jwt_r["refresh"], options={"verify_signature": False})['exp']) - datetime.datetime.utcnow().timestamp()
        response.set_cookie("access", jwt_r["access"], httponly = True, secure=True, samesite='None')
        response.set_cookie("refresh", jwt_r["refresh"], httponly = True, secure=True, samesite='None', max_age = exp_time)
        print('==========')
        print(response.cookies)
    print('^^^^^^^^^^^^^^^^^^6')
    print(response)
    print(response_content)
    return response

def ReturnResponseWithNewAccessRefreshTockens(response_content, response_status = 200, jwt_r = {}, exp_time = 'Auto'):
    response = HttpResponse(response_content, status = response_status)

    if(exp_time == 'Auto'):
        exp_time = int(jwt.decode(jwt_r["refresh"], options={"verify_signature": False})['exp']) - datetime.datetime.utcnow().timestamp()
    response.set_cookie("access", jwt_r["access"], httponly = True, secure=True, samesite='None')
    response.set_cookie("refresh", jwt_r["refresh"], httponly = True, secure=True, samesite='None', max_age = exp_time)
    return response

def GetJWTExpTime(jwt_r, second_till_exp = True):
    # second_till_exp (if True returns the seconds till the cookie expires, else the timestamp of when it'll epire will be
    #                   returned)
    exp_time = int(jwt.decode(jwt_r["refresh"], options={"verify_signature": False})['exp'])
    if(second_till_exp == True):
        exp_time -= datetime.datetime.utcnow().timestamp()
    return exp_time

def VerifyRefreshAndGenerateNew(request, user_id):
    refresh = request.COOKIES.get('refresh')
    print('AAAAAAAAAAAAAAAAAAAaa')
    if(type(refresh) != str):
        print('AYO WTF')
        return False, ''
    if(cache.get('rt_' + user_id) != refresh):
        print( cache.get('rt_' + user_id) )
        print('###')
        print(refresh)
        print('---')
        print()
        print('Oh NOOOOO')
        return False, '', {}
    jwt_refresh = None
    for alg in jwt_algos:
        key_use = secret_jwt_key_refresh
        if(alg == 'PS512'):
            key_use = secret_ps_public_key_refresh
        elif(alg[:2] == 'RS' or alg[:2] == 'PS'):
            key_use = secret_rsa_public_key_refresh    
        elif(alg[:2] == 'ES' or alg[:2] == 'Ed'):
            key_use = secret_ec_public_key_refresh
        try:
            jwt_refresh = jwt.decode(refresh, key_use, audience = 'address', algorithms = [alg])
            break
        except jwt.ExpiredSignatureError:
            print('YO DAT EXPIRED!')
            return 'Refresh Expired'
        except:
            pass
    if(jwt_refresh != None):
        print('creating pair')
        oauth = CreateJWTPair(int(user_id), refresh_exp = jwt_refresh['exp'])
        jwt_r = oauth["access"]
        refresh = oauth["refresh"]
        cache.set('rt_' + user_id, refresh, timeout = int(jwt_refresh['exp']) - datetime.datetime.utcnow().timestamp())
        return True, jwt.decode(jwt_r, options={"verify_signature": False}), {"access": jwt_r, "refresh":refresh}
    else:
        return False, '', {}

def VerifyJWT(request):
    '''
    @info: returns True if JWT is correct. Note: There is aud param indicating what apis the user has access to. This
            is there to separate users from employees from superusers etc.
    '''
    jwt_c = request.COOKIES.get('access')
    print(jwt_c)
    if(type(jwt_c) != str):
        return False, ''
    jwt_r = None
    for alg in jwt_algos:
        key_use = secret_jwt_key
        if(alg == 'PS512'):
            key_use = secret_ps_public_key
        elif(alg[:2] == 'RS' or alg[:2] == 'PS'):
            key_use = secret_rsa_public_key    
        elif(alg[:2] == 'ES' or alg[:2] == 'Ed'):
            key_use = secret_ec_public_key
        try:
            jwt_r = jwt.decode(jwt_c, key_use, audience = 'address', algorithms = [alg])
            print('pppppppppppppppppp')
            print(jwt_r)
            print('**')
            break
        except jwt.ExpiredSignatureError:
            print('expired!!!')
            user_id = jwt.decode(jwt_c, options={"verify_signature": False})['iss']
            return VerifyRefreshAndGenerateNew(request, user_id)
        except:
            pass
        print(jwt_r)
    print('=============')
    if(jwt_r == None):
        return False, '', {}
    else:
        return True, jwt_r, {}

def CreateJWTPair(user_id, access = 'default_user', refresh_exp = None, remember_me = False):
    '''
    JWT payload will contain:
        iat: timestamp created in utc
        aud: string of urls that the user can access (as they are seen in urls.py of Ecommerce_backend)
        exp: expiration timestamp in utc (set 60 days from iat)
        nonce: 16-bit random string of letters (capital and lower) and numbers
    '''
    # Payload
    iat = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    aud = None
    if(access == 'default_user'):
        # No need to add login_register since you've already registed or logged in
        aud = 'address'
    iss = str(user_id)
    exp = str(int((iat + datetime.timedelta(minutes = 15)).timestamp()))
    if(refresh_exp == None):
        if(remember_me == True):
            exp_refresh = str(int((iat + datetime.timedelta(days = 60)).timestamp()))
        else:
            exp_refresh = str(int((iat + datetime.timedelta(days = 1)).timestamp()))
    else:
        exp_refresh = refresh_exp
    iat = str(int(iat.timestamp()))
    nonce = secrets.token_urlsafe()
    # Headers
    tp = 'JWT'
    alg = secrets.choice(jwt_algos)
    key_use = secret_jwt_key
    key_use_refresh = secret_jwt_key_refresh

    if(alg == 'PS512'):
        key_use = secret_ps_private_key
        key_use_refresh = secret_ps_private_key_refresh
    elif(alg[:2] == 'RS' or alg[:2] == 'PS'):
        key_use = secret_rsa_private_key
        key_use_refresh = secret_rsa_private_key_refresh
    elif(alg[:2] == 'ES' or alg[:2] == 'Ed'):
        key_use = secret_ec_private_key
        key_use_refresh = secret_ec_private_key_refresh
    
    jwt_c = jwt.encode({"iat": iat, "iss": iss, "exp":exp, "nonce": nonce, "aud": aud},
                    key_use,
                    alg)
    
    nonce_refresh = secrets.token_urlsafe()

    refresh_c = jwt.encode({"iat":iat, "iss": iss, "exp": exp_refresh, "nonce":nonce_refresh, "aud":aud},
                        key_use_refresh,
                        alg)
    cache.set('rt_' + iss, refresh_c, timeout = int(exp_refresh))
    o_auth = {"access":jwt_c, "refresh": refresh_c}
    
    return o_auth
    # jwt_c -> jwt cookie

@api_view(['GET'])
def CreateJWTPair_AsDifferentEndPoint(request, access = 'default_user'):
    '''
    JWT payload will contain:
        iat: timestamp created in utc
        aud: string of urls that the user can access (as they are seen in urls.py of Ecommerce_backend)
        exp: expiration timestamp in utc (set 60 days from iat)
        nonce: 16-bit random string of letters (capital and lower) and numbers
    '''
    if(request.method == 'GET'):
        user_id = json.loads(request.body.decode('utf-8'))['user_id']
        # Payload
        iat = datetime.datetime.utcnow()
        aud = None
        if(access == 'default_user'):
            # No need to add login_register since you've already registed or logged in
            aud = 'address'
        iss = str(user_id)
        exp = str(int((iat + datetime.timedelta(minutes = 15)).timestamp()))
        exp_refresh = str(int((iat + datetime.timedelta(days = 60)).timestamp()))
        iat = str(int(iat.timestamp()))
        nonce = secrets.token_urlsafe()
        # Headers
        tp = 'JWT'
        alg = secrets.choice(jwt_algos)
        key_use = secret_jwt_key
        key_use_refresh = secret_jwt_key_refresh

        if(alg == 'PS512'):
            key_use = secret_ps_private_key
            key_use_refresh = secret_ps_private_key_refresh
        elif(alg[:2] == 'RS' or alg[:2] == 'PS'):
            key_use = secret_rsa_private_key
            key_use_refresh = secret_rsa_private_key_refresh
        elif(alg[:2] == 'ES' or alg[:2] == 'Ed'):
            key_use = secret_ec_private_key
            key_use_refresh = secret_ec_private_key_refresh
        
        jwt_c = jwt.encode({"iat": iat, "iss": iss, "exp":exp, "nonce": nonce, "aud": aud},
                        key_use,
                        alg)
        
        nonce_refresh = secrets.token_urlsafe()

        refresh_c = jwt.encode({"iat":iat, "iss": iss, "exp": exp_refresh, "nonce":nonce_refresh, "aud":aud},
                            key_use_refresh,
                            alg)
        o_auth = json.dumps({"access":jwt_c, "refresh": refresh_c})
        #response = HttpResponse('access and refresh cookies set', status = 200)
        #response.set_cookie('o_auth', o_auth, httponly = True, secure=True)
        #response.set_cookie("refresh", refresh_c, httponly = True, secure=True)
        
        return HttpResponse(o_auth)
        # jwt_c -> jwt cookie
    else:
        return HttpResponse('Request method can only be GET', status = 405)

def CreateJWT_old(user_id, access = 'default_user'):
    '''
    JWT payload will contain:
        iat: timestamp created in utc
        aud: string of urls that the user can access (as they are seen in urls.py of Ecommerce_backend)
        exp: expiration timestamp in utc (set 60 days from iat)
        nonce: 16-bit random string of letters (capital and lower) and numbers
    '''
    # Payload
    iat = datetime.datetime.utcnow()
    aud = None
    if(access == 'default_user'):
        # No need to add login_register since you've already registed or logged in
        aud = 'address'
    iss = str(user_id)
    exp = str(int((iat + datetime.timedelta(days = 60)).timestamp()))
    iat = str(int(iat.timestamp()))
    nonce = secrets.token_urlsafe()
    # Headers
    tp = 'JWT'
    alg = secrets.choice(jwt_algos)
    key_use = secret_jwt_key
    if(alg == 'PS512'):
        key_use = secret_ps_private_key
    elif(alg[:2] == 'RS' or alg[:2] == 'PS'):
        key_use = secret_rsa_private_key    
    elif(alg[:2] == 'ES' or alg[:2] == 'Ed'):
        key_use = secret_ec_private_key
    
    jwt_c = jwt.encode({"iat": iat, "iss": iss, "exp":exp, "nonce": nonce, "aud": aud},
                       key_use,
                       alg)
    
    return jwt_c
    # jwt_c -> jwt cookie

def CreateJWT_debug(user_id, user_name, access = 'default_user', alg = 'HS256'):
    key_use = secret_jwt_key
    if(alg == 'PS512'):
        key_use = secret_ps_private_key
    elif(alg[:2] == 'RS' or alg[:2] == 'PS'):
        key_use = secret_rsa_private_key    
    elif(alg[:2] == 'ES' or alg[:2] == 'Ed'):
        key_use = secret_ec_private_key

    iat = datetime.datetime.utcnow()
    aud = None
    if(access == 'default_user'):
        # No need to add login_register since you've already registed or logged in
        aud = 'address'
    iss = user_name + str(user_id)
    #exp = str(int((iat + datetime.timedelta(days = 60)).timestamp() * 1000000))
    #iat = str(int(iat.timestamp() * 1000000))
    exp = str(int((iat + datetime.timedelta(days = 60)).timestamp()))
    iat = str(int(iat.timestamp()))

    # don't do *1000000 because that value will be later checked in JWT to see if that timestamp has come.
    # Also don't use float but truncate it to integer. This is because pyjwt compares the float to an int (when checking
    # if the timestamp has passed). When this is run really fast in some code perhaps it might raise errors
    nonce = secrets.token_urlsafe()

    jwt_c = jwt.encode({"iat": iat, "iss": iss, "exp":exp, "nonce": nonce, "aud": aud},
                       key_use,
                       alg)
    
    print(jwt_c)
    print(iat)
    return jwt_c

def VerifyJWT_debug(jwt_c, alg = 'HS256'):
    key_use = secret_jwt_key
    if(alg == 'PS512'):
        key_use = secret_ps_public_key
    elif(alg[:2] == 'RS' or alg[:2] == 'PS'):
        key_use = secret_rsa_public_key    
    elif(alg[:2] == 'ES' or alg[:2] == 'Ed'):
        key_use = secret_ec_public_key
    jwt_r = jwt.decode(jwt_c, key_use, audience = "address", algorithms = [alg])
    print(jwt_r)

def VerifyJWT_old(jwt_c):
    '''
    @info: returns True if JWT is correct. Note: There is aud param indicating what apis the user has access to. This
            is there to separate users from employees from superusers etc.
    '''
    if(type(jwt_c) != str):
        return False, ''
    jwt_r = None
    for alg in jwt_algos:
        key_use = secret_jwt_key
        if(alg == 'PS512'):
            key_use = secret_ps_public_key
        elif(alg[:2] == 'RS' or alg[:2] == 'PS'):
            key_use = secret_rsa_public_key    
        elif(alg[:2] == 'ES' or alg[:2] == 'Ed'):
            key_use = secret_ec_public_key
        try:
            jwt_r = jwt.decode(jwt_c, key_use, audience = 'address', algorithms = [alg])
            break
        except:
            pass
    if(jwt_r == None):
        return False, ''
    else:
        return True, jwt_r

# jwt_c = CreateJWT(1, 'John')
# print(jwt_c)
# print(VerifyJWT(jwt_c))

def VerifyAuthRequest(request, message401 = 'No JWT Provided', message403 = 'Not Authenticated'):
    if('access' not in request.COOKIES or 'refresh' not in request.COOKIES):
        return (False, HttpResponse(json.dumps(message401), status = 401))
    jwt_r = VerifyJWT(request)
    if(jwt_r[0] == False):
        return (False, HttpResponse(json.dumps(message403), status = 403))
    else:
        return jwt_r

def CreateJWTKeyPair(userid, rememberme = False):
    '''
    # Variables
    @param: userid (int)
                The userid, for who a JWT will be created
            rememberme (bool)
                If True: both refresh& access key will have a value. The refresh key will have an expiration of 60 days and
                access key of 15 minutes. The refresh will be stored in Redis with key: rk_{userid}
                If False: refresh = None & access will have a value. The access key will be a session cookie. Also in Redis we
                will store the access key with key name: ak_{userid}. In Redis it will have an expiration of 10 minutes. In
                the function VerifyJWT, if the key has not expired those 10 minutes will refresh. That way the user will stay
                logged in either until he closes the session OR 10 minutes of iactivity pass
    # Description
    Creates a JWT for the user. Also saves the approprite values in Redis database. If rememberme=True, it will set a keyvalue
    pair with key: ('ut_' + userid) AND value: (the value of the refresh key). The expiration of that keyvalue pair is defined
    by the enviroment variable: JWT_ACCESS_TIME. If rememberme=False, it will set a keyvalue pair with key: ('ut_' + userid) AND
    value: 
    # Returns
    A dict with keys "access", "refresh", "time. {"access" someval, "refresh": someval, "time": someval}
    If access=None & refresh=None, means something went wrong
    If type(access)=str & refresh=None, means user selected rememberme=False
    If type(access)=str & type(refresh)=str, means user selected rememberme=True
    If rememberme=True, type(time)=int and holds the creation date of refresh in seconds. In any other case time=None
    '''
    if(type(userid) != int):
        return {"access": None, "refresh": None}
    iat = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    if(rememberme == False):
        access_val = CreateJWTKey(userid, iat, "access", "private")
        if(access_val[0] == False):
            return {"access": None, "refresh": None, "time": None}
        redis_client.lpush('ut_' + str(userid), access_val[1])
        redis_client.expire('ut_' + str(userid), int(os.environ.get('JWT_ACCESS_TIME')))
        return {"access": access_val[1], "refresh": None, "time": iat}
    elif(rememberme == True):
        refresh_val = CreateJWTKey(userid, iat, "refresh", "private")
        access_val = CreateJWTKey(userid, iat, "access", "private")
        if(access_val[0] == False or refresh_val[0] == False):
            return {"access": None, "refresh": None, "time": None}
        redis_client.set('ur_' + str(userid), refresh_val[1], ex = int(os.environ.get('JWT_REFRESH_TIME')))
        return {"access": access_val[1], "refresh": refresh_val[1], "time": iat}
    else:
        return {"access": None, "refresh": None, "time": None}
    
def CreateResponseWithCookies(userid, jwtfail_msg = 'Something went wrong with the server', jwtfail_status = 500, response_msg = '', response_status = 200, username_cookie = 'None', rememberme = False):
    '''
    # Variables
    @param: userid (int)
                The userid, for who a JWT will be created
            jwtfail_msg (str)
                The string of the Response, if the Server couldnt create the JWT keys. That essentially means that
                the function CreateJWTKeyPair returned a dict with "access": None
            jwtfail_status (int)
                The status code of thr Response, if the Server couldnt crete the JWT keys.
            response_msg (str)
                The string of the Response, if everything is successfull
            response_status (int)
                The status code of the Response, if everything is successfull
            user_cookie (str)
                The username of the user. Essentially this affects the value of a returned cookie with key: 'userinfo'.
                That cookie hasa a value of the form: (username) + '$' + (userid). This cookie is accessed by the
                javascript frontend code, to recognise if someone is logged in or not
            rememberme (bool)
                If True: both refresh& access key will have a value. The refresh key will have an expiration of 60 days and
                access key of 15 minutes. The refresh will be stored in Redis with key: ur_{userid}
                If False: refresh = None & access will have a value. The access key will be a session cookie. Also in Redis we
                will store the access key with key name: ut_{userid}. In Redis it will have an expiration of 10 minutes. In
                the function VerifyJWT, if the key has not expired those 10 minutes will refresh. That way the user will stay
                logged in either until he closes the session OR 10 minutes of iactivity pass.
                ut_ -> usertemporary
                ur_ -> useremember
                NOTE: if rememberme=True, the stored cookie will be of the form: ur_+(userid): (refresh key value) -> expiration 60 days
                if rememberme=False, the stored cookie will be of the form: ut_+(userid): [(access key 1 value), (access key 2 value), ...] -> expiration 10 minutes

                That way if one device loggs in with rememberme=True, it will create the ur_(userid) key in Redis, pass the refresh value and set
                the expiration of the key. If another device loggs in with rememberme=True, it will get that same key from Redis 
                AND will NOT set a different key. That way all devices with rememberme=True share the shame refresh key.
                If a device loggs in with rememberme=False, it will create the ut_(userid) key in Redis (which is a list) and
                set its expiration and push its access key value. If another devices loggs in with rememberme=False, it will find
                the ut_(userid) key, and push its access key value in that list and reset the list's expiration. That way each
                device with rememberme=False is independent from one another
    # Description
    Creates an HttpRespone, with the appropriate cookies. If rememberme=False, the HttpResponse will have a userinfo AND access
    cookie. If rememberme=True, the HttpResponse will have a userinfo AND access AND refresh cookie
    value: 
    # Returns
    A HttpResponse
    '''
    jwt_keys = None
    if(rememberme == True):
        jwt_keys = GetRefreshCookie(userid)
    if(jwt_keys == None or jwt_keys["access"] == None):
        jwt_keys = CreateJWTKeyPair(userid, rememberme = rememberme)
    if(jwt_keys["access"] == None):
        return HttpResponse(json.dumps(jwtfail_msg), status = jwtfail_status)
    response = HttpResponse(json.dumps(response_msg), status = response_status)
    cookieexp = None
    if(jwt_keys["refresh"] != None):
        cookieexp = jwt_keys["time"]
        response.set_cookie("refresh", jwt_keys["refresh"], httponly = True, secure = False, max_age = int(os.environ.get('JWT_REFRESH_TIME')), samesite = "Lax")
    response.set_cookie("access", jwt_keys["access"], httponly = True, secure = True, max_age = int(os.environ.get('JWT_REFRESH_TIME')) if cookieexp != None else None, samesite = "Lax")
    response.set_cookie("userinfo", username_cookie + "$" + str(userid), httponly = False, secure = True, max_age = int(os.environ.get('JWT_REFRESH_TIME')) if cookieexp != None else None, samesite = "Lax")
    return response

def GetRefreshCookie(userid):
    '''
    # Variables
    @param: userid (int)
                The userid, for who the JWT refresh key will be retrieved
    # Description
    Gets the JWT refresh key of the user stored in Redis. Specifically it will try and search for the key with name:
    ur_+(userid).
    # Returns
    A dict with keys: "access", "refresh", "time".
    If the JWT key in Redis does not exist, then it will return: {"access": None, "refresh": None, "time": None}
    If the JWT key exists, then it will create an access key and return:
    {"access": (value of created access key), "refresh": (value of refresh key that was found in Redis), "time": (the creation time of the refresh key)}
    If an invalid userid is passed it will return: None
    '''
    if(type(userid) != int):
        return None
    refresh = redis_client.get('ur_' + str(userid))
    if(refresh == None):
        return {"access": None, "refresh": None, "time": None}
    else:
        iat = int(jwt.decode(refresh, options={"verify_signature":False})['iat'])
        access = CreateJWTKey(userid, iat, "access", "private")
        if(access[0] == False):
            return {"access": None, "refresh": None, "time": None}
        else:
            return {"access": access[1], "refresh": refresh, "time": iat}
        

def ValidateJWT(jwt_value, jwt_type, jwt_info = None):
    '''
    # Variables
    @param: jwt_value (str)
                the value of the JWT key (access OR refresh) that will be validated
            jwt_type (str)
                this value must either be "access" OR "refresh". If the key you are validating is an access key, pass
                "access". If the key you are validating is a refresh key, pass "refresh"
            jwt_info (None OR dict)
                If None, it will run the jwt_value through the function: jwt.decode(jwt_value, options={"verify_signature":False})
                This will essentially return a dict with the headers of the key. For keys it will have the names of the key
                headers AND for values it will have the corresponding values. You also may pass that dict yourself in jwt_info
                (If you have already gotten it before at some point in a parent function, you can pass it here and skip
                uneccessary computations).
    # Description
    Validates the key passed
    # Returns
    A list with len=3.
    The first value is a (bool): False -> if the key is invalid, True -> if the key is valid
    The second value is a (str): If key is valid it will be an empty string: ''.
        If the key is invalid, it will have the appropriate string explaining why the key is invalid
    The third value is an (int): A status code to be used in an HttpResponse. For example: If the key is valid then this value
        will be 200. For example: If the key has expired then this value will be 498
    '''
    if(jwt_type != "access" and jwt_type != "refresh"):
        return [False, 'jwt_type value must be "access" or "refresh"', 400]
    if(jwt_info == None):
        jwt_info = jwt.decode(jwt_value, options={"verify_signature":False})
        if('alg' not in jwt_info):
            return [False, 'Invalid JWT', 400]
    jwt_key = GetJWTKey(jwt_info['alg'], jwt_type, "public")
    if(jwt_key == None):
        return [False, 'Invalid Encryption Algo', 400]
    
    try:
        jwtkey = jwt.decode(jwt_value, jwt_key, jwt_info['alg'])
    except:
        return [False, 'Somwthing went wrong with the Server: Invalid Private Key', 400]
    
    time_val = 'JWT_ACCESS_TIME' if jwt_type == "access" else 'JWT_REFRESH_TIME'
    
    if(int(jwtkey['iat']) + int(os.environ.get(time_val)) < int(datetime.datetime.now(datetime.timezone.utc).timestamp())):
        return [False, 'Access Key Expired', 498]
    
    return [True, '', 200]

def GetJWTKey(jwtalgo, jwttype = "access", jwtcontent = "public"):
    '''
     # Variables
    @param: jwtalgo (str)
                The algorythm you are using to encode/decode a JWT key.
            jwttype (str)
                this value must either be "access" OR "refresh". If the key you are trying to encode/decode is an access key then
                pass the value "access". If the key you are trying to encode/decode is a refresh key then pass the value "refresh"
            jwtcontent (str)
                this value must either be "public" OR "private". If the key you are trying to encode a key, then pass the value
                "private". If you are trying to decode a key, then pass the value "public"
    # Description
    Gets the appropriate secret/private or public key, that will be used to encode OR decode a value/key
    # Returns
    None or str. If an invalid argument is passed then None will be returned. If everything is valid, it will return a string
    that is the value of the wanted key (private or public for the specific algorythm)
    '''
    if((jwttype != "access" and jwttype != "refresh") or (jwtcontent != "public" and jwtcontent != "private")):
        return None
    jwtkey = None
    if(jwtalgo == 'PS256'):
        if(jwttype == "access"):
            if(jwtcontent == "public"):
                jwtkey = public_ps_access
            else:
                jwtkey = private_ps_access
        else:
            if(jwtcontent == "public"):
                jwtkey = public_ps_refresh
            else:
                jwtkey = private_ps_refresh
    elif(jwtalgo == 'HS256'):
        if(jwttype == "access"):
            jwtkey = hs_access
        else:
            jwtkey = hs_refresh
    elif(jwtalgo == 'RS256'):
        if(jwttype == "access"):
            if(jwtcontent == "public"):
                jwtkey = public_rsa_access
            else:
                jwtkey = private_rsa_access
        else:
            if(jwtcontent == "public"):
                jwtkey = public_rsa_refresh
            else:
                jwtkey = private_rsa_refresh
    else:
        return None
    return jwtkey

def CreateNewAccess(access, refresh, access_info = None):
    if(access_info == None):
        access_info = jwt.decode(access, options={"verify_signature":False})
    if('iss' not in access_info):
        return [False, 'Invalid Access Key', 400, '']
    if(refresh == None):
        #if(access not in redis_client.lrange('ut_' + access_info['iss'], 0, -1)):
        if(redis_client.lrem('ut_' + access_info['iss'], 1, access) == 0):
            return [False, 'Invalid Access Key', 403, '']
        new_access = CreateJWTKey(int(access_info['iss']), keytype = "access", keycontent = "private")
        if(new_access[0] == False):
            return [False, 'Could not create new access key', 500]
        redis_client.expire('ut_' + access_info['iss'], int(os.environ.get('JWT_ACCESS_TIME')))
        redis_client.lpush('ut_' + access_info['iss'], new_access[1])
        return [True, new_access[1], 200, int(access_info['iss'])]
    else:
        #jwt_valid = ValidateJWT(refresh, "refresh")
        #if(jwt_valid[0] == False):
        #    return [False, 'Refresh Key Expired or Invalid', 400]
        if(redis_client.get('ur_' + access_info['iss']) != refresh):
            return [False, 'Invalid Refresh Key', 400, '']
        new_access = CreateJWTKey(int(access_info['iss']), keytype = "access", keycontent = "private")
        return [True, new_access, 200, int(access_info['iss'])]

def CreateJWTKey(userid, timestamp = None, keytype = "access", keycontent = "public"):
    if(type(userid) != int):
        return [False, 'userid must be an int']
    if(timestamp != None and type(timestamp) != int):
        return [False, 'timestamp must be an int or None']
    if(keytype != "access" and keytype != "refresh"):
        return [False, 'keytype value must be either "access" or "refresh"']
    if(keycontent != "public" and keycontent != "private"):
        return [False, 'keycontent value must be either "public" or "private"']
    if(timestamp == None):
        timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    nonce = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))
    algo = secrets.choice(encrypt_algos)
    key = GetJWTKey(algo, keytype, keycontent)

    jwtkey = jwt.encode({"iat": str(timestamp), "iss": str(userid), "nonce": nonce, "alg": algo}, key, algo)
    return [True, jwtkey]

def ValidateAndCreateJWT(request, newifexpired = True):
    cookies = request.COOKIES
    if("access" not in cookies):
        return [False, "Access Key Not Sent", 401, '']
    access_info = jwt.decode(cookies["access"], options={"verify_signature":False})
    if('alg' not in access_info):
        return [False, 'Invalid JWT', 400, '']
    
    valid_jwt = None
    if("refresh" in cookies):
        valid_jwt = ValidateJWT(cookies["access"], "access", access_info)
    

    if( ("refresh" not in cookies) or (valid_jwt[2] == 498 and newifexpired == True) ):
        return CreateNewAccess(cookies["access"], None if "refresh" not in cookies else cookies["refresh"], access_info)
    elif(valid_jwt[2] == 200):
        return [True, None, valid_jwt[2], int(access_info['iss'])]
    else:
        return [False, valid_jwt[1], valid_jwt[2], '']
    
def CreateResponseNewAccess(newaccess, response_msg = '', response_status = 200):
    response = HttpResponse(json.dumps(response_msg), status = response_status)
    if(newaccess != None):
        response.set_cookie("access", newaccess, httponly = True, secure = True, max_age = None, samesite = "Lax")
    return response

def ReturnHttpInvalidJWT(jwt, deletecookies = True):
    response = HttpResponse(json.dumps(jwt[1]), status = jwt[2])
    if(deletecookies == True):
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        response.delete_cookie('userinfo')
    return response