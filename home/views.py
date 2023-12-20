from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Person
from .serializers import PeopleSerializer, LoginSerializer, RegistrationSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action

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
  


@api_view(['POST'])
def login(request):
  data = request.data
  serializer = LoginSerializer(data = data)

  if serializer.is_valid():
    data = serializer.validated_data
    print(data)
    return Response({'message': 'Login successful'})
  
  return Response(serializer.errors)


# APIView methods
class PersonAPI(APIView):

  permission_classes = [IsAuthenticated]
  authentication_classes = [TokenAuthentication]

  # GET request
  def get(self, request):
    try:     
      print(request.user)
      obj  = Person.objects.all()
      page = request.GET.get('page', 1)
      page_size  = 3
      paginator = Paginator(obj, page_size)
      serializer = PeopleSerializer(paginator.page(page), many=True)
      return Response(serializer.data)
    except Exception as e:
      return Response({'status': False, 'message':'Invalid pagination'})
  
  # POST request
  def post(self, request):
    data = request.data
    serializer = PeopleSerializer(data = data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors)
  
  # PUT request
  def put(self, request):
    data = request.data
    serializer = PeopleSerializer(data = data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors)

  # PATCH request
  def patch(self, request):
    data = request.data
    obj = Person.objects.get(id = data['id'])
    serializer = PeopleSerializer(obj, data = data, partial = True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors)

  # DELETE request
  def delete(self, request):
    data = request.data
    obj = Person.objects.get(id = data['id'])
    obj.delete()
    return Response({'message': 'person deleted'})


# Normal api_view
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def people(request):

  # GET request
  if request.method == 'GET':
    obj = Person.objects.filter(color__isnull=False)
    serializer = PeopleSerializer(obj, many = True)
    return Response(serializer.data)
  
  # POST request
  elif request.method == 'POST':
    data = request.data
    serializer = PeopleSerializer(data = data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors)
  
  # PUT request
  elif request.method == 'PUT':
    data = request.data
    serializer = PeopleSerializer(data = data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors)
  
  # PATCH request
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
  


# ModelViewSet
class PeopleViewSet(viewsets.ModelViewSet):

  serializer_class = PeopleSerializer
  queryset = Person.objects.all()

  def list(self, request):
    search = request.GET.get('search')
    queryset = self.queryset
    if search:
      queryset = queryset.filter(name__startswith=search)

    serializer = PeopleSerializer(queryset, many=True)
    
    return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)
  

  @action(detail=True, methods=['POST'])
  def send_mail_to_person(self, request):
    return Response({'status': True, 'message':'Email send Success'}, status=status.HTTP_200_OK)


# Resgisteration
class ResgisterAPI(APIView):

  def post(self, request):
    data = request.data
    serializer = RegistrationSerializer(data = data)

    if not serializer.is_valid():
      return Response({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()

    return Response({'status': True, 'message': 'User Created'}, status=status.HTTP_201_CREATED)
  


# Login
class LoginAPI(APIView):

  def post(self, request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if not serializer.is_valid():
      return Response({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    print(serializer.data)

    user = authenticate(username = serializer.data['username'], password = serializer.data['password'])

    if not user:
      return Response({'status': False, 'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    print(user)


    token,_ = Token.objects.get_or_create(user = user)

    return Response({'status': True, 'message': 'User Login', 'token': str(token)} , status=status.HTTP_201_CREATED)