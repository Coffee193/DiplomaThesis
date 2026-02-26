import jwt

# RSA

access_key_private = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAq/Es60o1ONimH5t6R4vOh7wIq30GoMbguvkT/o8m4V4TkOvp
aYsvJ7EY6PmrAk2F7bFzhRNsIkM8LLJE+XYyR5Mf6dj+Y7K9xh1XLL7DRMnYZ6ec
fhS8dDcym2FItq5llux31LFR80gq51eCTeyYG9r8RMsxJudtt/85zGyPNC3I0UfF
qpJMiuVgISA316JgcpVMGzDqbjFOrI+2CTe+Z5BNrwBr5sNPoAI8WZJYcXVJjz1U
priSlOSJHxbSLkFJvRNvmi4DUgsan0uYAsLkSQoN2eXvAzvYptAqREe0GI7l8v22
apU27G5JSIplTDXXzX7sshGczha66eT4aPwpVwIDAQABAoIBAEfTyMmD5wbXzlH+
386ak0z1moOVB5tLaV8CJT2erIXSCIduXcQG7kx8+WR9w9gC7ZNVoWXyrqYDg1RC
pni1zRxEVD0atm6MoSVtZVjeWfFXBq2Kgd/TpsQ/uMbbFYanBO5O22JBLvRb7fxV
fKwzzXk5ek/8uAxB+n42Qv1oTkxjskWrg0XnFg3HcPUMoElOSLur07cqHtYCayBt
i9QTkUe5JGo4Ejon9Z3p+OV5kRZipBHJ3l1Ebi9/+q6s5Y3NapLjl8taP95TxkBN
Vezrzckdf/dd3lxa5LjJ6g8PE25+8DdIIcVvgMNtuO1S5yxG1N6UrFybkr80uDly
ltSx7xkCgYEA4E0Jknc9JooMVS34KY2K5D1jCGJ5HnfW6J+MT+oyPhSwzahmiVa/
GgipyQ19h7WW2ng6RcBj98IoZ5tZNtFSz9R+AqR0HjYDlZ/v+WVqSblyji78uWiw
VV1AbScGWu3gBv7yoccJcyGw/FPUCbjCQhVZQBsOSkFg9w66V4UY4Y8CgYEAxD3a
QoD5INCd4hGG408yU32K4L+plDPeiZNkJg7eei6nVpbZukvPdF5cekcsKeEvgVyl
w6+NEwl4/HcsKcveem3nsRcDry2oq2VGiBJ/2zLcyqg7yJ+T9eSecbb9VfQ+iKTU
csp2EIZZJpuqsobhH221zWrwWLMn6jh9Gqclx7kCgYBZ2sKw6A+ZNshF/0pg6xDu
6iCYJUq8B+oR+ohtIzbJY+SIHqQk9JlNxpatsjfNe9NY5b0CYFYr1J33E2aj7Sst
ksSALn1N9PluoUmzMQtpSV840l3vsJ6jM94xW+bR2mVaqBtu75s7gg2yp6pT0q4P
Zxn/8lbBLHu5vS6tDOawxQKBgQCdmvdhled/PUyvtVfZ008d0qPo4MU263l8kE1M
a4CuLC3k0v5GKoCQewBWjDah4+KdSGUxBhqNAXyTdrqXTs59ESuVBGDHHipqjMna
mtDooK7Ga9qnw9G3GEdQGKDZmXFnmMmu739mwh9zbG3pN34yGZB7S7l/41LZP0jq
UPd8sQKBgQCgvk31Ij8NxqnCktmqw2HIjagBSPzMbF3cIbxvLSXZwH7192vgle94
Wt3CcuNZW0QobideDnhwd3A+zPIJJB8bgfXK6YvwXgU9oAWtjkpQ854pQgiXWg+w
UjyNjb4STpVl05lJo/1a/RlDAAQtvF1XL9FGtG5D3jfjyX1kwdvG1Q==
-----END RSA PRIVATE KEY-----
"""

access_key_public = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq/Es60o1ONimH5t6R4vO
h7wIq30GoMbguvkT/o8m4V4TkOvpaYsvJ7EY6PmrAk2F7bFzhRNsIkM8LLJE+XYy
R5Mf6dj+Y7K9xh1XLL7DRMnYZ6ecfhS8dDcym2FItq5llux31LFR80gq51eCTeyY
G9r8RMsxJudtt/85zGyPNC3I0UfFqpJMiuVgISA316JgcpVMGzDqbjFOrI+2CTe+
Z5BNrwBr5sNPoAI8WZJYcXVJjz1UpriSlOSJHxbSLkFJvRNvmi4DUgsan0uYAsLk
SQoN2eXvAzvYptAqREe0GI7l8v22apU27G5JSIplTDXXzX7sshGczha66eT4aPwp
VwIDAQAB
-----END PUBLIC KEY-----
"""

