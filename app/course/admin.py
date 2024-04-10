from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'user']
    readonly_fields = ['user']


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'teacher']
    readonly_fields = ['teacher']


@admin.register(models.Cart)
class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    readonly_fields = ['user']
