'''
Serializers for course app
'''


from rest_framework import serializers
from . import models


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'title', 'description', 'teacher', 'price']
        extra_kwargs = {
            'teacher': {'read_only': True}
        }

    def create(self, validated_data):
        teacher = self.context['teacher']
        return models.Course.objects.create(teacher=teacher, **validated_data)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['id', 'first_name', 'last_name',]

    def create(self, validated_data):
        user = self.context['user']
        return models.Teacher.objects.create(user_id=user, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['id', 'course', 'price']

    def create(self, validated_data):
        cart_id = self.context['cart']
        return models.CartItem.objects.create(cart_id=cart_id, **validated_data)

    # each course price
    def get_price(self, obj: models.CartItem):
        return obj.course.price

    price = serializers.SerializerMethodField('get_price', read_only=True)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price']

    # sum of all courses in a cart
    def get_total_price(self, obj: models.CartItem):
        return sum([item.course.price for item in obj.items.all()])

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField('get_total_price')
