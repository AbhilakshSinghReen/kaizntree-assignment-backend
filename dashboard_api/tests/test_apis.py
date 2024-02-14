from json import loads as json_loads

import pytest

from dashboard_api.models import (
    CustomUser,
)


# @pytest.mark.skip
@pytest.mark.django_db
class TestAuthAPIs:
    register_endpoint = "/api/dashboard/auth/register/"
    login_endpoint = "/api/dashboard/auth/login/"
    token_refresh_endpoint = "/api/dashboard/auth/token/refresh/"
    logout_endpoint = "/api/dashboard/auth/logout/"
    
    def test_register_invalid(self, api_client, organization_1):
        # Test Register
        original_num_users = CustomUser.objects.count()

        response = api_client().post(
            self.register_endpoint,
            {
                "username": "user11",
                "password": "1234",
                "full_name": "User Eleven",
                "phone_number": "0000000000",
                "organization_id": organization_1.id,
                "role": "admin"
            },
            format='json'
        )

        assert response.status_code == 400
        assert response.headers['content-type'] == "application/json"

        response_data = response.json()

        assert "email" in response_data.keys()

        assert CustomUser.objects.count() == original_num_users
        
    def test_auth(self, api_client, organization_1):
        # Test Register
        original_num_users = CustomUser.objects.count()

        register_response = api_client().post(
            self.register_endpoint,
            {
                "email": "user11@kaizntree.com",
                "username": "user11",
                "password": "1234",
                "full_name": "User Eleven",
                "phone_number": "0000000000",
                "organization_id": organization_1.id,
                "role": "admin"
            },
            format='json'
        )

        assert register_response.status_code == 201
        assert CustomUser.objects.count() == original_num_users + 1

        pytest.cache['auth']['email'] = "user11@kaizntree.com"
        pytest.cache['auth']['username'] = "user11"
        pytest.cache['auth']['password'] = "1234"


        # Test Login
        login_response = api_client().post(
            self.login_endpoint,
            {
                "username": pytest.cache['auth']['username'],
	            "password": pytest.cache['auth']['password']
            },
            format='json'
        )

        assert login_response.status_code == 200
        assert login_response.headers['content-type'] == "application/json"

        login_response_data = login_response.json()

        assert "access" in login_response_data.keys()
        assert "refresh" in login_response_data.keys()

        pytest.cache['auth']['access_token'] = login_response_data['access']
        pytest.cache['auth']['refresh_token'] = login_response_data['refresh']


        # Test Refresh
        token_refresh_response = api_client().post(
            self.token_refresh_endpoint,
            {
                "refresh": pytest.cache['auth']['refresh_token']
            },
            format='json'
        )

        assert token_refresh_response.status_code == 200
        assert token_refresh_response.headers['content-type'] == "application/json"

        token_refresh_response_data = token_refresh_response.json()

        assert "access" in token_refresh_response_data.keys()

        pytest.cache['auth']['access_token'] = token_refresh_response_data['access']


        # Test Logout (Blacklist)
        logout_response = api_client().post(
            self.logout_endpoint,
            {
                "refresh": pytest.cache['auth']['refresh_token']
            },
            format='json'
        )

        assert logout_response.status_code == 200
        assert logout_response.headers['content-type'] == "application/json"

        logout_response_data = logout_response.json()

        assert len(logout_response_data.keys()) == 0


        # Test Refresh Again (after Blacklist)
        token_refresh_response = api_client().post(
            self.token_refresh_endpoint,
            {
                "refresh": pytest.cache['auth']['refresh_token']
            },
            format='json'
        )

        assert token_refresh_response.status_code == 401
        assert token_refresh_response.headers['content-type'] == "application/json"


