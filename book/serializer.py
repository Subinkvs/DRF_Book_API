from rest_framework import serializers
from django.contrib.auth.models import User
from book.models import Book


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    This serializer validates and handles the registration of new users.
    
    """
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        """
        Validate method to check if the username and email provided are unique.
        
        """
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username already exists")
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("Email already exists")
        
        return data
    
    def create(self, validated_data):
        """
        Method to create and save a new user instance using the provided validated data.
        
        """
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    This serializer handles the validation of user login credentials.
    
    """
    username = serializers.CharField()
    password = serializers.CharField()
    
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    This serializer serializes Book model instances into JSON representations and vice versa.
    
    """
    class Meta:
        model = Book
        fields = '__all__'