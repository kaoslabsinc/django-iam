from django.contrib import admin

from .models import SimpleManager, SimpleModel, SimpleProxy

admin.site.register(SimpleManager)
admin.site.register(SimpleModel)
admin.site.register(SimpleProxy)
