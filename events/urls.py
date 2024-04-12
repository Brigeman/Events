from django.urls import path
from .views import EventSerializer

urlpatterns = [
    path('events/', EventSerializer.as_view()),
]