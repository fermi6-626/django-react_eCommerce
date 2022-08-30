import jwt
import datetime
from rest_framework import status
from rest_framework.response import Response


def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
    }, 'access_secret', algorithm='HS256')


def create_refresh_token(id):
    return jwt.encode({
        'user_id': id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }, 'refresh_secret', algorithm='HS256')


def decode_access_token(token):
    try:
        return jwt.decode(token, 'access_secret', algorithms='HS256').user_id
    except:
        return Response({"message": "Authentication error"}, status=status.HTTP_401_UNAUTHORIZED)
