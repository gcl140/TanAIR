from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)  # Include country code
    email = models.EmailField(unique=True, verbose_name="Official Email")
    email_verified = models.BooleanField(default=False)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)

    # Override username to use email as the unique identifier
    username = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} - {self.company}"

@property
def is_logistics_worker(self):
        # Check if the user has an associated LogisticsWorker record
        return hasattr(self, "logisticsworker")
    
# Coordinator account setup for the logistics manager
class Coordinator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="coordinator")

    def __str__(self):
        return f"Coordinator: {self.user.username}"