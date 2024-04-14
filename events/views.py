from rest_framework.views import APIView
from .models import Event, Registration
from .serializers import EventSerializer, UserRegistrationSerializer, RegistrationSerializer
from rest_framework import status, views, viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logger.debug(f"Request data: {request.data}")
        logger.debug(f"Is user authenticated: {request.user.is_authenticated}")
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        logger.debug("Listing all events")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        logger.debug(f"Retrieving event with id: {pk}")
        return super().retrieve(request, pk, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        logger.debug(f"Updating event with id: {pk} with data: {request.data}")
        return super().update(request, pk, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        logger.debug(f"Deleting event with id: {pk}")
        return super().destroy(request, pk, *args, **kwargs)


class UserRegistrationView(views.APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        serializer = RegistrationSerializer(data={
            'user': request.user.id,
            'event': event_id,
            'status': 'active'
        }, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, registration_id):
        try:
            registration = Registration.objects.get(id=registration_id, user=request.user)
            registration.status = 'cancelled'
            registration.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Registration.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
