from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from accountapp.managers import CustomUserManager

ROLE_SELECTION = [
    ('JUNIOR', 'Junior'),
    ('SENIOR', 'Senior'),
    ('STAFF', 'Staff')
]


class User(AbstractUser):
    username = None
    email = models.EmailField('email_address', unique=True)
    objects = CustomUserManager()

    # SoriDam Custom
    role = models.CharField(max_length=20, choices=ROLE_SELECTION)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email