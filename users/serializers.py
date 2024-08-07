from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.password_validation import validate_password

class UniversitiesSerializer(serializers.ModelSerializer):
    """ 
    serializer for creating universities
    """
    class Meta:
        model = Universities
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    """ 
    serializer for creating user,
    password is write only after user is created,
    override create method to create a user
    """
    
    university = serializers.PrimaryKeyRelatedField(queryset=Universities.objects.all())
    class Meta:
        model = User
        fields = ['id', 'user_type', 'username', 'full_name', 'password', 'university', 'id_or_matricn_number']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            full_name = validated_data['full_name'],
            university = validated_data['university'],
            id_or_matricn_number = validated_data['id_or_matricn_number'],
            user_type = validated_data['user_type'],
            password = validated_data['password'],
        )
        return user
   
    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
 
    
class LoginSerializer(serializers.Serializer):
    """ 
    serializer for login
    user is validated only if credentials id_or_matricn_number, usertype and password are provided
    """
    
    id_or_matricn_number = serializers.CharField(max_length=80)
    user_type = serializers.ChoiceField(choices = User.USER_TYPE_CHOICES)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    
    def validate(self, attrs):
        id_or_matricn_number = attrs.get('id_or_matricn_number')
        user_type = attrs.get('user_type')
        password = attrs.get('password')
    
        if id_or_matricn_number and user_type and password:
            try:
                user = User.objects.get(
                id_or_matricn_number = id_or_matricn_number,
                user_type = user_type
             )
                if user.check_password(password):
                    attrs['user'] = user
                    return attrs
                else:
                    msg = 'Unable to login with provided credentials'
                    raise serializers.ValidationError(msg, code='authorization')
            except User.DoesNotExist:
                msg = 'User with provided credentials does not exist'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include id_or_matricn_number, user_type and password'
            raise serializers.ValidationError(msg, code='authorization')
        
class UniversityListSerializer(serializers.ModelSerializer):
    """ 
    serializer for university list
    """
    class Meta:
        model = Universities
        fields = ['id', 'name']

class UserUpdatesSerializer(UserSerializer):
    """
    for updating username and password
    """
    class Meta(UserSerializer.Meta):
        """ 
        override the fields to allow updating username and password
        """
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False},
            'full_name': {'required': False},
            'user_type': {'required': False},
            'university': {'required': False},
            'id_or_matricn_number': {'required': False},
        }
    def validate_password(self, value):
        if value:
            validate_password(value)
        return value