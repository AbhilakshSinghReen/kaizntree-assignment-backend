from json import dumps as json_dumps

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import pytest

from dashboard_api.models import (
    CustomUser,
    Item,
    ItemCategory,
    ItemSubCategory,
    Organization,
)


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
        print("1 completed")
        
    def test_auth(self, api_client, organization_1):
        print("2 starting")
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


@pytest.mark.django_db
class TestItemCategoryAPIs:
    endpoint = "item-categories/"
    endpoint_with_pk = "item-categories/{{pk}}/"

    def get_access_token(self, user_fixture, api_client):
        login_response = api_client().post(
            self.login_endpoint,
            {
                "username": user_fixture.username,
	            "password": user_fixture.password
            },
            format='json'
        )

        assert login_response.status_code == 200
        assert login_response.headers['content-type'] == "application/json"

        login_response_data = login_response.json()

        assert "access" in login_response_data.keys()
        
        return login_response_data["access"]
    
    # def test_unauthorized()
    
    # def test_create_item_category(self, org_1_user_1):
    #     access_token = self.get_access_token(org_1_user_1)
    #     pass
    
