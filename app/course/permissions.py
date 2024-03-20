from rest_framework.permissions import BasePermission
from . import models


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        has_teacher_record = models.Teacher.objects.filter(
            user=request.user.id).exists()

        if request.user.is_authenticated and has_teacher_record:
            return True
        return False
