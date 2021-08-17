from django.contrib import admin

from .models import SimpleManager, SimpleModel

admin.site.register(SimpleManager)
admin.site.register(SimpleModel)
