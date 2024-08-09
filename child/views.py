from django.shortcuts import render
from .models import Child
from rest_framework.viewsets import ModelViewSet 
from .serializers import ChildSerializers
from rest_framework.response import Response
from rest_framework import status 
# Create your views here.


class ChildView(ModelViewSet):

    serializer_class = ChildSerializers
    queryset = Child.objects.all()

    def partial_update(self, request, pk=None):
        serialized = ChildSerializers(request.user,data=request.data,partial=True)
        return Response(status=status.HTTP_202_ACCEPTED)