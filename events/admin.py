from django.contrib import admin
from .models import User, Event, Registration


# register models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser']


# register Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_time', 'location', 'max_participants', 'organizer')
    search_fields = ('name', 'description')
    list_filter = ('date_time', 'location')


# register Registration
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date_registered', 'status')
    search_fields = ('user__username', 'event__name')
    list_filter = ('status', 'date_registered')

