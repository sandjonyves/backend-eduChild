from django.urls import path,include
from .views import *
from rest_framework import routers

route =routers.SimpleRouter()

route.register('register',UserRegister,basename='user')


route.register('parent',ParentUser,basename='marchand')
route.register('admin',AdminUser,basename='admin')

urlpatterns =[
    
    path('',include(route.urls)),
    
    path('login',UserLogin.as_view(),name='login'),
    path('logout/<id>',Logout.as_view(),name='logout'),
]