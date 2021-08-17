class RolesUserMixin:
    def has_role(self, role, privileged=False):
        if not self.is_authenticated:
            return False

        self.__dict__.setdefault('_roles_cache', {})

        roles_cache = self.__dict__['_roles_cache']
        cache_key = (role, privileged)
        if roles_cache.get(cache_key) is None:
            profile_model = role.profile_model
            try:
                profile = profile_model.objects.all().get(user=self)
                roles_cache[(role, False)] = True
                try:
                    roles_cache[(role, True)] = profile.privileged
                except AttributeError:
                    pass
            except profile_model.DoesNotExist:
                roles_cache[(role, False)] = False
                roles_cache[(role, True)] = False  # harmless cache if profile.privileged doesn't exist
        return roles_cache[cache_key]
