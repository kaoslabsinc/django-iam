from django.contrib import admin

from .models import BlogAdminProfile, BlogAuthorProfile

admin.site.register(BlogAdminProfile)
admin.site.register(BlogAuthorProfile)
