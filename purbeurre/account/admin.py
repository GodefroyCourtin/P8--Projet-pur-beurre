"""Django administration module."""
from django.contrib import admin
from .models import My_user, Substitute

admin.site.register(My_user)
admin.site.register(Substitute)
