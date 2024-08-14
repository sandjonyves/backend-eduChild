from django.urls import path,include
from .views import ChildView,CustomChilView
from rest_framework import routers

route =routers.SimpleRouter()

route.register('',ChildView,basename='child')
route.register('',CustomChilView,basename='children_of_parent')
urlpatterns =[
    
    path('',include(route.urls)),
 
    
]