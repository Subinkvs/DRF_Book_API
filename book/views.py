from django.shortcuts import render
from rest_framework.response import Response
from book.serializer import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from book.models import Book
from rest_framework import generics
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RegisterAPI(APIView):
    def post(self, request):
        _data = request.data
        serializer = RegisterSerializer(data = _data)
        
        if not serializer.is_valid():
            return Response({'message':serializer.errors})
        
        serializer.save()
        
        return Response({'message':'User Created'})
    
class LoginAPI(APIView):
    def post(self, request):
        _data = request.data
        serializer = LoginSerializer(data = _data)
        
        if not serializer.is_valid():
            return Response({'message':serializer.errors})
        
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        
        if not user:
            return Response({'message':"Invalid"})
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({'message':'Login successfull', 'token':str(token)})


@method_decorator(cache_page(60 * 60 * 2), name='dispatch') # Cache the response for 2 hours
@permission_classes([IsAuthenticated])
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.prefetch_related()
    serializer_class = BookSerializer

@permission_classes([IsAuthenticated])       
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer