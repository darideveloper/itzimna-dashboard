from rest_framework import serializers

from properties import models
from utils.media import get_media_url


class PropertySerializer(serializers.ModelSerializer):
    """Api serializer for Property model"""

    # Get foreign fields
    company = serializers.CharField(source="company.name", read_only=True)
    location = serializers.SerializerMethodField()
    seller = serializers.CharField(source="seller.get_full_name", read_only=True)
    category = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    meters = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = models.Property

        # Return all fields except for description_es and description_en
        exclude = ("description_es", "description_en")

    def get_language(self) -> str:
        """Retrieve language from the request context or default to 'es'

        Returns:
            str: Language code
        """
        request = self.context.get("request")
        return request.headers.get("Accept-Language", "es") if request else "es"

    def get_location(self, obj) -> str:
        """Retrieve location name in the correct language

        Returns:
            str: Location name in the correct language
        """

        return obj.location.get_name(self.get_language())

    def get_description(self, obj) -> str:
        """Retrieve description in the correct language

        Returns:
            str: Description in the correct language
        """
        return obj.get_description(self.get_language())

    def get_banner(self, obj) -> str:
        """Retrieve banner url

        Returns:
            str: Banner url
        """

        all_images = models.PropertyImage.objects.filter(property=obj)
        try:
            banner = all_images[0]
            banner_url = get_media_url(banner.image)
            banner_alt = banner.get_alt_text(self.get_language())
        except Exception:
            banner_url = ""
            banner_alt = ""
            
        return {"url": banner_url, "alt": banner_alt}

    def get_price(self, obj) -> str:
        """Retrieve price in correct format: 1,000,000.00

        Returns:
            str: Price in the correct format
        """

        return obj.get_price_str()
    
    def get_category(self, obj) -> str:
        """Retrieve category name in the correct language

        Returns:
            str: Category name in the correct language
        """

        return obj.category.get_name(self.get_language())
    
    def get_short_description(self, obj) -> str:
        """Retrieve short description in the correct language

        Returns:
            str: Short description in the correct language
        """

        return obj.short_description.get_description(self.get_language())