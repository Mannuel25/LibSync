import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(style={"input_type": 'password'})

    def validate(self, data):
        email, password = data.get('email').lower(), data.get('password')
        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                data['user'] = user
            else: raise serializers.ValidationError('Invalid email or password')
        else: raise serializers.ValidationError('Enter a valid email and password')
        return data


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=500, required=True)

    def create(self, validated_data):
        refresh = validated_data.get('refresh_token')
        try:
            # generate a new access token using the refresh token
            refresh_token = RefreshToken(refresh)
            access_token = str(refresh_token.access_token)
            return access_token
        except Exception as e:
            raise Exception(str(e))


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(style={"input_type": 'password'}, required=True)

    def validate(self, data):
        password = data.get('password')
        try:
            validators.validate_password(password=password)
        except Exception as e:
            msg_error = eval(str(e))[0]
            raise Exception(msg_error)
        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['date_joined', 'groups', 'user_permissions', 'last_login', 'is_active', 'is_superuser']


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class BorrowedBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowedBook
        fields = '__all__'


