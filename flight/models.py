from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError("User must have an email.")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, name, email, password):
        user = self.create_user(name, email, password)
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=64)
    name = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        ordering = ["-created", "-updated"]

    def get_first_name(self):
        _name = self.name.split(" ")
        first_name = _name[0]
        return first_name

    def __str__(self):
        return self.get_first_name()


# ======================================================================================================
# THE DATA THAT CONCERNS THE STAFF ONLY.
# ======================================================================================================

FLIGHT_STATUS = (
    ("P", "Pending"),
    ("D", "Departed"),
    ("A", "Arrived"),
    ("C", "Cancelled"),
)


class StaffAirport(models.Model):
    """AIRPORT FEILDS THAT THE STAFFS WILL FILL TO MAKE THE DATAS AVAILABLE FOR THE USERS CONVINENCE"""
    city = models.CharField(max_length=64)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.city}({self.code})"


class StaffFlight(models.Model):
    """FLIGHT FEILDS THAT THE STAFFS WILL FILL TO MAKE THE DATAS AVAILABLE FOR THE USERS CONVINENCE"""
    origin = models.ForeignKey(StaffAirport, on_delete=models.CASCADE, related_name="departure")
    destination = models.ForeignKey(StaffAirport, on_delete=models.CASCADE, related_name="arrival")
    duration = models.IntegerField()
    flight_status = models.CharField(choices=FLIGHT_STATUS, max_length=1)

    def __str__(self):
        return f"Flight { self.id }: From { self.origin } to { self.destination }"

# ======================================================================================================
# THE DATA THAT CONCERNS THE USERS ALONE.
# ======================================================================================================

FLIGHT_TYPE = (
    ("B", "Business"),
    ("F", "First Class"),
    ("E", "Economy"),
    ("BE", "Business Economy"),
)


class Flight(models.Model):
    """FLIGHT FEILDS THAT THE STAFFS WILL FILL TO MAKE THE DATAS AVAILABLE FOR THE USERS CONVINENCE"""
    origin = models.ForeignKey(StaffAirport, on_delete=models.CASCADE, related_name="departure")
    destination = models.ForeignKey(StaffAirport, on_delete=models.CASCADE, related_name="arrival")

    def __str__(self):
        return f"From {self.origin} to {self.destination}"


class Passenger(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=64, blank=True, null=True, unique=True)
    photo = models.ImageField()
    mobile_number = models.CharField(max_length=16, unique=True)
    flight = models.ManyToManyField(Flight, blank=True, related_name="passenger")
    flight_type = models.CharField(choices=FLIGHT_TYPE, max_length=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
