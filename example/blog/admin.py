from django.contrib import admin

from .models import BlogAdminProfile, BlogAuthorProfile, BlogPost

admin.site.register(BlogAdminProfile)
admin.site.register(BlogAuthorProfile)
admin.site.register(BlogPost)
