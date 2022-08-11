from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from .models import Users

class UserSerializer(ModelSerializer):
    class Meta():
        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'password', ]
        {
            'password': {'write_only': True}
        }

    def create(self, valid_data):
        password = valid_data

