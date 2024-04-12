from .models import Event, Registration
from .serializers import EventSerializer, UserRegistrationSerializer, RegistrationSerializer
from rest_framework import status, views, viewsets, permissions
from rest_framework.response import Response


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