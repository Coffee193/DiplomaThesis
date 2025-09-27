import datetime
import time
import secrets
import jwt

secret_jwt_key = "DpfBxh575Q"

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

def CreateJWT(user_id, access = 'default_user'):
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

def VerifyJWT(jwt_c):
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
    