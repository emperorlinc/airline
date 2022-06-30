from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import StaffAirport, CustomUser, StaffFlight, Flight, Passenger
from .forms import AirportForm, PassengerForm
from django.shortcuts import render, redirect
from .decorators import restriction
from django.contrib import messages

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html")

@restriction
def register_view(request, *args, **kwargs):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password != confirm_password:
            messages.error(request, "Password did not match.")
            return redirect("register")
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request, "Email already taken.")
            return redirect("register")
        else:
            user = CustomUser.objects.create_user(name=name, email=email, password=password)
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
    return render(request, "register.html")

@restriction
def login_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, "User does not have an account with us.")
            return redirect("login")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "User is None(AnonymousUser).")
            return redirect("login")
    return render(request, "login.html")

@login_required(login_url="login")
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("home")

@login_required(login_url="login")
def flight_view(request, *args, **kwargs):
    flights = Flight.objects.all()
    context = {"flights": flights}
    return render(request, "flight.html", context)

@login_required(login_url="login")
def clients_view(request, *args, **kwargs):
    clients = Passenger.objects.all()
    context = { "clients": clients }
    return render(request, "client.html", context)

@login_required(login_url="login")
def client_detail_view(request, pk, *args, **kwargs):
    clients = Passenger.objects.get(id=pk)
    flights = clients.flight.all()
    context = { "clients": clients, "flights": flights }
    return render(request, "client_detail.html", context)

@login_required(login_url="login")
def passenger_view(request, pk, *args, **kwargs):
    flight = Flight.objects.get(id=pk)
    passengers = flight.passenger.all()
    context = { "passengers": passengers }
    return render(request, "passenger.html", context)

@login_required(login_url="login")
def create_flight_view(request, *args, **kwargs):
    form = FlightForm()
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()