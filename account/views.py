from django.db import transaction
from django.shortcuts import render
from django.contrib.auth import authenticate ,login,logout
from django.core.mail import send_mail

from .serializers import UserSerializer,UserLoginSerializer, AdminSerializers,ParentSerializers
from.models import CustomUser,Parent,Admin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework import generics,viewsets,mixins
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.hashers import make_password

class PersonnalModelViewSet(
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass

def createAdmin(validated_data):
    return Admin.objects.create(
        is_superuser =True,
        is_staff=True,
        **validated_data
    )

def createParent(validated_data):
    return Parent.objects.create(
        is_staff=True,
        **validated_data
    )

class AdminUser(PersonnalModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AdminSerializers
    queryset = Admin.objects.all()

class ParentUser(PersonnalModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ParentSerializers
    queryset = Parent.objects.all()


class UserRegister(viewsets.ModelViewSet):

    permission_classes =[AllowAny]
    serializer_class =UserSerializer
    queryset = CustomUser.objects.all()

    def create(self,request,*arg,**kwarg):

        serializers = self.get_serializer(data=request.data)
        
        if serializers.is_valid():

            role = serializers.validated_data.get('role')
            password = serializers.validated_data.get('password')
            email = serializers.validated_data.get('email')
            
            serializers.validated_data['password']  =  make_password(password)

            if role == Admin.Role.ADMIN:
                user= createAdmin(serializers.validated_data)
            elif role == Parent.Role.PARENT:
                user = createParent(serializers.validated_data)
            else:
                raise serializers.ValidationError('This role can not exist ')
            #verifiction if the user have be succesfuli create
            
            if user is  None:
                return Response({'message':'error this user can not create '},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            user = authenticate(email = email, password=password)
            if not user:
                raise serializers.ValidationError('data is not valid')
            if not user.is_active:
                raise serializers.ValidationError('user is not activated ')

            login(request, user)
            token = RefreshToken.for_user(user)
            response_data = {
                'id':user.id,
                'refresh': str(token),
                'access': str(token.access_token),
                'message':'user create succesfuly'

            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        else:
            return Response({"message":"data is not valid "},status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    serializer_class=UserLoginSerializer
    permission_classes=[AllowAny]

    def post(self, request):
        """
        Login a user with their username and password.

        Parameters:
        username (str): The username of the user.
        password (str): The password of the user.

        Returns:
        Response: A JSON response containing the access and refresh tokens.

        Raises:
        ValidationError: If the provided credentials are invalid.
        """
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email = email, password=password)

        if not user:
            return Response({"message":"data is not valid"},status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({"message":"User is not activate"},status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        
        token = RefreshToken.for_user(user)
        # level_data = LevelSerializer(user.level_id).data if user.level_id else None
        # sector_data = SectorSerializer(user.sector_id).data if user.sector_id else None
        # token['role'] = user.role
        # token['firstName'] = user.firstName
        # token['lastName']  = user.lastName
        # token['email']  = user.email
        # token['phone_number'] = user.phone_number
        # token['password'] = user.password


        response_data = {
            'id':user.id,
            'refresh': str(token),
            'access': str(token.access_token),
             'message':'user login succesfuly'
        }
        return Response(response_data, status=status.HTTP_200_OK)
      
        
# class Logout(APIView):
#     permission_classes=[AllowAny]
class Logout(APIView):
    permission_classes=[AllowAny]
    def post(self, request,id):
        user =  CustomUser.objects.filter(id=id).first
        request.user = user
        # print(request.user)
        logout(request)
        if not request.user.is_authenticated:

            return Response({
            'message': 'logout succesfull'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
            'message': 'logout failed'
            })
