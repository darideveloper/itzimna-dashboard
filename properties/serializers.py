from rest_framework import serializers

from properties import models
from utils.media import get_media_url
from utils.whatsapp import get_whatsapp_link
from core.serializers import BaseModelTranslationsSerializer


class SellerSerializer(serializers.ModelSerializer):
    """Serializer for Seller model"""
    
    whatsapp = serializers.SerializerMethodField()

    class Meta:
        model = models.Seller
        fields = "__all__"

    def get_whatsapp(self, obj) -> str:
        """Retrieve whatsapp url

        Returns:
            str: Whatsapp url
        """
        
        if obj.has_whatsapp:
            return get_whatsapp_link(obj.phone)
        else:
            return ""
        
        
class LocationSerializer(BaseModelTranslationsSerializer):
    """Serializer for Location model"""
    
    name = serializers.SerializerMethodField()

    class Meta:
        model = models.Location
        fields = ('id', 'name')
        
    def get_name(self, obj) -> str:
        """Retrieve details in the correct language

        Returns:
            str: Details in the correct language
        """

        return obj.get_name(self.__get_language__())
    
    
class TagSerializer(BaseModelTranslationsSerializer):
    """Serializer for Tag model"""
    
    name = serializers.SerializerMethodField()

    class Meta:
        model = models.Tag
        fields = ('id', 'name')
        
    def get_name(self, obj) -> str:
        """Retrieve details in the correct language

        Returns:
            str: Details in the correct language
        """

        return obj.get_name(self.__get_language__())


class PropertyListItemSerializer(BaseModelTranslationsSerializer):
    """Api serializer for Property model"""

    # Calculates fields
    company = serializers.CharField(source="company.name", read_only=True)
    location = serializers.SerializerMethodField()
    seller = serializers.CharField(source="seller.get_full_name", read_only=True)
    category = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    short_description = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    meters = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = models.Property

        # Return all fields except for description_es and description_en
        exclude = [
            "description_es",
            "description_en",
            "active",
            "created_at",
            "updated_at",
            "featured",
        ]

    def get_location(self, obj) -> str:
        """Retrieve location name in the correct language

        Returns:
            str: Location name in the correct language
        """

        return obj.location.get_name(self.__get_language__())

    def get_banner(self, obj) -> str:
        """Retrieve banner url

        Returns:
            str: Banner url
        """

        all_images = models.PropertyImage.objects.filter(property=obj)
        try:
            banner = all_images[0]
            banner_url = get_media_url(banner.image)
            banner_alt = banner.get_alt_text(self.__get_language__())
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

        return obj.category.get_name(self.__get_language__())

    def get_short_description(self, obj) -> str:
        """Retrieve short description in the correct language

        Returns:
            str: Short description in the correct language
        """

        return obj.short_description.get_description(self.__get_language__())

    def get_description(self, obj) -> str:
        """Retrieve description in the correct language

        Returns:
            str: Description in the correct language
        """

        return obj.get_description(self.__get_language__())
    

class PropertyDetailSerializer(PropertyListItemSerializer):
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    seller = SellerSerializer()
    
    class Meta:
        model = models.Property
        exclude = ["active", "description_es", "description_en"]

    def get_images(self, obj) -> list:
        """Retrieve all images for the property

        Returns:
            list: List of images
        """

        all_images = models.PropertyImage.objects.filter(property=obj)
        images = []
        for image in all_images:
            image_url = get_media_url(image.image)
            image_alt = image.get_alt_text(self.__get_language__())
            images.append({
                "id": image.id,
                "url": image_url,
                "alt": image_alt
            })
        return images

    def get_description(self, obj) -> str:
        """Retrieve description in the correct language

        Returns:
            str: Description in the correct language
        """

        return obj.get_description(self.__get_language__())
    

class PropertySummarySerializer(BaseModelTranslationsSerializer):
    """Return only the property's names"""
    
    location = serializers.SerializerMethodField()
    company = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = models.Property
        fields = ("id", "name", "slug", "updated_at", "company", "location")
        page_size = 1000
        
    def get_location(self, obj) -> str:
        """Retrieve location name in the correct language

        Returns:
            str: Location name in the correct language
        """

        return obj.location.get_name(self.__get_language__())