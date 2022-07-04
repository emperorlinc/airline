from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser, Profile

# Create your signals here.
@receiver(post_save, sender=CustomUser)
def create_profile(sender, created, instance, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            name=user.name,
            email=user.email,
            phone=user.phone
        )