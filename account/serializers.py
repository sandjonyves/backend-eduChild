from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import Admin ,Parent,CustomUser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    # user_type = serializers.IntegerField(write_only = True)
    class Meta:
        model = CustomUser
        fields = ('firstName','lastName','email','password','role')

class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField()
    password = serializers.CharField()


class AdminSerializers(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields =('__all__')



class ParentSerializers(serializers.ModelSerializer):

    class Meta:
        model  = Parent
        fields = ('__all__')
