from .models import Event, Registration
from .serializers import EventSerializer, UserRegistrationSerializer, RegistrationSerializer
from rest_framework import status, views, viewsets, permissions
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        logger.debug(f"Creating event with data: {request.data}")
        return super().create(request, *args, **kwargs)

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


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UserRegistrationView(views.APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRegistrationView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        serializer = RegistrationSerializer(data={
            'user': request.user.id,
            'event': event_id,
            'status': 'active'
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, registration_id):
        registration = Registration.objects.get(id=registration_id, user=request.user)
        registration.status = 'cancelled'
        registration.save()
        return Response(status=status.HTTP_204_NO_CONTENT)








