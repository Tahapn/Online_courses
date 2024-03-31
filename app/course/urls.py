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
router.register('carts', views.CartViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

cartitem_route = routers.NestedSimpleRouter(router, 'carts', lookup='cart')
cartitem_route.register('items', views.CartItemViewSet, basename='cart-items')

course_file_route = routers.NestedSimpleRouter(
    router, 'teacher-courses', lookup='course')
course_file_route.register(
    'files', views.CourseFileViewSet, basename='course-files')

urlpatterns = [
    path('teacher-profile/', views.TeacherProfileView.as_view())
] + router.urls + cartitem_route.urls + course_file_route.urls
