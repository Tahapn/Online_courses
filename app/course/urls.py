'''
urls for course app 
'''
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()

router.register('courses', views.CoursesViewSet)

urlpatterns = [] + router.urls
