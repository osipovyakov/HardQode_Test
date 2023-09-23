from django.contrib import admin
from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role',)
    list_filter = ('role',)


admin.site.register(CustomUser, UserAdmin)
