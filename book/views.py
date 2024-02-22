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
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny 
from rest_framework.pagination import LimitOffsetPagination



class RegisterAPI(APIView):
    """
    This API endpoint allows clients to register new users by sending a POST request
    with user registration data. Upon successful registration, a new user is created
    and a success message is returned.
    
    """
    permission_classes = [AllowAny]  # Allow any user to access this view
    def post(self, request):
        _data = request.data
        serializer = RegisterSerializer(data = _data)
        
        if not serializer.is_valid():
            return Response({'message':serializer.errors})
        
        serializer.save()
        
        return Response({'message':'User Created'})
 
    
class LoginAPI(APIView):
    """
    This API endpoint allows clients to authenticate users by sending a POST request
    with user login credentials. Upon successful authentication, a token is generated
    and returned to the client, allowing access to authenticated endpoints.
    
    """
    permission_classes = [AllowAny] # Allow any user to access this view
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

# class setPagination(PageNumberPagination):
#     """
#     limit the number of items per page
    
#     """
#     page_size = 2
    

@method_decorator(cache_page(60 * 60 * 2), name='dispatch') # Cache the response for 2 hours
@permission_classes([IsAuthenticated])
class BookListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating books.

    This API endpoint allows authenticated users to list and create books.
    The response is cached for 2 hours to improve performance.

    Permissions:
        - The user must be authenticated to access this endpoint.
    Pagination:
        - Allow the client to request a specific page and limit the number of items per page
          using limit and offset.
    """    
    
    queryset = Book.objects.prefetch_related()
    serializer_class = BookSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10  
    pagination_class.limit_query_param = 'limit'  
    pagination_class.offset_query_param = 'offset'  
    
    def get(self, request):
        queryset = Book.objects.all()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = BookSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    
    

@permission_classes([IsAuthenticated])       
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a book.

    This API endpoint allows authenticated users to retrieve, update, and delete
    a specific book identified by its ID.

    Permissions:
        - The user must be authenticated to access this endpoint..
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    

    

   