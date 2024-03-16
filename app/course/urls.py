'''
urls for course app 
'''
from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()

router.register('courses', views.CoursesViewSet)
router.register('teacher-courses', views.TeacherCoursesViewSet,
                basename='teacher')

urlpatterns = [
    path('teacher-profile', views.TeacherProfileView.as_view())
] + router.urls
