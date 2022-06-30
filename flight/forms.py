from django import forms
from .models import Flight, Passenger

# Create your forms here.

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ["origin", "destination"]

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = "__all__"
        exclude = ("user", "name", "email",)