from django.contrib import admin


class AutoOwnerAdminMixin(admin.ModelAdmin):
    owner_field = 'owner'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == self.owner_field and field.initial is None:
            profile_model = getattr(self.model, self.owner_field).field.related_model
            try:
                field.initial = profile_model.objects.active().get(user=request.user)
            except profile_model.DoesNotExist:
                pass
        return field


__all__ = [
    'AutoOwnerAdminMixin',
]
