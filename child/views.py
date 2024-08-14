from django.shortcuts import render
from .models import Child
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import viewsets
from .serializers import ChildSerializers
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser

# Create your views here.


class ChildView(ModelViewSet):

    serializer_class = ChildSerializers
    queryset = Child.objects.all()
    permission_classes=[AllowAny]

    def partial_update(self, request, pk=None):
        serialized = ChildSerializers(request.user,data=request.data,partial=True)
        return Response(status=status.HTTP_202_ACCEPTED)


class CustomChilView(viewsets.ViewSet):
    permission_classes ={AllowAny}

    @action(detail=False,methods=['GET'],url_path='children-of-parent/(?P<parentUID>\w+)')
    def childrenOfParent(self,request,parentUID):
        
        queryset = Child.objects.filter(parentUID=parentUID)

        serailizer = ChildSerializers(queryset,many=True,context={"request":request})

        return Response(serailizer.data)