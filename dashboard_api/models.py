from json import loads as json_loads

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, full_name, phone_number, organization, role, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')
        
        if isinstance(organization, int):
            user = self.model(
                email=self.normalize_email(email),
                username=username,
                full_name=full_name,
                phone_number=phone_number,
                organization_id=organization,
                role=role,
                **extra_fields
            )
        else:
            user = self.model(
                email=self.normalize_email(email),
                username=username,
                full_name=full_name,
                phone_number=phone_number,
                organization=organization,
                role=role,
                **extra_fields
            )
        
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password, full_name, phone_number, organization, role, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, full_name, phone_number, organization, role, **extra_fields)

    def create_superuser(self, email, username, password, full_name, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, username, password, full_name, phone_number, organization=1, role="admin", **extra_fields)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    roles = models.TextField(default='foo this')

    def clean(self):
        super().clean()

        try:
            roles_list = json_loads(self.roles)

            if not isinstance(roles_list, list):
                raise ValidationError("Roles must be a list.")
            
            if not "admin" in roles_list:
                raise ValidationError("Organization must have an \"admin\" role.")
        except ValueError:
            raise ValidationError("Invalid JSON format for roles.")

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
