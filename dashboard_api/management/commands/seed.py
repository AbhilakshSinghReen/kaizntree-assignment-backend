from json import dumps as json_dumps
from random import randint, sample, seed, uniform

from django.core.management.base import BaseCommand

from dashboard_api.models import (
    CustomUser,
    Item,
    ItemCategory,
    ItemSubCategory,
    Organization,
)

RANDOM_SEED = 0
NUM_USERS_PER_ORG = 2
NUM_ITEM_CATEGORIES_PER_ORG = 2
NUM_ITEM_SUBCATEGORIES_PER_ITEM_CATEGORY = 3
NUM_ITEMS_PER_ITEM_SUBCATEGORY = 4
DEFAULT_TAGS = ["shopify", "xero"]
DEFAULT_USAGE_TAGS = ["assembly", "component", "purchasable", "saleable", "bundle"]


seed(RANDOM_SEED)


class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        self.run_seed()
        self.stdout.write('    ... done.')

    def run_seed(self):
        default_roles = ["admin", "worker", "sales"]

        org_0 = Organization.objects.create(
            name="Kaizntree",
            roles=json_dumps(default_roles),
            item_tags=json_dumps(DEFAULT_TAGS),
            item_usage_tags=json_dumps(DEFAULT_USAGE_TAGS)
        )
        org_1 = Organization.objects.create(
            name="Organization 1",
            roles=json_dumps(default_roles),
            item_tags=json_dumps(["shopify", "xero"]),
            item_usage_tags=json_dumps(["assembly", "component", "purchasable", "saleable", "bundle"])
        )
        org_2 = Organization.objects.create(
            name="Organization 2",
            roles=json_dumps(default_roles),
            item_tags=json_dumps(["shopify", "xero"]),
            item_usage_tags=json_dumps(["assembly", "purchasable", "saleable"])
        )
        org_3 = Organization.objects.create(
            name="Organization 3",
            roles=json_dumps(default_roles),
            item_tags=json_dumps(["xero"]),
            item_usage_tags=json_dumps(["assembly", "component", "purchasable", "saleable", "bundle"])
        )

        user_1 = CustomUser.objects.create_user(
            email="marcos@kaizntree.com",
            username="marcos_brisson",
            password="1234",
            full_name="Marcos Brisson",
            phone_number="0000000000",
            organization=org_0,
            role="admin"
        )

        user_2 = CustomUser.objects.create_user(
            email="ali@kaizntree.com",
            username="ali_quidwai",
            password="1234",
            full_name="Ali Quidwai",
            phone_number="0000000000",
            organization=org_0,
            role="admin"
        )

        user_3 = CustomUser.objects.create_user(
            email="abhilakshsinghreen@gmail.com",
            username="abhilaksh_singh_reen",
            password="1234",
            full_name="Abhilaksh Singh Reen",
            phone_number="0000000000",
            organization=org_0,
            role="admin"
        )

        user_4 = CustomUser.objects.create_user(
            email="foo@bar.com",
            username="foo_bar",
            password="1234",
            full_name="Foo Bar",
            phone_number="0000000000",
            organization=org_1,
            role="admin"
        )

        org_1_item_categories = []
        for i in range(1, 1 + NUM_ITEM_CATEGORIES_PER_ORG):
            new_item_category = ItemCategory.objects.create(
                name=f"Item Category {i}",
                organization=org_0
            )
            org_1_item_categories.append(new_item_category)
        
        org_1_item_subcategories = []
        for i, item_category_object in enumerate(org_1_item_categories):
            for j in range(1, 1 + NUM_ITEM_SUBCATEGORIES_PER_ITEM_CATEGORY):
                new_item_subcategory = ItemSubCategory.objects.create(
                    name=f"Item Sub Category {i}_{j}",
                    category=item_category_object,
                    organization=org_0
                )
                org_1_item_subcategories.append(new_item_subcategory)
        
        org_1_items = []
        for i, item_subcategory_object in enumerate(org_1_item_subcategories):
            for j in range(1, 1 + NUM_ITEMS_PER_ITEM_SUBCATEGORY):
                random_tags = sample(DEFAULT_TAGS, randint(0, len(DEFAULT_TAGS)))
                random_usage_tags = sample(DEFAULT_USAGE_TAGS, randint(0, len(DEFAULT_USAGE_TAGS)))

                new_item = Item.objects.create(
                    name=f"Item {j}",
                    sub_category=item_subcategory_object,
                    category=item_subcategory_object.category,
                    organization=org_0,
                    stock_keeping_unit=f"Item_sku_{i}_{j}",
                    cost=str(round(uniform(10.0, 1000.0), 2)),
                    available_stock=randint(50, 250),
                    tags=json_dumps(random_tags),
                    usage_tags=json_dumps(random_usage_tags),
                )
                org_1_items.append(new_item)
