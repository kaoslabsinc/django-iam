from django.contrib import admin
from django.contrib.auth import get_user_model

from iam.contrib.users.admin import IAMUserAdmin
from .models import AppAdminProfile

User = get_user_model()

admin.site.register(User, IAMUserAdmin)


@admin.register(AppAdminProfile)
class AppAdminProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    autocomplete_fields = ('user',)
