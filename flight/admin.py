from django.contrib import admin
from .models import CustomUser, Flight, Airport, Passenger, Profile

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "is_staff")

class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "flight_status")
    horizontal_filter = "flight"

class PassengerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Airport)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger)
admin.site.register(Profile)