from django.utils.text import camel_case_to_spaces


def get_profile_cls_verbose_name_plural(cls_name=None, verbose=None):
    if cls_name is not None:
        return f"{camel_case_to_spaces(cls_name)}s 👤"
    return f"{verbose} 👤"
