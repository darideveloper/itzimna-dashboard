from rest_framework import viewsets

from content import serializers
from content import models


class BestDevelopmentsImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.BestDevelopmentsImage.objects.all()
    serializer_class = serializers.BestDevelopmentsImageSerializer
    pagination_class = None