from iam.contrib.utils import get_profile_cls_verbose_name_plural


class Test_get_profile_cls_verbose_name_plural:
    def test_cls_name(self):
        assert get_profile_cls_verbose_name_plural("AuthorProfile") == "authors 👤"

    def test_verbose(self):
        assert get_profile_cls_verbose_name_plural(verbose="companies") == "companies 👤"
