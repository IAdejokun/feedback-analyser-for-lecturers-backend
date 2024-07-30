from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """ 
    serializer for creating user
    password is write only after user is created
    override create method to create a user
    """
    class Meta:
        model = User
        fields = ['id', 'user_type', 'username', 'full_name', 'password', 'university_name', 'id_or_matricn_number']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            full_name = validated_data['full_name'],
            university_name = validated_data['university_name'],
            id_or_matricn_number = validated_data['id_or_matricn_number'],
            user_type = validated_data['user_type'],
            password = validated_data['password'],
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    """ 
    serializer for login
    user is validated only if credentials university_name, id_or_matricn_number, usertype and password are provided
    """
    university_name = serializers.CharField(max_length=80)
    id_or_matricn_number = serializers.CharField(max_length=80)
    user_type = serializers.ChoiceField(choices = User.USER_TYPE_CHOICES)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    
    def validate(self, attrs):
        university_name = attrs.get('university_name')
        id_or_matricn_number = attrs.get('id_or_matricn_number')
        user_type = attrs.get('user_type')
        password = attrs.get('password')
    
        if university_name and id_or_matricn_number and user_type and password:
            try:
                user = User.objects.get(
                university_name = university_name,
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
            msg = 'Must include university_name, id_or_matricn_number, user_type and password'
            raise serializers.ValidationError(msg, code='authorization')