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


class SearchLinksSerializer(BaseModelTranslationsSerializer):
    """Serializer for SearchLinks model"""

    class Meta:
        model = models.SearchLinks
        fields = "__all__"
        
        
class SearchLinksSearchSerializer(BaseSearchSerializer):
    """ Api serializer for Post model in search endpoint """
    
    # Calculated fields
    image = serializers.URLField(source="image_url")
    extra = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source="updated_at")
    type = serializers.CharField(default="link")
    
    # overwrite model
    class Meta(BaseSearchSerializer.Meta):
        model = models.SearchLinks
        
    def get_extra(self, obj) -> dict:
        """Retrieve extra fields (author) as dict"""
        
        return {}