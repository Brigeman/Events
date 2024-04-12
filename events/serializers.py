from rest_framework import serializers
from .models import Event, Registration
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'date_registered', 'status']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date_time', 'location', 'organizer', 'max_participants']

