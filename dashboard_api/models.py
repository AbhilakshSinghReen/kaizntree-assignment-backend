from json import loads as json_loads

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    roles = models.JSONField(default='foo this')

    def clean(self):
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

