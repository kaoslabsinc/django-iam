from django.contrib import admin
from django.contrib.auth import get_user_model

from iam.contrib.admin import ObjectPermissionsProfileAdmin
from iam.contrib.users import IAMUserAdmin
from .models import AppAdminProfile

User = get_user_model()

admin.site.register(User, IAMUserAdmin)
admin.site.register(AppAdminProfile, ObjectPermissionsProfileAdmin)
