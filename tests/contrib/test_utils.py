from iam.contrib.utils import get_profile_cls_verbose_name_plural


def test_get_profile_cls_verbose_name_plural():
    profile_cls_name = 'SomeClassProfile'
    verbose_name_plural = get_profile_cls_verbose_name_plural(profile_cls_name)
    assert verbose_name_plural == "some class profiles 👤"


def test_get_profile_cls_verbose_name_plural_verbose():
    verbose = "some class profiles"
    verbose_name_plural = get_profile_cls_verbose_name_plural(verbose=verbose)
    assert verbose_name_plural == "some class profiles 👤"
