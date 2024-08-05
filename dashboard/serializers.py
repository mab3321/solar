from rest_framework import serializers
from .models import Business, Service, UserIntegration


class BusinessNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('business_name',)

class BusinessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('business_name','industry', 'stage')


class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'category', 'resource')

class UserIntegrationSerializer(serializers.ModelSerializer):
    service = IntegrationSerializer()
    class Meta:
        model = UserIntegration
        fields = ('id', 'service', 'business_id', 'user_id', 'status')