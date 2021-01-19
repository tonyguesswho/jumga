from rest_framework import serializers
from apps.user.models import Account


class AccountSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'
