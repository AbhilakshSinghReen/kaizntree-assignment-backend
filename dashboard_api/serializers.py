from rest_framework import serializers

from dashboard_api.models import (
    CustomUser,
)


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    organization_id = serializers.IntegerField()
    
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'password',
            'email',
            'full_name',
            'phone_number',
            'organization_id',
            'role',
        )
        # exclude = ('organization',)
        read_only_fields = ('id',)
