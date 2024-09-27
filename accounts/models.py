

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        user = self.model(phone_number=phone_number)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
