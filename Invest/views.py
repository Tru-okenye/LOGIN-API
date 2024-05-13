from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer

@api_view(['GET','POST'])
def login(request):
    user = get_object_or_404(User, username= request.data['username'])
    if not user.check_password(request.data['password']):
         return Response({'details':'not found'}, status=status.HTTP_404_NOT_FOUND)
   
    serializer = UserSerializer(instance=user)
         
    return Response({ 'user':serializer.data})


@api_view(['GET', 'POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
           serializer.save()
           user = User.objects.get(username= request.data['username'])
           user.set_password(request.data['password'])
           user.save()
           token = Token.objects.create(user=user)
           return Response({'token': token.key, 'user':serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


