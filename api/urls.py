from django.urls import path, include
from book.views import * 

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('books/', BookListCreateView.as_view(), name='book-list-view'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail')
]
