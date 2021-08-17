class IAMUserMixin:
    def has_role(self, role, *args):
        if not self.is_authenticated:
            return False

        self.__dict__.setdefault('_roles_cache', {})

        roles_cache = self.__dict__['_roles_cache']
        cache_key = (role, *args)
        if roles_cache.get(cache_key) is None:
            profile_model = role.profile_model
            try:
                profile = profile_model.objects.active().get(user=self)
                self.role_profile_exists(profile, role, *args)
            except profile_model.DoesNotExist:
                self.role_profile_doesnt_exist(role, *args)
        return roles_cache[cache_key]

    def role_profile_exists(self, profile, role, *args):
        roles_cache = self.__dict__['_roles_cache']
        cache_key = (role, *args)
        roles_cache[cache_key] = True

    def role_profile_doesnt_exist(self, role, *args):
        roles_cache = self.__dict__['_roles_cache']
        cache_key = (role, *args)
        roles_cache[cache_key] = False
