from django.contrib import admin
from django.contrib.auth import get_user_model

from iam.contrib.users.admin import IAMUserAdmin

User = get_user_model()

admin.site.register(User, IAMUserAdmin)
