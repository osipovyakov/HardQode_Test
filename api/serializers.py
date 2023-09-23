from django.db import transaction
from djoser.serializers import UserSerializer
from products.models import (Lesson, Product, LessonProduct, ProductsForUsers)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, ReadOnlyField
from users.models import CustomUser


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
        )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonProductSerializer(serializers.ModelSerializer):
    name = ReadOnlyField(
        source='lesson.name')
    id = ReadOnlyField(
        source='lesson.id')

    class Meta:
        model = LessonProduct
        fields = ('id', 'name')


class ProductReadSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    lessons = LessonProductSerializer(
        read_only=True, many=True, source='product_lessonproduct')
    is_accessed = SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_is_accessed(self, obj):
        return ProductsForUsers.objects.filter(
            user=self.context['request'].user.id, product=obj.id).exists()


class LessonProductCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        source='lesson')

    class Meta:
        model = LessonProduct
        fields = '__all__'


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    lesson = LessonProductCreateSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def validate_lessons(self, value):
        lessons = value
        if not lessons:
            raise ValidationError({
                'Нужен хотя бы один урок!'})
        lessons_list = []
        for item in lessons:
            if item in lessons_list:
                raise ValidationError({
                    'Уроки не могут повторяться!'})
            lessons_list.append(item)
        return value

    def product_lessons(self, product, lessons):
        LessonProduct.objects.bulk_create(
            LessonProduct(
                product=product,
                lesson=lesson.get('lesson'),
                status=lesson.get('status')
            ) for lesson in lessons)

    @transaction.atomic
    def create(self, validated_data):
        lessons = validated_data.pop('lessons')
        product = Product.objects.create(**validated_data)
        self.product_lessons(
            product=product, lessons=lessons)
        return product

    @transaction.atomic
    def update(self, instance, validated_data):
        lessons = validated_data.pop('lessons')
        instance = super().update(instance, validated_data)
        instance.lessons.clear()
        self.product_lessons(
            product=instance, lessons=lessons)
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ProductReadSerializer(instance, context=context).data


class ProductsForUsersReadSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    lessons = LessonProductSerializer(
        read_only=True, many=True, source='product_lessonproduct')
    is_accessed = SerializerMethodField()

    class Meta:
        model = ProductsForUsers
        fields = '__all__'

    def get_is_accessed(self, obj):
        return ProductsForUsers.objects.filter(
            user=self.context['request'].user.id, product=obj.id).exists()


class ProductsForUsersCreateUpdateSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    lessons = LessonProductSerializer(
        read_only=True, many=True, source='product_lessonproduct')
    is_accessed = SerializerMethodField()

    class Meta:
        model = ProductsForUsers
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.pop('product_for_user')
        product = ProductsForUsers.objects.create(**validated_data)
        self.product_for_user(
            product=product, user=user)
        return product

    @transaction.atomic
    def update(self, instance, validated_data):
        user = validated_data.pop('lessons')
        instance = super().update(instance, validated_data)
        instance.user.clear()
        self.product_lessons(
            product=instance, user=user)
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ProductReadSerializer(instance, context=context).data
