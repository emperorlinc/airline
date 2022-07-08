from django import forms
from .models import Airport, Flight, Passenger, Profile

# Create your forms here.
class CustomUserForm(forms.Form):
    name = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=64)
    phone = forms.CharField(max_length=14)
    photo = forms.ImageField()
    password = forms.CharField(min_length=8, max_length=16, widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=8, max_length=16, widget=forms.PasswordInput)
    

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