# @pytest.mark.skip
@pytest.mark.django_db
class TestItemCategoryAPIs:
    endpoint = "/api/dashboard/item-categories/"
    endpoint_with_pk = "/api/dashboard/item-categories/{{pk}}/"
    
    def test_get_by_id(self, api_client, org_1_item_categories, org_1_users, org_2_users):
        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(org_1_item_categories[0].id))

        # Test Org 1 Category with Org 1 User
        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(endpoint_with_pk, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert response_1_data['id'] == org_1_item_categories[0].id

        
        # Test Org 1 Category with Org 2 User
        headers_2 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_2_users[0]['tokens']['access']}",
        }

        response_2 = api_client().get(endpoint_with_pk, **headers_2)

        assert response_2.status_code == 404

    def test_get_all(self, api_client, org_1_item_categories, org_1_users):
        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(self.endpoint, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert isinstance(response_1_data, list)
        assert len(response_1_data) == len(org_1_item_categories)

        for i, object in enumerate(response_1_data):
            assert object['id'] == org_1_item_categories[i].id
    
    def test_create(self, api_client, org_1_users):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response = api_client().post(
            self.endpoint,
            {
                "name": "Item Category X",
            },
            format='json',
            **headers
        )

        assert create_response.status_code == 201
        assert create_response.headers['content-type'] == "application/json"

        create_response_data = create_response.json()
        assert create_response_data['name'] == "Item Category X"
        assert create_response_data['organization'] == 1

    def test_update(self, api_client, org_1_users):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response = api_client().post(
            self.endpoint,
            {
                "name": "Item Category Y",
            },
            format='json',
            **headers
        )

        create_response_data = create_response.json()

        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(create_response_data['id']))

        update_response = api_client().put(
            endpoint_with_pk,
            {
                "name": "Item Category Y2",
            },
            format='json',
            **headers
        )
        
        assert update_response.status_code == 200
        assert update_response.headers['content-type'] == "application/json"

        update_response_data = update_response.json()
        assert update_response_data['name'] == "Item Category Y2"
        assert update_response_data['organization'] == 1
    
    def test_delete(self, api_client, org_1_users):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response = api_client().post(
            self.endpoint,
            {
                "name": "Item Category Y",
            },
            format='json',
            **headers
        )

        create_response_data = create_response.json()

        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(create_response_data['id']))

        delete_response = api_client().delete(endpoint_with_pk,**headers)

        assert delete_response.status_code == 204

    # TODO: def test_create_duplicate
    # TODO: def test_update_to_duplicate
    # TODO: def test_update_of_different_org
    # TODO: def test_delete_of_different_org


