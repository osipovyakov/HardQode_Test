from django.shortcuts import get_object_or_404
from users.models import CustomUser
from products.models import (Lesson, Product, LessonProduct, LessonsForUsers, ProductsForUsers)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, SAFE_METHODS
from .permissions import IsOwner, UserAccess
from .serializers import (
    CustomUserSerializer, LessonSerializer, ProductsForUsers,
    ProductReadSerializer, ProductsForUsersReadSerializer,
    ProductCreateUpdateSerializer, ProductsForUsersCreateUpdateSerializer)


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LessonsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (IsOwner, UserAccess,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductReadSerializer
        return ProductCreateUpdateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsOwner])
    def access(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ProductsForUsers, request.user, pk)
        return self.delete_from(ProductsForUsers, request.user, pk)


class ProductsForUsersViewSet(viewsets.ModelViewSet):
    queryset = ProductsForUsers.objects.all()
    permission_classes = (IsOwner, UserAccess,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductsForUsersReadSerializer
        return ProductsForUsersCreateUpdateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsOwner])
    def access(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ProductsForUsers, request.user, pk)
        return self.delete_from(ProductsForUsers, request.user, pk)
