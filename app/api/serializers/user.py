from rest_framework import serializers
from apps.user.models import User
from api.serializers.seller import SellerSerializer


class RegistrationSerilaizer(serializers.ModelSerializer):
    """Serilaizers registration request and creates user"""

    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)

    seller = SellerSerializer(required=False, many=False)

    class Meta:
        model = User

        fields = ['email', 'password', 'first_name', 'last_name', 'seller']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
