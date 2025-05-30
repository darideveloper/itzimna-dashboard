from rest_framework import serializers

from core.serializers import BaseModelTranslationsSerializer
from content import models


class BestDevelopmentsImageSerializer(BaseModelTranslationsSerializer):
    """Serializer for BestDevelopmentsImage model"""

    alt_text = serializers.SerializerMethodField()

    class Meta:
        model = models.BestDevelopmentsImage
        fields = "__all__"

    def get_alt_text(self, obj) -> str:
        """Retrieve alt text in the correct language

        Returns:
            str: Alt text in the correct language
        """
        return obj.get_alt_text(self.__get_language__()) if obj.alt_text else ""
