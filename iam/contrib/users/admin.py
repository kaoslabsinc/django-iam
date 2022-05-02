from building_blocks.admin.mixins import ExcludeFromFieldsetsMixin, ExcludeFromNonSuperusersMixin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _


class HideSuperuserUserAdminMixin(
    ExcludeFromNonSuperusersMixin,
    ExcludeFromFieldsetsMixin,
    BaseModelAdmin
):
    exclude_from_non_superusers = ('is_superuser', 'user_permissions')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(is_superuser=False)


class BaseIAMUserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'full_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'groups')
    readonly_fields = ('date_joined', 'last_login',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        (_('Permissions'), {
            'classes': ('wide',),
            'fields': ('is_staff',),
        }),
        (_('Personal info'), {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name',),
        }),
    )


class IAMUserAdmin(HideSuperuserUserAdminMixin, BaseIAMUserAdmin):
    pass


__all__ = [
    'HideSuperuserUserAdminMixin',
    'BaseIAMUserAdmin',
    'IAMUserAdmin',
]
