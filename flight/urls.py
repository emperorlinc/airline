from django.urls import path
from . import views

# Create your urlpatterns here.
urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    path("flight/", views.flight_view, name="flight"),
    path("client/", views.clients_view, name="client"),
    path("client/<str:pk>/", views.client_detail_view, name="client_detail"),
    path("passenger/<str:pk>/", views.passenger_view, name="passenger"),

    path("booking/", views.create_flight_view, name="create-flight"),
    path("add_airport/", views.add_airport, name="add-airport"),
    path("book_flight/", views.booking_view, name="book-flight"),
    path("profile/", views.profile_view, name="profile"),
]
