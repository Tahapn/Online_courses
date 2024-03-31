'''
Serializers for course app
'''

from django.db import transaction
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


class CourseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseFiles
        fields = ['id', 'title', 'file', 'course']
        extra_kwargs = {
            'course': {'read_only': True}
        }

    def create(self, validated_data):
        course = self.context['course']
        return models.CourseFiles.objects.create(course_id=course, **validated_data)


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

    def validate_course(self, course):

        orders = models.Order.objects.filter(user=self.context['user'])

        # checks if user already owns the course
        for item in orders:
            if item.orderitems.filter(course=course).exists():
                raise serializers.ValidationError(
                    'You already own this course.')

        # checks if user already has the course in the cart
        if models.CartItem.objects.filter(cart=self.context['cart'], course=course).exists():
            raise serializers.ValidationError('Course is already in cart')

        else:
            return course

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
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')


class OrderItemSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['id', 'course', 'price']


class OrderGETserializer(serializers.ModelSerializer):
    '''
    Serializer for GET requests. (orderendpoint)
    '''
    class Meta:
        model = models.Order
        fields = ['id', 'created_at', 'orderitems']

    orderitems = OrderItemSerilizer(many=True)


class OrderPOSTSerializer(serializers.Serializer):
    '''
    Serializer for POST requests. (order endpoint)
    '''
    cart = serializers.UUIDField()

    def validate_cart(self, cart_id):
        try:
            cart = models.Cart.objects.get(pk=cart_id)
            if models.CartItem.objects.filter(cart=cart).count() == 0:
                raise serializers.ValidationError('Empty Cart!!')
            return cart_id  # Return the valid cart_id UUID
        except models.Cart.DoesNotExist:
            raise serializers.ValidationError('No cart with this ID')

    def save(self, **kwargs):
        with transaction.atomic():
            # create an order
            order = models.Order.objects.create(user=self.context['user'])

            cart_id = self.validated_data['cart']

            cart_items = models.CartItem.objects.filter(
                cart_id=cart_id)
            order_items = [
                models.OrderItem(
                    order=order,
                    price=item.course.price,
                    course=item.course,)
                for item in cart_items
            ]
            # save all order items
            models.OrderItem.objects.bulk_create(order_items)

            # delete the cart
            models.Cart.objects.filter(pk=cart_id).delete()
