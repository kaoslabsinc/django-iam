from django.contrib.admin.options import BaseModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _


class HideSuperuserUserAdminMixin(BaseModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(is_superuser=False)

    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj) or ()
        if request.user.is_superuser:
            return exclude
        return (
            *exclude,
            'is_superuser', 'user_permissions',
        )

    def get_fieldsets(self, request, obj=None):
        exclude = self.get_exclude(request, obj)
        fieldsets = super().get_fieldsets(request, obj) or ()
        return [
            (fieldset_name,
             {'fields': [field for field in values['fields'] if field not in exclude]})
            for fieldset_name, values in fieldsets
        ]


class BaseIAMUserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'full_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'groups')
    readonly_fields = ('date_joined', 'last_login',)

    add_fieldsets = (
        *DjangoUserAdmin.add_fieldsets,
        (_('Permissions'), {
            'fields': ('is_staff',),
        })
    )


class IAMUserAdmin(HideSuperuserUserAdminMixin, BaseIAMUserAdmin):
    pass


__all__ = [
    'HideSuperuserUserAdminMixin',
    'BaseIAMUserAdmin',
    'IAMUserAdmin',
]
