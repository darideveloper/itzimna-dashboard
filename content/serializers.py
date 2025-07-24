from rest_framework import serializers

from core.serializers import BaseSearchSerializer
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


class SearchLinkSearchSerializer(BaseSearchSerializer):
    """Api serializer for Post model in search endpoint"""

    # Calculated fields
    extra = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source="updated_at")
    type = serializers.CharField(default="link")
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    # overwrite model
    class Meta(BaseSearchSerializer.Meta):
        model = models.SearchLink

    def get_title(self, obj) -> str:
        """Retrieve title in the correct language

        Returns:
            str: Title in the correct language
        """
        return obj.get_title(self.__get_language__()) if obj.title else ""

    def get_description(self, obj) -> str:
        """Retrieve description in the correct language

        Returns:
            str: Description in the correct language
        """
        return obj.get_description(self.__get_language__()) if obj.description else ""

    def get_extra(self, obj) -> dict:
        """Retrieve extra fields (author) as dict"""

        return {}
