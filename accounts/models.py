from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


ROLE_CHOICES = { 
        'vip' : 'vip',
        'regular' : 'regular',
        'dealership' : 'dealership',
    }
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=11)
    full_name = models.CharField(max_length=40)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='regular')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.email
    

