from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import AppAdminProfile

User = get_user_model()

admin.site.register(User, UserAdmin)


@admin.register(AppAdminProfile)
class AppAdminProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    autocomplete_fields = ('user',)
