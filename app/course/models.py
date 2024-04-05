from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
# Create your models here.


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField(validators=[MinValueValidator(1000)])
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)


class CourseFiles(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='files')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='files')


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ['cart', 'course'],
        ]


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderitems')
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
