from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

# ======================================================================================================
# THE CUSTOM USER MODEL MANAGER.
# ======================================================================================================

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, phone, photo, password=None):
        if not email:
            raise ValueError("User must have an email.")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, phone=phone, photo=photo)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, name, email, phone, password):
        user = self.create_user(name, email, phone, password)
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone, password):
        user = self.create_user(name, email, phone, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# ======================================================================================================
# THE CUSTOM USER THAT ALLOWS TO ADD MORE FIELDS THAN THE DEFAULT.
# ======================================================================================================

class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=64)
    photo = models.ImageField(upload_to="profile", default=None)
    email = models.EmailField(unique=True, max_length=64)
    phone = models.CharField(max_length=14)
    password = models.CharField(max_length=16)
    confirm_password = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    class Meta:
        ordering = ["-created", "-updated"]

    def get_first_name(self):
        _name = self.name.split(" ")
        first_name = _name[0]
        return first_name

    def __str__(self):
        return self.get_first_name()

# ======================================================================================================
# THE PROFILE MODEL HANDLER FOR THE USER.
# ======================================================================================================

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=14)
    photo = models.ImageField()

    def __str__(self):
        return self.name


# ======================================================================================================
# THE DATA THAT CONCERNS THE STAFF ONLY.
# ======================================================================================================

class Airport(models.Model):
    """AIRPORT FIELDS THAT THE STAFFS WILL FILL TO MAKE THE DATAS AVAILABLE FOR THE USERS CONVINENCE"""
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{ self.name }({ self.code }) of { self.city }"

FLIGHT_STATUS = (
    ("P", "Pending"),
    ("D", "Departed"),
    ("A", "Arrived"),
    ("C", "Cancelled"),
)

class Flight(models.Model):
    """FLIGHT FIELDS THAT THE STAFFS WILL FILL TO MAKE THE DATAS AVAILABLE FOR THE USERS CONVINENCE"""
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="initial")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="final")
    duration = models.IntegerField(blank=True, null=True)
    flight_status = models.CharField(choices=FLIGHT_STATUS, max_length=1, blank=True, null=True)

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

class Passenger(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departure")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrival")
    # flight = models.ManyToManyField(Flight, blank=True, related_name="passenger")
    flight_class = models.CharField(choices=FLIGHT_TYPE, max_length=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
