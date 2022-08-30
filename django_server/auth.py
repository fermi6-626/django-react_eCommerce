import jwt
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .models import Users


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = Users.objects.get(pk=id)
            return user
        return Response({"message": "Authentication error"}, status=status.HTTP_401_UNAUTHORIZED)


def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
    }, 'access_secret', algorithm='HS256')


def create_refresh_token(id):
    return jwt.encode({
        'user_id': id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }, 'refresh_secret', algorithm='HS256')


def decode_access_token(token):
    try:
        return jwt.decode(token, 'access_secret', algorithm='HS256').get('user_id')
    except:
        return Response({"message": "Authentication error"}, status=status.HTTP_401_UNAUTHORIZED)