access_ps_public = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxBX+8MvtxIAGS+yfhNBl
/YXlHsmQwqF+JC71lgN3ntn1TVJQH+2FtbgcXTOz28Mo8/3VvBI3E4MvjJ6MnhV9
XMtzqs1uWpLXRK5LtLCBrH6LknhvUVit1fnH1KGMqiDFn8RcjzGG3y5LYmB6/kU+
L9OqmeJMZ8mBjPMXGuSmokh+jknPuRShEup7nLPM0CsuEoK0Ly4MAkMkJbksiK0i
u5ddoKR/mujxOdx/ccc5FG8+/j5yMNLzNowZ7j/EkQwSbwv9bX+O4+gRleFhOu3m
LJz/ytmTXBGTDvq1yU4tDolO9Nm+49eSmBlaornUHVf+L3QAZD9oZm6dAVLjvT31
swIDAQAB
-----END PUBLIC KEY-----
"""

access_ps_private = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxBX+8MvtxIAGS+yfhNBl/YXlHsmQwqF+JC71lgN3ntn1TVJQ
H+2FtbgcXTOz28Mo8/3VvBI3E4MvjJ6MnhV9XMtzqs1uWpLXRK5LtLCBrH6Lknhv
UVit1fnH1KGMqiDFn8RcjzGG3y5LYmB6/kU+L9OqmeJMZ8mBjPMXGuSmokh+jknP
uRShEup7nLPM0CsuEoK0Ly4MAkMkJbksiK0iu5ddoKR/mujxOdx/ccc5FG8+/j5y
MNLzNowZ7j/EkQwSbwv9bX+O4+gRleFhOu3mLJz/ytmTXBGTDvq1yU4tDolO9Nm+
49eSmBlaornUHVf+L3QAZD9oZm6dAVLjvT31swIDAQABAoIBAA2U5cb7+Qi77V5j
kgZQVkrMdBBBLzEBSowVt0D1azBU3HQcmBwosYg4AQ7w6SuhmuaQ1bW5ypgkEAO8
v59Q0bwUWNCjJgT0Asu+XtQHHb7ljPlPijZSNB2MDYFMJ0K+vlwl7QX7Yjd3LMAw
T+nowI6Y1J+QAxwf4u9GWdACYmBUZ1WZaFXXm79jOdv5VI1bLiZqZfgt2dbQRi/L
CYGND3FmoA5ecbt62rHOp+D1KdjL5PQ18YjEBXYE6FcmivLA1s28tEabXNRn6uYb
51ewbQOKLi76mrUqfO5eZSGzB1hSIHc1ICM29hBWOX4uMLYuEmyhyIlXT3wtirlh
9143DoECgYEA8UcstYoHRh1p0YGaIGbX4eT6MlWvOc2QsA/g87ohaIoX+IlZRDd3
JWDGy7SpHGtnT6lRDm4sTi/plcSwa+pStbN567xesuFjuHjG+z+Dzz0iK+cFmS2t
ky7i9hZX6K6An1RAy95MTUM/TkD03zE8EPdok48+LSqHX92FyF8UUxMCgYEA0Azo
qGGpS2AJOQVNTXCFhI8a2g7RiL2oW8suvDa7y7mr0/JrmPjvlkWqMQjkgU99I8Yo
SAx6wXwbCG0lzht5xcjexFFjcDs/K7HUktIu6M42ys0cyIc0BRc197a2cXQQw0DI
9dwgAkKGjetbEe0xXFEcPYvi/oFwHghHVLsnhuECgYEAsC85Bpd0GE8CJmptEZwH
qHx79qV6/sqNDQOLUG5qVtwABQzGknmuFy1D/Rw/IPGMzy7kcZUh5TY3a5Xk/eht
3SDhtrImtJjBKMOJCY6nwXzypvxbqi8gwIlMUkaeitpiMfZkGnqJXSHt6EamiRR6
uCjxxE6lKHYVxHsOZfKH9OECgYAmVFqAuw1fj5/jW3C0daiDlYHS7qv3z0k3MCW6
EzNiAyD++UiNdD9fphIG2qaOlEBv2NAPBg2Pm/e3A7TVVgaHQ8yWyo/RW3j16dtJ
+WMfDO7XShalcxNIZNBShNzz5fg4oLTlZtqWz/7OIrAyi0puwZq8VAtL7Djlr4zE
tX5AwQKBgQDILwgVJjt6/WJS+dLnbLV/39JDuVhEQmA06T2yMwf11gQN3yYz9nlc
ujQVApC8rRW5joMHlRUnN4lGVftRMde17/qJxfjamKVHqY2BHBAB4EWbv/h97IJf
77DmfuMOpwUy+5lxNv+ppCGuOlk3HOpaONXUPtXUDIC2tSx5pe1/Fw==
-----END RSA PRIVATE KEY-----
"""

