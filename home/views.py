from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

def new(request):
  return HttpResponse("Welcome to Django")


@api_view(['GET'])
def index(request):
  courses = {
    'course_name' : 'Python',
    'learn' : ['Django', 'Flask', 'FastApi', 'Tornado'],
    'course__provider' : 'Scaler'
  }
  return Response(courses)