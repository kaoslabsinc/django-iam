import pytest


class TestAbstractIAMUser:
    @pytest.fixture
    def user(self, create_user):
        return create_user(first_name="John", last_name="Smith", username="jsmith")

    @pytest.fixture
    def user_no_name(self, create_user):
        return create_user(username="jsmith2")

    def test_full_name(self, user, user_no_name):
        assert user.full_name == "John Smith"
        assert user_no_name.full_name == ""

    def test_display_name(self, user, user_no_name):
        assert user.display_name == "John Smith"
        assert user_no_name.display_name == "jsmith2"

    def test_display_id(self, user, user_no_name):
        assert user.display_id == "jsmith"
        assert user_no_name.display_id == "jsmith2"
