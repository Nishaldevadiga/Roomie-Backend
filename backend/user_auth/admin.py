from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Booking, UserProfile

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(UserProfile)
