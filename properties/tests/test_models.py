from core.test_base.test_models import TestPropertiesModelsBase


class LocationTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):
        self.location = self.create_location()

    def test_get_name(self):
        """Validate retrieving the name of the location in each language"""

        self.assertEqual(
            self.location.get_name("es"),
            self.location.name.es
        )
        self.assertEqual(
            self.location.get_name("en"),
            self.location.name.en
        )


class CategoryTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):
        self.category = self.create_category()

    def test_get_name(self):
        """Validate retrieving the name of the category in each language"""

        self.assertEqual(
            self.category.get_name("es"),
            self.category.name.es
        )
        self.assertEqual(
            self.category.get_name("en"),
            self.category.name.en
        )


class SellerTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):
        self.seller = self.create_seller()
        
    def test_get_full_name(self):
        """Validate retrieving the full name of the seller"""

        self.assertEqual(
            self.seller.get_full_name(),
            f"{self.seller.first_name} {self.seller.last_name}"
        )


class PropertyTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):

        # Property required models
        self.property = self.create_property()

    def test_get_description(self):
        """Validate retrieving the description of the property in each language"""

        self.assertEqual(
            self.property.get_description("es"),
            self.property.description_es
        )
        self.assertEqual(
            self.property.get_description("en"),
            self.property.description_en
        )

    def test_get_price_str(self):
        """Validate retrieving the price as a string"""

        self.assertEqual(
            self.property.get_price_str(),
            "1,000.00"
        )
        
    def test_get_short_description(self):
        """Validate retrieving the short description of the property in each language"""

        self.assertEqual(
            self.property.get_short_description("es"),
            self.property.short_description.es
        )
        self.assertEqual(
            self.property.get_short_description("en"),
            self.property.short_description.en
        )