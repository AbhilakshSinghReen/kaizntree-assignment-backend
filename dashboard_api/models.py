from json import loads as json_loads, dumps as json_dumps

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from dashboard_api.model_managers import (
    CustomUserManager,
)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    roles = models.TextField(default=json_dumps(["admin"]))
    item_tags = models.TextField(default=json_dumps(["shopify", "xero"]))
    item_usage_tags = models.TextField(default=json_dumps(["assembly", "component", "purchasable", "saleable", "bundle"]))
    
    def clean(self):
        super().clean()

        json_list_fields = ["roles", "item_tags", "item_usage_tags"]
        for field_name in json_list_fields:
            try:
                parsed_list = json_loads(getattr(self, field_name))
                if not isinstance(parsed_list, list):
                    raise ValidationError(f"\"{field_name}\" must be a list.")
            except ValueError:
                raise ValidationError(f"Invalid JSON format for \"{field_name}\".")
        
        roles_list = json_loads(self.roles)
        if not "admin" in roles_list:
            raise ValidationError("Organization must have an \"admin\" role.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255, blank=False)
    username = models.CharField(unique=True, max_length=255, blank=False)
    full_name = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=False)
    role = models.CharField(max_length=255, blank=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', 'full_name', 'phone_number']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super().clean()

        user_organization_roles = json_loads(self.organization.roles)
        if self.role not in user_organization_roles:
            raise ValidationError(f"User role ({self.role}) does not exist in the organization's roles.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username


class ItemCategory(models.Model):
    name = models.CharField(max_length=255, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ('organization', 'name')

    def __str__(self):
        return self.name


class ItemSubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('organization', 'category', 'name')

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255, blank=False)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, blank=False)
    sub_category = models.ForeignKey(ItemSubCategory, on_delete=models.CASCADE, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=False)

    description = models.TextField(default="", blank=True)
    stock_keeping_unit = models.CharField(unique=True, max_length=255, blank=False)

    allocated_to_sales = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])
    allocated_to_builds = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])
    
    available_stock = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])
    incoming_stock = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])
    minimum_stock = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])
    desired_stock = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])

    stock_status = models.CharField(default="out_of_stock", max_length=64,blank=False)
    
    on_build_order = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])
    can_build = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])

    cost = models.DecimalField(max_digits=19, decimal_places=4, validators=[MinValueValidator(0)])
    # cost = MoneyField(max_digits=19, decimal_places=4, default_currency='USD', validators=[MinMoneyValidator(0)])

    tags = models.TextField(default=json_dumps([]))
    usage_tags = models.TextField(default=json_dumps([]))

    class Meta:
        unique_together = ('organization', 'category', 'sub_category', 'name')

    def clean(self):
        super().clean()

        json_list_fields = ["tags", "usage_tags"]
        for field_name in json_list_fields:
            try:
                parsed_list = json_loads(getattr(self, field_name))
                if not isinstance(parsed_list, list):
                    raise ValidationError(f"\"{field_name}\" must be a list.")
            except ValueError:
                raise ValidationError(f"Invalid JSON format for \"{field_name}\".")

        if self.tags:
            item_tags = json_loads(self.tags)
            organization_item_tags = json_loads(self.organization.item_tags)
            undefined_item_tags = []

            for tag in item_tags:
                if not tag in organization_item_tags:
                    undefined_item_tags.append(tag)
            
            if len(undefined_item_tags) > 0:
                raise ValidationError(
                    f"Tags {', '.join(undefined_item_tags)} are "
                    "not defined in the item's organization."
                )
        
        if self.usage_tags:
            item_usage_tags = json_loads(self.usage_tags)
            organization_usage_tags = json_loads(self.organization.item_usage_tags)
            undefined_usage_tags = []

            for tag in item_usage_tags:
                if not tag in organization_usage_tags:
                    undefined_usage_tags.append(tag)

            if len(undefined_usage_tags) > 0:
                raise ValidationError(
                    f"Usage tags {', '.join(undefined_usage_tags)} are "
                    "not defined in the item's organization."
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Build(models.Model):
    pass


class SalesOrder(models.Model):
    pass
