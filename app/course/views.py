from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import serializers
from . import models


class CoursesViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()


class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user.id
        queryset = models.Teacher.objects.get(user=user)
        serializer = serializers.TeacherSerializer(queryset)
        return Response(serializer.data)
