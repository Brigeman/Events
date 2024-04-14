from rest_framework import serializers
from .models import Event, Registration
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


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
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date_time', 'location', 'organizer', 'created_by', 'max_participants']
        read_only_fields = ['id', 'organizer', 'created_by']

    def create(self, validated_data):
        logger.debug(f"Received data: {validated_data}")
        logger.debug(f"Context user: {self.context['request'].user if 'request' in self.context else 'No user context'}")
        if self.context['request'].user.is_authenticated:
            validated_data['organizer'] = validated_data.get('organizer', self.context['request'].user)
            validated_data['created_by'] = validated_data.get('created_by', self.context['request'].user)
            event = super().create(validated_data)
            logger.debug(f"Event created: {event}")
            return event
        else:
            raise serializers.ValidationError("User must be authenticated to create event")
