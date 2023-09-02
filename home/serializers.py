from rest_framework.fields import empty
from rest_framework_simplejwt.tokens import Token
from .models import User
from rest_framework import serializers
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    profile_picture = serializers.FileField(required=False)
    class Meta:
        model = User
        fields = ['name','email','password','profile_picture','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
  
    
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        name = data.get('name')
        if password != password2 :
            raise serializers.ValidationError('password doesnot match')
        elif re.match(r"^\d{1,3}", name):   
            raise serializers.ValidationError('Name should Start with Alphabets')
        return data
     

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
        
        
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','profile_picture']    
         
    

class ProfileCRUDSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = User
        fields = ['id','name','email','profile_picture']

