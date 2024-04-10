from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'last_login', 'is_staff',
              'is_active', 'groups', 'user_permissions', 'date_joined',]
