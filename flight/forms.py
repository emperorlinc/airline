from django import forms
from .models import Airport, Flight, Passenger, Profile

# Create your forms here.
class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = "__all__"

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = "__all__"

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = "__all__"
        exclude = ("user",)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ("user",)