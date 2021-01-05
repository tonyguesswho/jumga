from rest_framework import serializers
from apps.seller.models import Seller


class SellerSerializer(serializers.ModelSerializer):

    def validate_url(self, value):
        """
        Check that the url is valid
        """
        start_str = ['-', '_']
        if value[0] in start_str or value[-1] in start_str:
            raise serializers.ValidationError("Invalid url")
        for i, v in enumerate(value):
            if v in start_str and value[i+1] in start_str:
                raise serializers.ValidationError("Invalid url")
        return value.lower()

    def create(self, validated_data):
        return super(SellerSerializer, self).create(validated_data)

    class Meta:
        model = Seller
        fields = ['id', 'name', 'description', 'is_active',
                  'url', 'uuid', 'user',  'created_at', 'updated_at']
        read_only_fields = ["user"]
