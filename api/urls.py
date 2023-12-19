from django.urls import path,include
from home.views import *


urlpatterns = [
  path('index/', index),
  path('people/', people),
  path('login/', login),
  path('persons/', PersonAPI.as_view()),
]