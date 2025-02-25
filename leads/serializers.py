from rest_framework import serializers
from leads import models


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lead
        fields = "__all__"