from rest_framework.views import APIView
from rest_framework.response import Response
from django_server.auth import JWTAuthentication, create_access_token, create_refresh_token
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

        user = Users.objects.filter(email=email).first()
        if "username" in request.data:
            user = Users.objects.filter(username=username).first()

        if user is None:
            return Response({"message": "invalid user"}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return err_stat

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        response = Response()
        response.set_cookie(key='refresh_token',
                            value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }
        return response


class User(APIView):
    authentication_classes = [JWTAuthentication]
    print("hello duxk")

    def get(self, request):
        return Response(UserSerializer(request.user).data)
