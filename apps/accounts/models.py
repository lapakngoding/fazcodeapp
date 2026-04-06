from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    # Role sederhana namun powerful
    class Role(models.TextChoices):
        SUPERADMIN = "SUPERADMIN", "Super Admin"
        ADMIN = "ADMIN", "Administrator"
        OPERATOR = "OPERATOR", "Operator"
        USER = "USER", "Regular User"

    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.USER
    )
    
    def is_admin(self):
        return self.role in [self.Role.SUPERADMIN, self.Role.ADMIN]

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    def is_valid(self):
        # Link valid jika sudah diapprove dan belum lewat 1 jam
        if self.approved_at:
            return timezone.now() < self.approved_at + timedelta(hours=1)
        return False

    def __str__(self):
        return f"Reset {self.user.email} - {self.is_processed}"
