from rest_framework import serializers
from apps.delivery.models import Rider


class RiderSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = Rider
        fields = '__all__'
