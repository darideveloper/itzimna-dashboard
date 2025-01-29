from django.test import TestCase

from properties import models as properties_models
from translations import models as translations_models


class ModelsTestCase(TestCase):
    """Validate model custom methods"""

    def create_translation(
        self, key, es: str = "", en: str = ""
    ) -> translations_models.Translation:
        """Create a translation object

        Args:
            key (str): Translation key
            es (str): Spanish translation
            en (str): English translation

        Returns:
            Translation: Translation object created
        """

        if not es:
            es = "Traducción de prueba"

        if not en:
            en = "Test translation"

        return translations_models.Translation.objects.create(
            key=key,
            es=es,
            en=en,
        )

    def create_location(
        self, name_es: str = "", name_en: str = "", details: str = ""
    ) -> properties_models.Location:
        """Create a location object"""

        if not name_es:
            name_es = "Ubicación de prueba"

        if not name_en:
            name_en = "Test location"

        return properties_models.Location.objects.create(
            name=self.create_translation("location_test", name_es, name_en),
            details=details,
        )

    def create_category(
        self, name_es: str = "", name_en: str = "", details: str = ""
    ) -> properties_models.Category:
        """Create a category object"""

        if not name_es:
            name_es = "Categoría de prueba"

        if not name_en:
            name_en = "Test category"

        return properties_models.Category.objects.create(
            name=self.create_translation("category_test", name_es, name_en),
            details=details,
        )

    def create_seller(
        self, first_name: str = "", last_name: str = "", phone: str = "123456789"
    ) -> properties_models.Seller:
        """Create a seller object"""

        if not first_name:
            first_name = "Test"

        if not last_name:
            last_name = "Seller"

        if not phone:
            phone = "123456789"

        return properties_models.Seller.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

    def create_property(
        self,
        name: str = "Property test",
        company: properties_models.Company = None,
        location: properties_models.Location = None,
        category: properties_models.Category = None,
        seller: properties_models.Seller = None,
        price: float = 1000,
        meters: float = 100,
        active: bool = True,
        description_es: str = "",
        description_en: str = "",
    ) -> properties_models.Property:
        """Create a property object"""

        if not company:
            company = properties_models.Company.objects.create()

        if not location:
            location = self.create_location()

        if not category:
            category = self.create_category()

        if not seller:
            seller = self.create_seller()

        if not description_es:
            description_es = "Descripción de la propiedad"

        if not description_en:
            description_en = "Property description"

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
        )
