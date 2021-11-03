from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import AdminProfile

User = get_user_model()

admin.site.register(User, UserAdmin)


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    autocomplete_fields = ('user',)
