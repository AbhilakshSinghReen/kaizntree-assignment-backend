import pytest

from dashboard_api.models import (
    CustomUser,
    Item,
    ItemCategory,
    ItemSubcategory,
    Organization,
)


@pytest.fixture
def organization_1(db, scope="session"):
    new_organization = Organization.objects.create(
        name="Organization 1",
        roles='["admin", "worker", "sales"]'
    )
    return new_organization

@pytest.fixture
def organization_2(db, scope="session"):
    new_organization = Organization.objects.create(
        name="Organization 2",
        roles='["admin", "worker", "sales"]'
    )
    return new_organization

@pytest.fixture
def user_1(db, organization_1, scope="session"):
    new_user = CustomUser.objects.create(
        email="user1@kaizntree.com",
        username="user1",
        full_name="User One",
        phone_number="0000000000",
        organization=organization_1,
        role="admin"
    )
    return new_user

@pytest.fixture
def item_category_1(db, organization_1, scope="session"):
    new_user = ItemCategory.objects.create(
        name="Item Category 1",
        organization=organization_1
    )
    return new_user

@pytest.fixture
def item_category_2(db, organization_1, scope="session"):
    new_user = ItemCategory.objects.create(
        name="Item Category 2",
        organization=organization_1
    )
    return new_user

@pytest.fixture
def item_sub_category_1(db, organization_1, item_category_1, scope="session"):
    new_user = ItemSubcategory.objects.create(
        name="Item Sub Category 1",
        organization=organization_1,
        category=item_category_1
    )
    return new_user

@pytest.fixture
def item_sub_category_2(db, organization_1, item_category_1, scope="session"):
    new_user = ItemSubcategory.objects.create(
        name="Item Sub Category 2",
        organization=organization_1,
        category=item_category_1
    )
    return new_user

# @pytest.fixture
# def item_1(db, organization_1, item_category_1, item_sub_category_1, scope="session"):
#     new_user = ItemSubcategory.objects.create(
#         name="Item 1",
#         stock_keeping_unit="item1",
#         organization=organization_1,
#         category=item_category_1,
#         sub_category=item_sub_category_1,
#     )
#     return new_user

