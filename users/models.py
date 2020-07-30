from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUser(AbstractUser):
    role_list = [("FA", "Financial advisor"), ("Cust", "Customer")]
    Role = models.CharField(max_length=50, choices=role_list)
    cell_phone = models.CharField(max_length=50, default=' ', null=True, blank=True)
    is_staff = models.BooleanField(default=True)
    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
