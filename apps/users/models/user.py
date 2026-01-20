from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    role = models.CharField(max_length=30, default=False)
    is_deleted = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
