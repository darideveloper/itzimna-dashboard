from rest_framework import viewsets

from properties import serializers
from properties import models


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """ Api viewset for Property model """
    queryset = models.Property.objects.filter(active=True)
    
    def get_queryset(self):
        """ filter with get parameters """
        queryset = models.Property.objects.filter(active=True).order_by('-updated_at')
        
        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured is not None:
            queryset = queryset.filter(featured=True)
            
        # return queryset
        return queryset
    
    def get_serializer_class(self, *args, **kwargs):
        """ Return serializer class """
        if "details" in self.request.query_params:
            return serializers.PropertyDetailSerializer
        if "only-names" in self.request.query_params:
            return serializers.PropertyNameSerializer
        return serializers.PropertySummarySerializer