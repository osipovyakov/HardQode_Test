from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserView
from api.views import LessonsViewSet, ProductViewSet, ProductsForUsersViewSet

router = DefaultRouter()
router.register(r'users', CustomUserView)
router.register(r'users/(?P<id>\d+)/products', ProductsForUsersViewSet)
router.register(r'lessons', LessonsViewSet)
router.register(r'products', ProductViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
