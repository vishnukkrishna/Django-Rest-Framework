from django.urls import path,include
from home.views import *


urlpatterns = [
  path('index/', index),
  path('people/', people)
]