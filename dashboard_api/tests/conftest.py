import pytest

from dashboard_api.models import (
    Organization,
)


@pytest.fixture
def organization_1(db, scope="session"):
    new_organization = Organization.objects.create(
        name="Organization 1",
        roles='["admin"]'
    )
    return new_organization
