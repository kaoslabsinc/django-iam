from django.contrib import admin

from iam.contrib.admin.admin import ObjectPermissionsProfileAdmin
from .models import BlogAdminProfile, BlogAuthorProfile, BlogPost

admin.site.register(BlogAdminProfile, ObjectPermissionsProfileAdmin)
admin.site.register(BlogAuthorProfile, ObjectPermissionsProfileAdmin)
admin.site.register(BlogPost)
