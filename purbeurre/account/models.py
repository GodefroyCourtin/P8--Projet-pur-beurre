from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    street_number=models.IntegerField(null=True)
    street=models.CharField(max_length=500)
    postal_code=models.IntegerField(null=True)
    city=models.CharField(max_length=20)