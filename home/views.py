from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Person
from .serializers import PeopleSerializer

# Create your views here.

def new(request):
  return HttpResponse("Welcome to Django")


@api_view(['GET', 'POST', 'PUT'])
def index(request):
  # courses = {
  #   'course_name' : 'Python',
  #   'learn' : ['Django', 'Flask', 'FastApi', 'Tornado'],
  #   'course__provider' : 'Scaler'
  # }
  # if request.method == 'GET':
  #   print(request.GET.get("search"))
  #   print("You hit the GET method")
  #   return Response(courses)
  # elif request.method == 'POST':
  #   data = request.data
  #   print("-----------------------------")
  #   print(data)
  #   print("-----------------------------")
  #   print("You hit the POST method")
  #   return Response(courses)
  # elif request.method == 'PUT':
  #   print("You hit the PUT method")
  #   return Response(courses)

  if request.method == 'GET':
    json_response = {
      'name' : 'Python',
      'course' : ['Django', 'Flask'],
      'method' : 'GET'
    }
  else:
    data = request.data
    print(data)
    json_response = {
      'name' : 'JavaScript',
      'course' : ['Node', 'React'],
      'method' : 'POST'
    }
    return Response(json_response)
  

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def people(request):
  if request.method == 'GET':
    obj = Person.objects.all()
    serializer = PeopleSerializer(obj, many = True)
    return Response(serializer.data)
  
  elif request.method == 'POST':
    data = request.data
    serializer = PeopleSerializer(data = data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors)
  
  elif request.method == 'PUT':
    data = request.data
    serializer = PeopleSerializer(data = data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors)
  
  elif request.method == 'PATCH':
    data = request.data
    obj = Person.objects.get(id = data['id'])
    serializer = PeopleSerializer(obj, data = data, partial = True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
  
    return Response(serializer.errors)
  
  else:
    data = request.data
    obj = Person.objects.get(id = data['id'])
    obj.delete()
    return Response({'message': 'person deleted'})