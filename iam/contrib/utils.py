from django.utils.text import camel_case_to_spaces


def get_profile_cls_verbose_name_plural(cls_name=None, verbose=None):
    """
    Create a `verbose_name_plural` for a profile model that includes a 👤 emoji. Use this class to make your profile
    classes stand out in the admin.

    :param cls_name: If this value is passed, it uses the class name to build `verbose_name_plural`.
    :param verbose: If this value is passed, it uses this value to build the `verbose_name_plural`.
    :return: A string to pass to `model._meta.verbose_name_plural`.
    """
    if cls_name is not None:
        return f"{camel_case_to_spaces(cls_name)}s 👤"
    return f"{verbose} 👤"
