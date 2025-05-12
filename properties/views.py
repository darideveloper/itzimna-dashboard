from rest_framework import viewsets

from properties import serializers
from properties import models


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """ Api viewset for Property model """
    queryset = models.Property.objects.filter(active=True)
    serializer_class = serializers.PropertyListItemSerializer
    
    def get_queryset(self):
        """ filter with get parameters """
        queryset = models.Property.objects.filter(active=True).order_by('-updated_at')
        
        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured is not None:
            queryset = queryset.filter(featured=True)
            
        # Filter by location
        location = self.request.query_params.get('ubicacion', None)
        if location is not None:
            queryset = queryset.filter(location__id=location)
            
        size_from = self.request.query_params.get('metros-desde', None)
        size_to = self.request.query_params.get('metros-hasta', None)
        if size_from is not None and size_to is not None:
            queryset = queryset.filter(meters__gte=size_from, meters__lte=size_to)
            
        price_from = self.request.query_params.get('precio-desde', None)
        price_to = self.request.query_params.get('precio-hasta', None)
        if price_from is not None and price_to is not None:
            queryset = queryset.filter(price__gte=price_from, price__lte=price_to)
            
        # return queryset
        return queryset
    
    def get_serializer_class(self, *args, **kwargs):
        """ Return serializer class """
        if "details" in self.request.query_params:
            return serializers.PropertyDetailSerializer
        if "summary" in self.request.query_params:
            return serializers.PropertySummarySerializer
        return self.serializer_class


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """ Api viewset for Location model """
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    pagination_class = None
    
    
class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """ Api viewset for Company model """
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySummarySerializer

    def get_serializer_class(self, *args, **kwargs):
        """ Return serializer class """
        if "details" in self.request.query_params:
            return serializers.CompanyDetailSerializer
        return self.serializer_class
    