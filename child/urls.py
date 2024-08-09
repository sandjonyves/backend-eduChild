from django.urls import path,include
from .views import ChildView
from rest_framework import routers

route =routers.SimpleRouter()

route.register('',ChildView,basename='child')

urlpatterns =[
    
    path('',include(route.urls)),
    
]