access_es_public = """
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEKxuHKZPtEF/HzTXxIYFxqRMNnvq8
uumOroX6LJ4d6OzuZUugWLzjpOEmVMTC/NBea6+sG43QvSneww2JxWvw+w==
-----END PUBLIC KEY-----
"""

access_es_private = """
-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgxL0BjgGL/WS926Pn
Jka0tC7Sy/1JJTKOyt2LW6DytX6hRANCAAQrG4cpk+0QX8fNNfEhgXGpEw2e+ry6
6Y6uhfosnh3o7O5lS6BYvOOk4SZUxML80F5rr6wbjdC9Kd7DDYnFa/D7
-----END PRIVATE KEY-----
"""

''' RSA IS OK
jwtval = jwt.encode({"iat": '12989090', "iss": 'aiojdioj', "nonce": 'ijio(*()^)', "alg": 'RS256'}, access_key_private, 'RS256')
print(jwtval)
print('_____')
jwtdec = jwt.decode(jwtval, access_key_public, 'RS256')
print('***')
print(jwtdec)
'''

''' PS IS OK
jwtval = jwt.encode({"iat": '12989090', "iss": 'aiojdioj', "nonce": 'ijio(*()^)', "alg": 'RS256'}, access_ps_private, 'PS256')
print(jwtval)
print('_____')
jwtdec = jwt.decode(jwtval, access_ps_public, 'PS256')
print('***')
print(jwtdec)
'''

jwtval = jwt.encode({"iat": '12989090', "iss": 'aiojdioj', "nonce": 'ijio(*()^)', "alg": 'RS256'}, access_es_private, 'ES256')
print(jwtval)
print('_____')
jwtdec = jwt.decode(jwtval, access_es_private, 'ES256')
print('***')
print(jwtdec)
jwtll = jwt.decode(jwtval, access_es_public, 'ES256')
print('&&7')
print(jwtll)