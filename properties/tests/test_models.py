from core.test_base.test_models import TestPropertiesModelsBase


class LocationTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):
        self.location = self.create_location()

    def test_get_name(self):
        """Validate retrieving the name of the location in each language"""

        self.assertEqual(self.location.get_name("es"), self.location.name.es)
        self.assertEqual(self.location.get_name("en"), self.location.name.en)


class CategoryTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):
        self.category = self.create_category()

    def test_get_name(self):
        """Validate retrieving the name of the category in each language"""

        self.assertEqual(self.category.get_name("es"), self.category.name.es)
        self.assertEqual(self.category.get_name("en"), self.category.name.en)


class ShortDescriptionTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):
        self.short_description = self.create_short_description()

    def test_get_description(self):
        """Validate retrieving the description of the short
        description in each language"""

        self.assertEqual(
            self.short_description.get_description("es"),
            self.short_description.description.es,
        )
        self.assertEqual(
            self.short_description.get_description("en"),
            self.short_description.description.en,
        )


class SellerTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):
        self.seller = self.create_seller()

    def test_get_full_name(self):
        """Validate retrieving the full name of the seller"""

        self.assertEqual(
            self.seller.get_full_name(),
            f"{self.seller.first_name} {self.seller.last_name}",
        )


class PropertyTestCase(TestPropertiesModelsBase):
    """Validate model custom methods"""

    def setUp(self):

        # Property required models
        self.property = self.create_property()

    def test_get_description(self):
        """Validate retrieving the description of the property in each language"""

        self.assertEqual(
            self.property.get_description("es"), self.property.description_es
        )
        self.assertEqual(
            self.property.get_description("en"), self.property.description_en
        )

    def test_get_price_str(self):
        """Validate retrieving the price as a string"""

        self.assertEqual(self.property.get_price_str(), "1,000.00")

    def test_get_short_description(self):
        """Validate retrieving the short description of the property in each language"""

        self.assertEqual(
            self.property.short_description.get_description("es"),
            self.property.short_description.description.es,
        )
        self.assertEqual(
            self.property.short_description.get_description("en"),
            self.property.short_description.description.en,
        )
        
    def test_save_generate_slug(self):
        """Validate generating a slug for the property"""

        self.property.name = "this is á   test name -- **"
        self.property.save()
        self.assertEqual(self.property.slug, "this-is-a-test-name")
        
    def test_save_google_maps_no_change_src(self):
        """ Validate that the google maps src is not changed if it is already correct """
        
        src = "https://www.google.com/maps/embed?pb=!1m18!12121gysart6126521h..."
        self.property.google_maps_src = src
        self.property.save()
        
        self.assertEqual(self.property.google_maps_src, src)
        
    def test_save_google_maps_change_src(self):
        """ Validate that the google maps src is changed if it is not correct """
        
        src = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d118464"
        iframe = f"""
            <iframe
                src="{src}"
                width="600"
                height="450"
                style="border:0;"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
            >
            </iframe>
        """
        self.property.google_maps_src = iframe
        self.property.save()
        
        self.assertEqual(self.property.google_maps_src, src)
        
    def test_save_google_maps_invalid_src(self):
        """ Validate that the google maps src is not changed if it is not
        a google maps link """
        
        src = "https://www.no-google.no-com/no-maps/embed?pb=!1m18!1m12!1m3!1d118464"

        self.property.google_maps_src = src
        
        with self.assertRaises(ValueError):
            self.property.save()
            
        self.assertNotEqual(self.property.google_maps_src, src)
        
        
