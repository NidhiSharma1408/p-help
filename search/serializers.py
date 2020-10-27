from rest_framework import serializers
from . import models

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DonationRequest
        fields = '__all__'

class DonationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DonationHistory
        fields = '__all__'