# @pytest.mark.skip
@pytest.mark.django_db
class TestItemSubCategoryAPIs:
    endpoint = "/api/dashboard/item-subcategories/"
    endpoint_with_pk = "/api/dashboard/item-subcategories/{{pk}}/"
    
    def test_get_by_id(self, api_client, org_1_item_subcategories, org_1_users, org_2_users):
        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(org_1_item_subcategories[0].id))

        # Test Org 1 Category with Org 1 User
        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(endpoint_with_pk, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert response_1_data['id'] == org_1_item_subcategories[0].id

        
        # Test Org 1 Category with Org 2 User
        headers_2 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_2_users[0]['tokens']['access']}",
        }

        response_2 = api_client().get(endpoint_with_pk, **headers_2)

        assert response_2.status_code == 404

    def test_get_all(self, api_client, org_1_item_subcategories, org_1_users):
        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(self.endpoint, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert isinstance(response_1_data, list)
        assert len(response_1_data) == len(org_1_item_subcategories)

        for i, object in enumerate(response_1_data):
            assert object['id'] == org_1_item_subcategories[i].id
    
    def test_get_filtered_by_category(self, api_client, org_1_item_categories, org_1_item_subcategories, org_1_users):
        org_1_category_1_item_subcategories = [
            object for object in org_1_item_subcategories
            if object.category == org_1_item_categories[0]
        ]

        endpoint = self.endpoint + f"?category={org_1_item_categories[0].id}"

        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(endpoint, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert isinstance(response_1_data, list)
        assert len(response_1_data) == len(org_1_category_1_item_subcategories)

        for i, object in enumerate(response_1_data):
            assert object['id'] == org_1_category_1_item_subcategories[i].id

    def test_create(self, api_client, org_1_users, org_1_item_categories):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response = api_client().post(
            self.endpoint,
            {
                "name": "Item Sub Category X",
                "category": org_1_item_categories[0].id
            },
            format='json',
            **headers
        )

        assert create_response.status_code == 201
        assert create_response.headers['content-type'] == "application/json"

        create_response_data = create_response.json()
        assert create_response_data['name'] == "Item Sub Category X"
        assert create_response_data['category'] == org_1_item_categories[0].id
        assert create_response_data['organization'] == 1

    def test_update(self, api_client, org_1_users, org_1_item_categories):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response = api_client().post(
            self.endpoint,
            {
                "name": "Item Sub Category Y",
                "category": org_1_item_categories[0].id
            },
            format='json',
            **headers
        )

        create_response_data = create_response.json()

        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(create_response_data['id']))

        update_response = api_client().put(
            endpoint_with_pk,
            {
                "name": "Item Sub Category Y2",
                "category": org_1_item_categories[1].id
            },
            format='json',
            **headers
        )
        
        assert update_response.status_code == 200
        assert update_response.headers['content-type'] == "application/json"

        update_response_data = update_response.json()
        assert update_response_data['name'] == "Item Sub Category Y2"
        assert update_response_data['category'] == org_1_item_categories[1].id
        assert update_response_data['organization'] == 1
    
    def test_delete(self, api_client, org_1_users, org_1_item_categories):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response = api_client().post(
            self.endpoint,
            {
                "name": "Item Sub Category ZZZ",
                "category": org_1_item_categories[0].id
            },
            format='json',
            **headers
        )

        create_response_data = create_response.json()

        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(create_response_data['id']))

        delete_response = api_client().delete(endpoint_with_pk,**headers)

        assert delete_response.status_code == 204

    # TODO: def test_create_duplicate
    # TODO: def test_update_to_duplicate
    # TODO: def test_update_of_different_org
    # TODO: def test_delete_of_different_org


