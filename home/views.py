from django.shortcuts import render
from .models import User
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.filters import SearchFilter


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserRegistrationSerializer
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid ():
            User.objects.create_user(
                username = serializer.validated_data['username'],
                email=serializer.validated_data['email'] ,
                password=serializer.validated_data['password']
            )
            return Response({"msg":"User Registrerd Succesfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    renderer_classes = [UserRenderer]
    def post(self,request,format=None): 
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg':'User Loggined Succesfully','token':token},status=status.HTTP_200_OK)
            return Response({'msg':'Login Failed','errors':{'non_field_errors':['Email or Password is not Valid']}},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    

class UserProfileEdit(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    renderer_classes = [UserRenderer]
    filter_backends = [SearchFilter]
    search_fields = ['^name','=email']

    def get(self,request):
        user = User.objects.all()
        serializer = UserProfileSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk=None):
        id = pk
        if id is not None:
            user = User.objects.get(pk=id)
            serializer = UserProfileSerializer(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Select a User'})
    def delete(self, request, pk=None):
        id=pk
        if id is not None:
            try:
                user = User.objects.get(pk=id)
            except User.DoesNotExist:
                return Response({"msg": "User Doesn't Exist!!!"}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
            return Response({"msg": "User Deleted!!!"}, status=status.HTTP_200_OK)
        return Response({'msg':'Select a User'})

    


