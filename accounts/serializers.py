from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only':True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match!')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exists.')
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ),
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid username or password.')