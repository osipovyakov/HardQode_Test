from django.contrib import admin
from products.models import (Lesson, Product, LessonProduct,
                             LessonsForUsers, ProductsForUsers)


class LessonAdmin (admin.ModelAdmin):
    list_display = ('name', 'link', 'duration', 'pub_date',)
    list_filter = ('pub_date',)


class ProductAdmin (admin.ModelAdmin):
    list_display = ('owner', 'name', 'pub_date',)
    list_filter = ('pub_date',)


class LessonProductAdmin (admin.ModelAdmin):
    list_display = ('lesson', 'product',)


class LessonsForUsersAdmin (admin.ModelAdmin):
    list_display = ('user', 'lesson', 'timming', 'status',)
    list_filter = ('user',)


class ProductsForUsersAdmin (admin.ModelAdmin):
    list_display = ('user', 'product',)
    list_filter = ('user',)


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(LessonProduct, LessonProductAdmin)
admin.site.register(LessonsForUsers, LessonsForUsersAdmin)
admin.site.register(ProductsForUsers, ProductsForUsersAdmin)
