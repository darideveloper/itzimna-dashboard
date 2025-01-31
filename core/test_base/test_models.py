import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from properties import models as properties_models
from translations import models as translations_models


class TestPropertiesModelsBase(TestCase):
    """Validate model custom methods"""

    def create_translation(
        self, key,
        es: str = "Traducción de prueba",
        en: str = "Test translation"
    ) -> translations_models.Translation:
        """Create a translation object

        Args:
            key (str): Translation key
            es (str): Spanish translation
            en (str): English translation

        Returns:
            Translation: Translation object created
        """

        return translations_models.Translation.objects.create(
            key=key,
            es=es,
            en=en,
        )

    def create_location(
        self,
        name_es: str = "Ubicación de prueba",
        name_en: str = "Test location",
        details: str = ""
    ) -> properties_models.Location:
        """ Create a location object
        
        Args:
            name_es (str): Spanish location name
            name_en (str): English location name
            details (str): Location details
            
        Returns:
            properties_models.Location: Location object created
        """

        return properties_models.Location.objects.create(
            name=self.create_translation("location_test", name_es, name_en),
            details=details,
        )

    def create_category(
        self,
        name_es: str = "Categoria de prueba",
        name_en: str = "Test category",
        details: str = ""
    ) -> properties_models.Category:
        """ Create a category object
        
        Args:
            name_es (str): Spanish category name
            name_en (str): English category name
            details (str): Category details
            
        Returns:
            properties_models.Category: Category object created
        """

        return properties_models.Category.objects.create(
            name=self.create_translation("category_test", name_es, name_en),
            details=details,
        )

    def create_seller(
        self,
        first_name: str = "Test",
        last_name: str = "Seller",
        phone: str = "123456789"
    ) -> properties_models.Seller:
        """ Create a seller object
        
        Args:
            first_name (str): Seller first name
            last_name (str): Seller last name
            phone (str): Seller phone
            
        Returns:
            properties_models.Seller: Seller object created
        """

        return properties_models.Seller.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        
    def create_company(
        self, name: str = "Company test"
    ) -> properties_models.Company:
        """ Create a company object
        
        Args:
            name (str): Company name
            
        Returns:
            properties_models.Company: Company object created
        """

        return properties_models.Company.objects.create(
            name=name,
        )

    def create_short_description(
        self,
        name: str = "short_description_test",
        es: str = "Descripción corta de prueba",
        en: str = "Test short description"
    ) -> properties_models.ShortDescription:
        """ Create a short description object
        
        Args:
            key (str): Short description key
            es (str): Spanish short description
            en (str): English short description
            
        Returns:
            properties_models.ShortDescription: Short description object created
        """

        return properties_models.ShortDescription.objects.create(
            description=self.create_translation(name, es, en),
            details="",
        )

    def create_property(
        self,
        name: str = "Property test",
        company: properties_models.Company = None,
        location: properties_models.Location = None,
        category: properties_models.Category = None,
        seller: properties_models.Seller = None,
        short_description: properties_models.ShortDescription = None,
        price: float = 1000,
        meters: float = 100,
        active: bool = True,
        description_es: str = "Descripción de la propiedad",
        description_en: str = "Property description",
    ) -> properties_models.Property:
        """ Create a property object
        
        Args:
            name (str): Property name
            company (properties_models.Company): Company object
            location (properties_models.Location): Location object
            category (properties_models.Category): Category object
            seller (properties_models.Seller): Seller object
            price (float): Property price
            meters (float): Property meters
            active (bool): Active property
            description_es (str): Spanish description
            description_en (str): English description
            
        Returns:
            properties_models.Property: Property object created
        """

        if not company:
            company = self.create_company()

        if not location:
            location = self.create_location()

        if not category:
            category = self.create_category()

        if not seller:
            seller = self.create_seller()
            
        if not short_description:
            short_description = self.create_short_description(
                name=f"short_description {name}"
            )

        return properties_models.Property.objects.create(
            name=name,
            company=company,
            location=location,
            seller=seller,
            category=category,
            price=price,
            meters=meters,
            active=active,
            description_es=description_es,
            description_en=description_en,
            short_description=short_description,
        )

    def create_property_image(
        self,
        property: properties_models.Property = None,
        image_name: str = "test.webp",
        alt_text_es: str = "Texto alternativo",
        alt_text_en: str = "Alt text",
        show_gallery: bool = True,
    ) -> properties_models.PropertyImage:
        """ Create a property image object
        
        Args:
            property (properties_models.Property): Property object
            image_name (str): Image source
            alt_text_es (str): Spanish alt text
            alt_text_en (str): English alt text
            show_gallery (bool): Show in gallery
            
        Returns:
            properties_models.PropertyImage: Property image object created
        """

        if not property:
            property = self.create_property()
            
        app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_path = os.path.dirname(app_path)
        media_path = os.path.join(project_path, 'media')
        
        image_path = os.path.join(media_path, 'property-images', image_name)
        image_file = SimpleUploadedFile(
            name=image_name,
            content=open(image_path, 'rb').read(),
            content_type='image/webp'
        )

        property_image = properties_models.PropertyImage.objects.create(
            property=property,
            alt_text=self.create_translation(
                f"alt_text_test {image_name}", alt_text_es, alt_text_en
            ),
            show_gallery=show_gallery,
        )
        property_image.image = image_file
        property_image.save()
        
        return property_image