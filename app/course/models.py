from django.db import models
from django.conf import settings
# Create your models here.


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    teacher = models.OneToOneField(Teacher, on_delete=models.PROTECT)
