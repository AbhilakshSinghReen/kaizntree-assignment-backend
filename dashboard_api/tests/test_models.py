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


@pytest.mark.skip
class TestOrganization:
    def test_organization_str_return(self, organization_1):
        assert organization_1.__str__() == "Organization 1"
    
    def test_create_organization_invalid_json_list_field(self):
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
    
    def test_create_organization_without_admin_role(self):
        with pytest.raises(ValidationError) as error:
            Organization.objects.create(
                name="Organization x",
                roles='["not_admin"]'
            )

            assert str(error.value) == "Organization must have an \"admin\" role."

    def test_update_organization_invalid_json_list_field(self, organization_1):
        original_roles = organization_1.roles
        original_item_tags = organization_1.item_tags

        with pytest.raises(ValidationError) as error:
            organization_1.roles = "foo"
            organization_1.save()

            assert str(error.value) == "Invalid JSON format for \"roles\"."
            assert organization_1.roles == original_roles

        with pytest.raises(ValidationError) as error:
            organization_1.roles = "{}"
            organization_1.save()

            assert str(error.value) == "\"item_tags\" must be a list."
            assert organization_1.item_tags == original_item_tags


@pytest.mark.skip
class TestCustomUser:
    def test_user_str_return(self, organization_1):
        new_user = CustomUser.objects.create_user(
            email="x@x.com",
            username="xxx",
            password="1234",
            full_name="X",
            phone_number="0000000000",
            organization=organization_1,
            role="admin"
        )

        assert new_user.__str__() == "xxx"

    def test_create_user_invalid_role(self, organization_1):
        with pytest.raises(ValidationError) as error:
            new_user = CustomUser.objects.create_user(
                email="x@x.com",
                username="xxx",
                password="1234",
                full_name="X",
                phone_number="0000000000",
                organization=organization_1,
                role="foo"
            )

            assert str(error.value) == "User role (foo) does not exist in the organization's roles."

    def test_update_user_invalid_role(self, user_1):
        original_role = user_1.role

        with pytest.raises(ValidationError) as error:
            user_1.role = "foo"
            user_1.save()

            assert "User role (foo) does not exist in the organization's roles." in str(error.value)

        updated_user_1 = CustomUser.objects.get(id=user_1.id)
        assert updated_user_1.role == original_role

    def test_create_user_check_password(self, organization_1):
        original_num_users = CustomUser.objects.count()

        new_user = CustomUser.objects.create_user(
            email="x@x.com",
            username="xxx",
            password="1234",
            full_name="X",
            phone_number="0000000000",
            organization=organization_1,
            role="admin"
        )

        assert CustomUser.objects.count() == original_num_users + 1

        user = CustomUser.objects.get(id=new_user.id)

        assert user.email == "x@x.com"
        assert user.username == "xxx"
        assert user.password != "1234"
        assert user.check_password("1234") == True
        assert user.full_name == "X"
        assert user.phone_number == "0000000000"
        assert user.organization.id == organization_1.id
        assert user.role == "admin"


    # def test_create_user_without_field(self, organization_1):
    #     original_num_users = CustomUser.objects.count()

    #     new_user = CustomUser.objects.create_user(
    #         full_name="A B C",
    #         phone_number="0000000000",
    #         organization=organization_1,
    #         role="admin"
    #     )

    #     print(new_user.email)

    #     assert CustomUser.objects.count() == original_num_users + 1

    def test_create_user(self, organization_1):
        original_num_users = CustomUser.objects.count()

        new_user = CustomUser.objects.create_user(
            email="abc@kaizntree.com",
            username="abc",
            password="1234",
            full_name="A B C",
            phone_number="0000000000",
            organization=organization_1,
            role="admin"
        )

        assert CustomUser.objects.count() == original_num_users + 1

    def test_custom_user_manager_create_user(self, organization_1):
        original_num_users = CustomUser.objects.count()

        CustomUser.objects.create_user(
            email="abcd@kaizntree.com",
            username="abcd",
            password="1234",
            full_name="A B C D",
            phone_number="0000000000",
            organization=organization_1,
            role="admin"
        )

        assert CustomUser.objects.count() == original_num_users + 1

    def test_custom_user_manager_create_super_user(self, organization_1):
        original_num_users = CustomUser.objects.count()

        CustomUser.objects.create_superuser(
            email="abcd@kaizntree.com",
            username="abcd",
            password="1234",
            full_name="A B C D",
            phone_number="0000000000",
        )

        assert CustomUser.objects.count() == original_num_users + 1


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
class TestItemCategory:
    def test_item_category_str_return(self, organization_1):
        new_item_category = ItemCategory.objects.create(
            name="Doors",
            organization=organization_1
        )

        assert new_item_category.__str__() == "Doors"

    def test_create_item_category_unique_together(self, organization_1, organization_2):
        ItemCategory.objects.create(
            name="Windows",
            organization=organization_1
        )

        with pytest.raises(IntegrityError) as error:
            ItemCategory.objects.create(
                name="Windows",
                organization=organization_1
            )

            assert 'UNIQUE constraint failed' in str(error.value)

        item_category_1 = ItemCategory.objects.create(
            name="Carpets",
            organization=organization_1
        )

        item_category_2 = ItemCategory.objects.create(
            name="Carpets",
            organization=organization_2
        )

        assert item_category_1.name == item_category_2.name
        assert item_category_1.organization != item_category_2.organization
    
    def test_update_item_category_unique_together(self, item_category_1, item_category_2):
        original_name = item_category_1.name
        
        with pytest.raises(IntegrityError) as error:
            item_category_1.name = item_category_2.name
            item_category_1.save()

            assert 'UNIQUE constraint failed' in str(error.value)

        updated_item_category_1 = ItemCategory.objects.get(id=item_category_1.id)
        assert updated_item_category_1.name == original_name


