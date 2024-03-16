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
