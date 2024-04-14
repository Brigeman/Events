from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserRegistrationView, EventRegisterView, EventCancelView


router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('events/register/<int:event_id>/', EventRegisterView.as_view(), name='event-register'),
    path('events/cancel/<int:registration_id>/', EventCancelView.as_view(), name='event-cancel'),

]

