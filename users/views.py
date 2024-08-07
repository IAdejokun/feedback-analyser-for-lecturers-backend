from  rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import mixins, viewsets
from django.contrib.auth import authenticate
from .serializers import *
from .models import *


class RegisterUserView(generics.CreateAPIView):
    """ 
    Register a new user 
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context = self.get_serializer_context()).data,
            "message": 'User created successfully'
        })

class LoginUserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_type': user.user_type,
            'user_id': user.id,
            'id_or_matricn_number': user.id_or_matricn_number
        })

class LogoutUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'message': 'User logged out successfully'
        })

#list all universities
class UniversityListView(generics.ListAPIView):
    queryset = Universities.objects.all()
    serializer_class = UniversityListSerializer
    permission_classes = [AllowAny]

class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class UpdateUserViewsSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdatesSerializer
    
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serialiser = self.get_serializer(instance, data=request.data, partial=partial)
        serialiser.is_valid(raise_exception=True)
        self.perform_update(serialiser)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            
        return Response(serialiser.data)

    
        
