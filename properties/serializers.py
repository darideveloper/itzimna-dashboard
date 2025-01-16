from rest_framework import serializers

from properties import models


class PropertySerializer(serializers.ModelSerializer):
    """ Api serializer for Property model """
    
    # Get foreign fields
    company = serializers.CharField(source='company.name', read_only=True)
    location = serializers.CharField(source='location.name', read_only=True)
    seller = serializers.CharField(source='seller.get_full_name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = models.Property
        fields = '__all__'
        