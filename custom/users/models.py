from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from .choices import USER_LOGIN_TYPE

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    name = models.CharField(blank=False, null=False, max_length=150)
    userType = models.CharField(max_length=50, choices=USER_LOGIN_TYPE, default="Candidate")
    
    def __str__(self):
        return self.email