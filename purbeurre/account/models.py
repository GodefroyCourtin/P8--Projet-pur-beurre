from django.db import models
from django.contrib.auth.models import AbstractUser


class My_user(AbstractUser):
    saved = models.ManyToManyField('search.Product', through='Substitute', through_fields=('myuser', 'product_initial'))

class Substitute(models.Model):
    myuser = models.ForeignKey(My_user, on_delete=models.CASCADE)
    product_initial = models.ForeignKey('search.Product', on_delete=models.CASCADE, related_name='product_initial')
    product_substitute = models.ForeignKey('search.Product', on_delete=models.CASCADE, related_name='product_substitue')
   