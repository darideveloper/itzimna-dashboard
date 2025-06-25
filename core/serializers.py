from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Call the parent method to generate tokens

        # Customize the response structure
        return {
            "status": "ok",
            "message": "generated",
            "data": data
        }
        

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Call the parent method to generate tokens

        # Customize the response structure
        return {
            "status": "ok",
            "message": "generated",
            "data": data
        }
        
        
# BASE SERIALIZERS

class BaseModelTranslationsSerializer(serializers.ModelSerializer):
    
    def __get_language__(self) -> str:
        """Retrieve language from the request context or default to 'es'

        Returns:
            str: Language code
        """
        request = self.context.get("request")
        return request.headers.get("Accept-Language", "es") if request else "es"


class BaseSearchSerializer(BaseModelTranslationsSerializer):
    """Base serializer for search endpoints"""
    
    class Meta:
        # dynamic model from chiild class
        model = None
        fields = (
            "id",
            "title",
            "image",
            "description",
            "extra",
            "date",
            "type",
        )