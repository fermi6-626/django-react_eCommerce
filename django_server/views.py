from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Users
from rest_framework import status

# Create your views here.


class Register(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['pass_confirm']:
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

        def query(user):
            if user is None:
                return Response({"message": "invalid user"}, status=status.HTTP_404_NOT_FOUND)
            if not user.check_password(password):
                return err_stat
            serializer = UserSerializer(user)
            return serializer

        if "email" in request.data and "username" not in request.data and "password" in request.data:
            login_email = Users.objects.filter(email=email).first()
            serializer = query(login_email)
            return Response(query(login_email).data, status=status.HTTP_200_OK)
            # if login_email is None:
            #     return Response({"message": "invalid user"}, status=status.HTTP_404_NOT_FOUND)
            # if not login_email.check_password(password):
            #     return err_stat
            # serializer = UserSerializer(login_email)
            # return Response(serializer.data, status=status.HTTP_200_OK)

        elif "username" in request.data and "email" not in request.data and "password" in request.data:
            login_username = Users.objects.filter(username=username).first()
            serializer = query(login_username)
            return Response(query(login_username).data, status=status.HTTP_200_OK)
            # if login_username is None:
            #     return Response({"message": "invalid user"}, status=status.HTTP_404_NOT_FOUND)
            # if not login_username.check_password(password):
            #     return err_stat
            # serializer = UserSerializer(login_username)
            # return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Request not understood"}, status=status.HTTP_400_BAD_REQUEST)
