from rest_framework.permissions import BasePermission
from . import models


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        query_set = models.Teacher.objects.filter(
            user=request.user.id).exists()

        if request.user.is_authenticated and query_set:
            return True
        return False
