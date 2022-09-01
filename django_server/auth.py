import jwt
import datetime
from .models import Users
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header


class Auth(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_token(token, 'access_token')
            user = Users.objects.get(pk=id)
            return (user, None)

        # rest_framework exception handler wtill convert it into appropriate Response with status_code
        raise exceptions.AuthenticationFailed('Authentication Error!')


def create_token(id):
    return jwt.encode({
        'user_id': id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
    }, 'access_token', algorithm='HS256')


def refresh_token(id):
    return jwt.encode({
        'user_id': id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }, 'session_token', algorithm='HS256')


def decode_token(token, which_token):
    try:
        return jwt.decode(token, which_token, algorithms='HS256').get('user_id')
    except:
        raise exceptions.AuthenticationFailed('Authentication Error!')
