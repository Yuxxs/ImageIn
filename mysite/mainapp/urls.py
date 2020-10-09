from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import *
from mainapp import views


urlpatterns = [

   path('', views.mainpage, name='mainpage'),
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path("register/", views.register, name="register"),
]
