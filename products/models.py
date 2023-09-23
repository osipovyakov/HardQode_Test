from django.core.validators import MinValueValidator
from users.models import CustomUser
from django.db import models


class Lesson(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название урока'
    )
    link = models.URLField(
        max_length=400,
        verbose_name='Ссылка на урок'
    )
    duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Длительность урока в секундах'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации урока',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='Владелец',
        null=False,
        default=None
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название продукта'
    )
    description = models.CharField(
        max_length=2000,
        verbose_name='Описание продукта'
    )
    lessons = models.ManyToManyField(
        Lesson,
        through='LessonProduct',
        related_name='product_lesson',
        verbose_name='Урок'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации продукта',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class LessonProduct (models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_lessonproduct',
        verbose_name='Урок',
        default=None
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_lessonproduct',
        verbose_name='Продукт',
        default=None
    )

    class Meta:
        verbose_name = 'Урок в продукте'
        verbose_name_plural = 'Уроки в продукте'
        ordering = ['-id']

    def __str__(self):
        return f'{self.product}: {self.lesson}'


class ProductsForUsers (models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='product_for_user',
        verbose_name='Пользователь',
        default=None
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_for_user',
        verbose_name='Продукт для пользователя',
        default=None
    )
    is_accessed = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Продукт для пользователя'
        verbose_name_plural = 'Продукты для пользователя'
        ordering = ['-id']

    def __str__(self):
        return f'Продукт {self.product} для пользователя {self.user}'


class LessonsForUsers (models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='lesson_for_user',
        verbose_name='Пользователь',
        default=None
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_for_user',
        verbose_name='Урок для пользователя',
        default=None
    )

    timming = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время просмотра урока в секундах'
    )

    status = models.CharField(
        max_length=50,
        verbose_name='Статус урока',
        default='Не просмотрено'
    )

    REQUIRED_FIELDS = ['timming']

    class Meta:
        verbose_name = 'Урок для пользователя'
        verbose_name_plural = 'Уроки для пользователя'
        ordering = ['-id']

    def __str__(self):
        return f'Урок {self.lesson} для пользователя {self.user}'
