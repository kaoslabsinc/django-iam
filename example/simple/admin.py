from django.contrib import admin

from iam.admin.admin import ProfileAdmin
from .models import SimpleManager, SimpleModel, SimpleProxy

admin.site.register(SimpleManager, ProfileAdmin)
admin.site.register(SimpleModel)
admin.site.register(SimpleProxy)
