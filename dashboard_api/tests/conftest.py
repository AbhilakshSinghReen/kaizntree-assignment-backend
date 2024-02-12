import pytest

from dashboard_api.models import (
    CustomUser,
    Item,
    ItemCategory,
    ItemSubCategory,
    Organization,
)
from rest_framework.test import APIClient


NUM_USERS_PER_ORG = 2
NUM_ITEM_CATEGORIES_PER_ORG = 2




def pytest_configure():
    pytest.cache = {
        'auth': {
            'email': None,
            'password': None,
            'access_token': None,
            'refresh_token': None,
        }
    }

@pytest.fixture
def api_client():
    return APIClient

# Organizations
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

# Users
@pytest.fixture
def org_1_users(db, organization_1, api_client, scope="session"):
    login_endpoint = "/api/dashboard/auth/login/"

    users = []

    for i in range(1, 1 + NUM_USERS_PER_ORG):
        new_user = CustomUser.objects.create_user(
            email=f"user{i}@org1.com",
            username=f"user1-{i}",
            password="1234",
            full_name=f"User {i}",
            phone_number="0000000000",
            organization=organization_1,
            role="admin"
        )

        login_response = api_client().post(
            login_endpoint,
            {
                "username": f"user1-{i}",
	            "password": "1234"
            },
            format='json'
        )

        login_response_data = login_response.json()

        users.append({
            'object': new_user,
            'tokens': login_response_data
        })
    
    return users

@pytest.fixture
def org_2_users(db, organization_2, api_client, scope="session"):
    login_endpoint = "/api/dashboard/auth/login/"

    users = []

    for i in range(1, 1 + NUM_USERS_PER_ORG):
        new_user = CustomUser.objects.create_user(
            email=f"user{i}@org2.com",
            username=f"user2-{i}",
            password="1234",
            full_name=f"User {i}",
            phone_number="0000000000",
            organization=organization_2,
            role="admin"
        )

        login_response = api_client().post(
            login_endpoint,
            {
                "username": f"user1-{i}",
	            "password": "1234"
            },
            format='json'
        )

        login_response_data = login_response.json()

        users.append({
            'object': new_user,
            'tokens': login_response_data
        })
    
    return users


@pytest.fixture
def user_1(db, organization_1, scope="session"):
    new_user = CustomUser.objects.create_user(
        email="user1@kaizntree.com",
        username="user1",
        password="1234",
        full_name="User One",
        phone_number="0000000000",
        organization=organization_1,
        role="admin"
    )
    return new_user

@pytest.fixture
def org_1_item_categories(db, organization_1, scope="session"):
    item_categories = []

    for i in range(11, 11 + NUM_ITEM_CATEGORIES_PER_ORG):
        new_item_category = ItemCategory.objects.create(
            name=f"Item Category {i}",
            organization=organization_1
        )
        item_categories.append(new_item_category)
        
    return item_categories

@pytest.fixture
def org_2_item_categories(db, organization_2, scope="session"):
    item_categories = []

    for i in range(11, 11 + NUM_ITEM_CATEGORIES_PER_ORG):
        new_item_category = ItemCategory.objects.create(
            name=f"Item Category {i}",
            organization=organization_2
        )
        item_categories.append(new_item_category)
        
    return item_categories






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
    new_user = ItemSubCategory.objects.create(
        name="Item Sub Category 1",
        organization=organization_1,
        category=item_category_1
    )
    return new_user

@pytest.fixture
def item_sub_category_2(db, organization_1, item_category_1, scope="session"):
    new_user = ItemSubCategory.objects.create(
        name="Item Sub Category 2",
        organization=organization_1,
        category=item_category_1
    )
    return new_user

# @pytest.fixture
# def item_1(db, organization_1, item_category_1, item_sub_category_1, scope="session"):
#     new_user = ItemSubCategory.objects.create(
#         name="Item 1",
#         stock_keeping_unit="item1",
#         organization=organization_1,
#         category=item_category_1,
#         sub_category=item_sub_category_1,
#     )
#     return new_user

