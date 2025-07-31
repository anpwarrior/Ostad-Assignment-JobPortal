from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('applicant', 'Applicant'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)