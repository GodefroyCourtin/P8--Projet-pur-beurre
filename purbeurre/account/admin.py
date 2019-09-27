from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import My_user, Substitute

admin.site.register(My_user)
admin.site.register(Substitute)

