from api.serializers import CustomUserSerializer
from djoser.views import UserViewSet
from .models import CustomUser


class CustomUserView(UserViewSet):
    quyryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
