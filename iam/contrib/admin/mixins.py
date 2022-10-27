from building_blocks.consts.field_names import OWNER
from django.contrib import admin


class AutoOwnerAdminMixin(admin.ModelAdmin):
    """
    Admin mixin that autofills an owner field (denoted by `owner_field`, default ``owner``) with the appropriate profile
    of the user who is logged in.
    """
    owner_field = OWNER

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
