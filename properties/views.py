from rest_framework import viewsets

from properties import serializers
from properties import models


class PropertyViewSet(viewsets.ModelViewSet):
    """ Api viewset for Property model """
    queryset = models.Property.objects.all()
    serializer_class = serializers.PropertySerializer