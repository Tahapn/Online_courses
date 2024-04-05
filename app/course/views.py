from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsTeacher
from .filters import PriceFilter
from . import serializers
from . import models


class CoursesViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PriceFilter
    search_fields = ['title', 'description']


class TeacherProfileView(APIView):

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsTeacher]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super(TeacherProfileView, self).get_permissions()

    def get(self, request):
        teacher = get_object_or_404(models.Teacher, user=self.request.user.id)
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
        teacher = models.Teacher.objects.get(user=self.request.user)
        serializer = serializers.TeacherSerializer(
            teacher, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request):
        teacher = models.Teacher.objects.get(user=self.request.user)
        if teacher.course_set.count() > 0:
            return Response({'error': 'you have some courses. you can\'t delete your profile!!'})
        else:
            teacher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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


class CourseFileViewSet(ModelViewSet):

    def get_queryset(self):
        return models.CourseFiles.objects.filter(course=self.kwargs['course_pk'])

    def get_serializer_context(self):
        return {'course': self.kwargs['course_pk']}

    serializer_class = serializers.CourseFileSerializer

    permission_classes = [IsTeacher]


class CartViewSet(RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer


class CartItemViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):

    def get_queryset(self):
        return models.CartItem.objects.filter(cart=self.kwargs['cart_pk'])

    def get_serializer_context(self):

        return {'cart': self.kwargs['cart_pk'], 'user': self.request.user}

    serializer_class = serializers.CartItemSerializer


class OrderViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    def get_queryset(self):
        return models.Order.objects \
            .prefetch_related('orderitems', 'orderitems__course', 'orderitems__course__files') \
            .filter(user=self.request.user.id)

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.OrderPOSTSerializer
        else:
            return serializers.OrderGETserializer

    permission_classes = [IsAuthenticated]
