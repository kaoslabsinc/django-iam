from django.utils.text import camel_case_to_spaces


def get_profile_class_verbose_name_plural(class_name=None, verbose_name_plural=None):
    if class_name is not None:
        return f"{camel_case_to_spaces(class_name)}s 👤"
    return f"{verbose_name_plural} 👤"
