from rest_framework import serializers

from dashboard_api.models import (
    CustomUser,
    Item,
    ItemCategory,
    ItemSubCategory
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
        read_only_fields = ('id',)


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = '__all__'

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError('Username is required')
        
        if not data.get('organization'):
            raise serializers.ValidationError('organization is required')

        return data


class ItemSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSubCategory
        fields = '__all__'

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError('Username is required')
        
        if not data.get('category'):
            raise serializers.ValidationError('category is required')
        
        if not data.get('organization'):
            raise serializers.ValidationError('organization is required')

        return data


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
