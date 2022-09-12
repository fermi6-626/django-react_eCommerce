import datetime
import random
import string
from django.core.mail import send_mail
from .models import Reset, Tokens, Users
from rest_framework import status, exceptions
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django_server.auth import Auth, create_token, decode_token, refresh_token
# Create your views here.


class Signup(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['confirm_pass']:
            return Response('Passwords do not match.')
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Login(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        err_stat = Response({
            "message": "invalid credentials"
        }, status=status.HTTP_400_BAD_REQUEST)
        user = Users.objects.filter(email=email).first()
        if "username" in request.data:
            user = Users.objects.filter(username=username).first()
        if user is None:
            return Response({"message": "invalid user"}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return err_stat
        access_token = create_token(user.id)
        session_token = refresh_token(user.id)
        # when logging in Token in models.py is populated with following data
        Tokens.objects.create(
            user_id=user.id,
            token=session_token,
            expired=datetime.datetime.utcnow() + datetime.timedelta(days=7)
        )
        response = Response()
        response.set_cookie(key='session-token',
                            value=session_token, httponly=True)
        response.data = {
            'token': access_token
        }
        return response


class User(APIView):
    authentication_classes = [Auth]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class RefreshSession(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('session-token')
        id = decode_token(refresh_token, 'session_token')
        if not Tokens.objects.filter(
            user_id=id,
            token=refresh_token,
            expired__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed('Authentication Error!')
        access_token = create_token(id)
        return Response({
            'token': access_token
        })


class Logout(APIView):
    def post(self, request):
        Tokens.objects.filter(
            token=request.COOKIES.get('session-token')).delete()
        response = Response()
        response.delete_cookie(key='session-token')
        response.data = {
            'message': 'Successfully logged out!'
        }
        return response


class ForgotPasswd(APIView):
    def post(self, request):
        email = request.data.get('email')
        token = ''.join(random.choice(string.ascii_letters) for i in range(32))
        Reset.objects.create(
            email=email,
            token=token
        )
        url = "http://127.0.0.1:3000/reset/"+token
        send_mail(
            subject='Did you forget your password again?',
            message='Click <a href="%s">here</a> to reset your password' % url,
            from_email='reset@email.com',
            recipient_list=[email],
        )
        return Response({
            'message': "Your password has been reset!"
        }, status=status.HTTP_200_OK)


class ResetPasswd(APIView):
    def post(self, request):
        data = request.data
        if data.get('password') != data.get('confirm_pass'):
            return Response('Passwords do not match.')
        reset_passwd = Reset.objects.filter(
            token=data.get('token')
        ).first()
        if not reset_passwd:
            raise exceptions.NotFound("Page doesn't exist!")
        user = Users.objects.filter(
            email=reset_passwd.email
        ).first()
        if not user:
            raise exceptions.NotFound("User doesn't exist!")
        user.set_password(data.get('password'))
        user.save()
        return Response({
            "message": "Your new password is %s" % data.get('password')
        })
