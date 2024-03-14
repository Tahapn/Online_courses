from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet
from . import serializers
from . import models


class CoursesViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()
