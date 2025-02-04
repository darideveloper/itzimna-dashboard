from rest_framework import viewsets

from properties import serializers
from properties import models


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """ Api viewset for Property model """
    queryset = models.Property.objects.filter(active=True)
    serializer_class = serializers.PropertySerializer