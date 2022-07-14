import jwt
import datetime

# 发放token
def releaseToken(user_id):
    secret = "key"
    payload = {
        # 过期时间
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        # 发放时间
        'iat': datetime.datetime.utcnow(),
        # 自定义数据
        'data': {
            'id': user_id
        }
    }
    return jwt.encode(payload, secret, algorithm='HS256')

# 解析token
def parseToken(token_string):
    secret = "key"
    payload = jwt.decode(token_string, secret, algorithms='HS256', options={"verify_signature": False})
    return payload