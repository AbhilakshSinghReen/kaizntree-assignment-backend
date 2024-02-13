from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, full_name, phone_number, organization, role, **extra_fields):
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
        user.save(using=self.db)
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