# @pytest.mark.skip
@pytest.mark.django_db
class TestItemAPIs:
    endpoint = "/api/dashboard/items/"
    endpoint_with_pk = "/api/dashboard/items/{{pk}}/"

    def test_get_by_id(self, api_client, org_1_items, org_1_users, org_2_users):
        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(org_1_items[0].id))

        # Test Org 1 Item with Org 1 User
        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(endpoint_with_pk, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert response_1_data['id'] == org_1_items[0].id

        
        # Test Org 1 Item with Org 2 User
        headers_2 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_2_users[0]['tokens']['access']}",
        }

        response_2 = api_client().get(endpoint_with_pk, **headers_2)

        assert response_2.status_code == 404

    def test_get_all(self, api_client, org_1_items, org_1_users):
        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(self.endpoint, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert isinstance(response_1_data, list)
        assert len(response_1_data) == len(org_1_items)

        for i, object in enumerate(response_1_data):
            assert object['id'] == org_1_items[i].id

    def test_get_filtered_by_direct_field(self, api_client, org_1_item_categories, org_1_items, org_1_users):
        org_1_category_1_items = [
            object for object in org_1_items
            if object.category == org_1_item_categories[0]
        ]

        endpoint = self.endpoint + f"?category={org_1_item_categories[0].id}"

        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(endpoint, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert isinstance(response_1_data, list)
        assert len(response_1_data) == len(org_1_category_1_items)

        for i, object in enumerate(response_1_data):
            assert object['id'] == org_1_category_1_items[i].id

    def test_get_filtered_by_contains_field(self, api_client, org_1_items, org_1_users):
        filter_usage_tags = ["assembly", "saleable"]

        org_1_items_with_usage_tags = [
            object for object in org_1_items
            if set(filter_usage_tags).issubset(set(json_loads(object.usage_tags)))
        ]

        endpoint = self.endpoint + f"?usage_tags={'%2c'.join(filter_usage_tags)}"
        
        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(endpoint, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert isinstance(response_1_data, list)
        assert len(response_1_data) == len(org_1_items_with_usage_tags)

        for i, object in enumerate(response_1_data):
            assert object['id'] == org_1_items_with_usage_tags[i].id

    def test_get_filtered_by_range_field(self, api_client, org_1_items, org_1_users):
        min_cost = 250
        max_cost = 750
        min_available_stock = 100
        max_available_stock = 200

        org_1_items_filtered = [
            object for object in org_1_items
            if object.cost > min_cost and object.cost < max_cost
            and object.available_stock >= min_available_stock and object.available_stock <= max_available_stock
        ]

        endpoint = self.endpoint \
            + f"?cost__gte={min_cost}" \
            + f"&cost__lte={max_cost}" \
            + f"&available_stock__gt={min_available_stock}" \
            + f"&available_stock__lt={max_available_stock}"

        headers_1 = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        response_1 = api_client().get(endpoint, **headers_1)

        assert response_1.status_code == 200
        assert response_1.headers['content-type'] == "application/json"

        response_1_data = response_1.json()

        assert isinstance(response_1_data, list)
        assert len(response_1_data) == len(org_1_items_filtered)

        for i, object in enumerate(response_1_data):
            assert object['id'] == org_1_items_filtered[i].id

    def test_create(self, api_client, org_1_users, org_1_item_subcategories):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response_1 = api_client().post(
            self.endpoint,
            {
                "name": "Item X",
                "sub_category": org_1_item_subcategories[0].id,
                "category": org_1_item_subcategories[0].category.id,
                "stock_keeping_unit": "foo",
                "cost": "50.00"
            },
            format='json',
            **headers
        )

        assert create_response_1.status_code == 201
        assert create_response_1.headers['content-type'] == "application/json"

        create_response_1_data = create_response_1.json()
        
        assert create_response_1_data['name'] == "Item X"
        assert create_response_1_data['sub_category'] == org_1_item_subcategories[0].id
        assert create_response_1_data['category'] == org_1_item_subcategories[0].category.id
        assert create_response_1_data['organization'] == 1

        assert create_response_1_data['description'] == ""
        assert create_response_1_data['stock_keeping_unit'] == "foo"
        assert create_response_1_data['allocated_to_sales'] == 0
        assert create_response_1_data['allocated_to_builds'] == 0
        assert create_response_1_data['available_stock'] == 0
        assert create_response_1_data['incoming_stock'] == 0
        assert create_response_1_data['minimum_stock'] == 0
        assert create_response_1_data['desired_stock'] == 0
        assert create_response_1_data['on_build_order'] == 0
        assert create_response_1_data['can_build'] == 0
        assert abs(float(create_response_1_data['cost']) - 50.00) < 0.001
        assert create_response_1_data['tags'] == "[]"
        assert create_response_1_data['usage_tags'] == "[]"

        
        create_response_2 = api_client().post(
            self.endpoint,
            {
                "name": "Item XY",
                "sub_category": org_1_item_subcategories[0].id,
                "category": org_1_item_subcategories[0].category.id,
                "stock_keeping_unit": "bar",
                "cost": "100.00",
                "description": "Very nice item",
                "allocated_to_sales": 50,
                "allocated_to_builds": 20,
                "available_stock": 25,
                "incoming_stock": 15,
                "minimum_stock": 10,
                "desired_stock": 50,
                "on_build_order": 5,
                "can_build": 2,
                "tags": '["shopify"]',
                "usage_tags": '["component", "saleable"]',
            },
            format='json',
            **headers
        )

        assert create_response_2.status_code == 201
        assert create_response_2.headers['content-type'] == "application/json"

        create_response_2_data = create_response_2.json()

        assert create_response_2_data['name'] == "Item XY"
        assert create_response_2_data['sub_category'] == org_1_item_subcategories[0].id
        assert create_response_2_data['category'] == org_1_item_subcategories[0].category.id
        assert create_response_2_data['organization'] == 1

        assert create_response_2_data['description'] == "Very nice item"
        assert create_response_2_data['stock_keeping_unit'] == "bar"
        assert create_response_2_data['allocated_to_sales'] == 50
        assert create_response_2_data['allocated_to_builds'] == 20
        assert create_response_2_data['available_stock'] == 25
        assert create_response_2_data['incoming_stock'] == 15
        assert create_response_2_data['minimum_stock'] == 10
        assert create_response_2_data['desired_stock'] == 50
        assert create_response_2_data['on_build_order'] == 5
        assert create_response_2_data['can_build'] == 2
        assert abs(float(create_response_2_data['cost']) - 100.00) < 0.001
        assert create_response_2_data['tags'] == '["shopify"]'
        assert create_response_2_data['usage_tags'] == '["component", "saleable"]'

    def test_update(self, api_client, org_1_users, org_1_item_subcategories):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response = api_client().post(
            self.endpoint,
            {
                "name": "Item X",
                "sub_category": org_1_item_subcategories[0].id,
                "category": org_1_item_subcategories[0].category.id,
                "stock_keeping_unit": "foo",
                "cost": "50.00"
            },
            format='json',
            **headers
        )

        create_response_data = create_response.json()
        
        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(create_response_data['id']))

        update_response = api_client().put(
            endpoint_with_pk,
            {
                "name": "Item XY",
                "sub_category": org_1_item_subcategories[0].id,
                "category": org_1_item_subcategories[0].category.id,
                "stock_keeping_unit": "bar",
                "cost": "100.00",
                "description": "Very nice item",
                "allocated_to_sales": 50,
                "allocated_to_builds": 20,
                "available_stock": 25,
                "incoming_stock": 15,
                "minimum_stock": 10,
                "desired_stock": 50,
                "on_build_order": 5,
                "can_build": 2,
                "tags": '["shopify"]',
                "usage_tags": '["component", "saleable"]',
            },
            format='json',
            **headers
        )
        
        assert update_response.status_code == 200
        assert update_response.headers['content-type'] == "application/json"

        update_response_data = update_response.json()

        assert update_response_data['name'] == "Item XY"
        assert update_response_data['sub_category'] == org_1_item_subcategories[0].id
        assert update_response_data['category'] == org_1_item_subcategories[0].category.id
        assert update_response_data['organization'] == 1

        assert update_response_data['description'] == "Very nice item"
        assert update_response_data['stock_keeping_unit'] == "bar"
        assert update_response_data['allocated_to_sales'] == 50
        assert update_response_data['allocated_to_builds'] == 20
        assert update_response_data['available_stock'] == 25
        assert update_response_data['incoming_stock'] == 15
        assert update_response_data['minimum_stock'] == 10
        assert update_response_data['desired_stock'] == 50
        assert update_response_data['on_build_order'] == 5
        assert update_response_data['can_build'] == 2
        assert abs(float(update_response_data['cost']) - 100.00) < 0.001
        assert update_response_data['tags'] == '["shopify"]'
        assert update_response_data['usage_tags'] == '["component", "saleable"]'
    
    def test_delete(self, api_client, org_1_users, org_1_item_subcategories):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {org_1_users[0]['tokens']['access']}",
        }

        create_response = api_client().post(
            self.endpoint,
            {
                "name": "Item ZZZ",
                "sub_category": org_1_item_subcategories[0].id,
                "category": org_1_item_subcategories[0].category.id,
                "stock_keeping_unit": "foo",
                "cost": "50.00"
            },
            format='json',
            **headers
        )

        create_response_data = create_response.json()

        endpoint_with_pk = self.endpoint_with_pk.replace("{{pk}}", str(create_response_data['id']))

        delete_response = api_client().delete(endpoint_with_pk,**headers)

        assert delete_response.status_code == 204

    # TODO: def test_create_duplicate
    # TODO: def test_update_to_duplicate
    # TODO: def test_update_of_different_org
    # TODO: def test_delete_of_different_org