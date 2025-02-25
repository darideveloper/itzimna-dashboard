from rest_framework import viewsets


from leads import models
from leads import serializers


class LeadView(viewsets.ModelViewSet):
    # JTW authentication is required
    queryset = models.Lead.objects.all()
    serializer_class = serializers.LeadSerializer
    http_method_names = ['post']