@pytest.mark.skip
class TestItemSubCategory:
    def test_item_sub_category_str_return(self, organization_1, item_category_1):
        new_item_sub_category = ItemSubcategory.objects.create(
            name="Wooden",
            category=item_category_1,
            organization=organization_1
        )

        assert new_item_sub_category.__str__() == "Wooden"


@pytest.mark.skip
class TestItem:
    def test_item_str_return(self, organization_1, item_category_1, item_sub_category_1):
        new_item = Item.objects.create(
            name="Red Wooden Door 6'x3'",
            stock_keeping_unit="RWD63",
            organization=organization_1,
            category=item_category_1,
            sub_category=item_sub_category_1,
            cost=100.00
        )

        assert new_item.__str__() == "Red Wooden Door 6'x3'"

    def test_item_invalid_json_list__tags(self, organization_1, item_category_1, item_sub_category_1):
        with pytest.raises(ValidationError) as error:
            new_item = Item.objects.create(
                name="Brown Wooden Door 6'x3'",
                stock_keeping_unit="BWD63",
                organization=organization_1,
                category=item_category_1,
                sub_category=item_sub_category_1,
                cost=100.00,
                tags="foo"
            )
            assert str(error.value) == "Invalid JSON format for \"tags\"."
        
        with pytest.raises(ValidationError) as error:
            new_item = Item.objects.create(
                name="Brown Wooden Door 6'x3'",
                stock_keeping_unit="BWD63",
                organization=organization_1,
                category=item_category_1,
                sub_category=item_sub_category_1,
                cost=100.00,
                tags="{}"
            )
            assert str(error.value) == "Invalid JSON format for \"tags\"."
    
    def test_item_undefined_tags(self, organization_1, item_category_1, item_sub_category_1):
        with pytest.raises(ValidationError) as error:
            new_item = Item.objects.create(
                name="Brown Wooden Door 6'x3'",
                stock_keeping_unit="BWD63",
                organization=organization_1,
                category=item_category_1,
                sub_category=item_sub_category_1,
                cost=100.00,
                tags=json_dumps(['foo', 'bar'])
            )
            assert str(error.value) == "Tags foo, bar are not defined in the item's organization."

    def test_item_undefined_usage_tags(self, organization_1, item_category_1, item_sub_category_1):
        with pytest.raises(ValidationError) as error:
            new_item = Item.objects.create(
                name="Brown Wooden Door 6'x3'",
                stock_keeping_unit="BWD63",
                organization=organization_1,
                category=item_category_1,
                sub_category=item_sub_category_1,
                cost=100.00,
                usage_tags=json_dumps(['foo', 'bar'])
            )
            assert str(error.value) == "Usage tags foo, bar are not defined in the item's organization."
