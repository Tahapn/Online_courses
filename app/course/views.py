from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from .permissions import IsTeacher
from . import serializers
from . import models


class CoursesViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()


class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user.id
        teacher = get_object_or_404(models.Teacher, user=user)
        serializer = serializers.TeacherSerializer(teacher)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = serializers.TeacherSerializer(
                data=request.data, context=self.get_serializer_context(request))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        except IntegrityError:
            return Response('Teacher profile already exists. no need to send post request', status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        teacher = get_object_or_404(models.Teacher, user=self.request.user.id)
        serializer = serializers.TeacherSerializer(
            teacher, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def get_serializer_context(self, request):
        return {'user': self.request.user.id}


class TeacherCoursesViewSet(ModelViewSet):

    def get_queryset(self):
        teacher = models.Teacher.objects.get(user=self.request.user.id)
        return models.Course.objects.filter(teacher=teacher)

    def get_serializer_context(self):
        teacher = models.Teacher.objects.get(user=self.request.user.id)
        return {'teacher': teacher}

    serializer_class = serializers.CourseSerializer

    permission_classes = [IsTeacher]


class CartViewSet(RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer


class CartItemViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):

    def get_queryset(self):
        return models.CartItem.objects.filter(cart=self.kwargs['cart_pk'])

    def get_serializer_context(self):

        return {'cart': self.kwargs['cart_pk']}

    serializer_class = serializers.CartItemSerializer


class OrderViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user.id)

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.OrderPOSTSerializer
        else:
            return serializers.OrderGETserializer

    permission_classes = [IsAuthenticated]
