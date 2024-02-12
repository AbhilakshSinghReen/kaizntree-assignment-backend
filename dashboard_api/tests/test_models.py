from django.core.exceptions import ValidationError
import pytest

from dashboard_api.models import (
    Organization,
)


def test_organization_str_return(organization_1):
    assert organization_1.__str__() == "Organization 1"


def test_create_organization_invalid_json_list_field():
    with pytest.raises(ValidationError) as error:
        Organization.objects.create(
            name="Organization x",
            roles='foo',
            item_tags="bar",
            item_usage_tags="also bar"
        )

        assert str(error.value) == "Invalid JSON format for \"roles\"."

    with pytest.raises(ValidationError) as error:
        Organization.objects.create(
            name="Organization x",
            roles='["admin"]',
            item_tags="{}",
            item_usage_tags="also bar"
        )

        assert str(error.value) == "\"item_tags\" must be a list."


def test_create_organization_without_admin_role():
    with pytest.raises(ValidationError) as error:
        Organization.objects.create(
            name="Organization x",
            roles='["not_admin"]'
        )

        assert str(error.value) == "Organization must have an \"admin\" role."
