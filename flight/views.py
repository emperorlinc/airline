from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Airport, CustomUser, Flight, Flight, Passenger, Profile
from .forms import AirportForm, CustomUserForm, PassengerForm, FlightForm, FlightForm
from django.shortcuts import render, redirect
from .decorators import restriction
from django.contrib import messages

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html")

@restriction
def register_view(request, *args, **kwargs):
    form = CustomUserForm()
    if request.method == "POST":

        form = CustomUserForm(request.POST, request.FILES)

        if form.is_valid():

            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")
            photo = form.cleaned_data.get("phote")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
        
            if password != confirm_password:
                messages.error(request, "ERROR: Your password didn't match.")
                return redirect("register")
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "ERROR: Email already taken.")
                return redirect("register")
            elif CustomUser.objects.filter(phone=phone).exists():
                messages.error(request, "ERROR: Phone number already used.")
                return redirect("register")
            else:
                user = CustomUser.objects.create_user(name=name, email=email, phone=phone, password=password, photo=photo)
                user.save()
                login(request, user)
                messages.success(request, "Registration successful...")
                return redirect("home")
    # if request.method == "POST":
    #     name = request.POST["name"]
    #     email = request.POST["email"]
    #     phone = request.POST["phone"]
    #     password = request.POST["password"]
    #     confirm_password = request.POST["confirm_password"]
    #     # photo = request.POST["photo"]
    #     if password != confirm_password:
    #         messages.error(request, "Password did not match...")
    #         return redirect("register")
    #     elif CustomUser.objects.filter(email=email).exists():
    #         messages.info(request, "Email already taken...")
    #         return redirect("register")
    #     elif CustomUser.objects.filter(phone=phone).exists():
    #         messages.info(request, "Phone number already taken...")
    #         return redirect("register")
    #     else:
    #         user = CustomUser.objects.create_user(name=name, email=email, phone=phone, password=password)
    #         user.save()
    #         login(request, user)
    #         messages.success(request, "Registration successful...")
    #         return redirect("home")
    return render(request, "register.html", { "form": form })

@restriction
def login_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, "User does not have an account with us...")
            return redirect("login")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful...")
            return redirect("home")
        else:
            messages.error(request, "User is None(AnonymousUser)...")
            return redirect("login")
    return render(request, "login.html")

@login_required(login_url="login")
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.success(request, "Logged Out...")
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
    passengers = Passenger.objects.filter(origin=flight.origin, destination=flight.destination)
    context = { "passengers": passengers, "flight": flight }
    return render(request, "passenger.html", context)

@login_required(login_url="login")
def untracked_flight_view(request, *args, **kwargs):
    flights = Flight.objects.filter(flight_status=None)
    context = { "flights": flights }
    return render(request, "untracked_flight.html", context)

@login_required(login_url="login")
def update_flight_view(request, pk, *args, **kwargs):
    data = Flight.objects.get(id=pk)
    form = FlightForm(instance=data)
    if request.method == "POST":
        form = FlightForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Flight track successfully...")
            return redirect("home")
        else:
            messages.error(request, "Flight track was not successful...")
            return redirect("update-flight")
    context = { "form": form }
    return render(request, "update_flight.html", context)

@login_required(login_url="login")
def add_airport(request, *args, **kwargs):
    form = AirportForm()
    if request.method == "POST":
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added new Airport...")
            return redirect("add-airport")
        else:
            messages.error(request, "Invalid Form Entry...")
            return redirect("add-airport")
    context = { "form": form }
    return render(request, "create_airport.html", context)

@login_required(login_url="login")
def booking_view(request, *args, **kwargs):
    form = PassengerForm()
    if request.method == "POST":
        form = PassengerForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            flight = Flight.objects.create(origin=user.origin, destination=user.destination)
            flight.save()
            messages.success(request, "Flight Booked successfully...")
            return redirect("home")
        else:
            messages.error(request, "Invalid Form Entry...")
            return redirect("book-flight")
    context = { "form": form }
    return render(request, "book_flight.html", context)

@login_required(login_url="login")
def profile_view(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    context = { "profile": profile }
    return render(request, "profile.html", context)