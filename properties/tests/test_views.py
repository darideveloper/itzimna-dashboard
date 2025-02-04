from rest_framework import status
from core.test_base.test_views import TestPropertiesViewsBase


class PropertyViewSetTestCase(TestPropertiesViewsBase):
    def setUp(self):
        # Set endpoint
        super().setUp(endpoint="/api/properties/")

    def test_unauthenticated_user_get(self):
        """Test unauthenticated user get request"""

        # Remove authentication
        self.client.logout()

        # Make request
        response = self.client.get(self.endpoint)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_get(self):
        """Test authenticated user get request in eng and es"""

        # Make request
        for lang in self.langs:
            response = self.client.get(
                self.endpoint,
                HTTP_ACCEPT_LANGUAGE=lang,
            )

            # Check response
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Validate response extra content
            json_data = response.json()
            self.assertEqual(json_data["count"], 2)
            self.assertIsNone(json_data["next"])
            self.assertIsNone(json_data["previous"])
            self.assertEqual(len(json_data["results"]), 2)

            # Loop results
            results = json_data["results"]
            properties = [self.property_1, self.property_2]
            for property in properties:
                
                # Validate each property
                result = list(
                    filter(lambda result: result["id"] == property.id, results)
                )[0]
                self.assertEqual(result["name"], property.name)
                self.assertEqual(
                    result["location"],
                    getattr(property.location.name, lang)
                )
                self.assertEqual(
                    result["seller"],
                    f"{property.seller.first_name} {property.seller.last_name}",
                )
                self.assertEqual(
                    result["category"],
                    getattr(property.category.name, lang)
                )
                self.assertEqual(result["price"], property.get_price_str())
                self.assertEqual(result["meters"], f"{property.meters}.00")
                self.assertEqual(result["active"], property.active)
                self.assertEqual(
                    result["short_description"],
                    getattr(property.short_description.description, lang)
                )
    
    def test_authenticated_user_post(self):
        """ Test that authenticated users can not post to the endpoint """
        
        self.validate_invalid_method("post")
        
    def test_authenticated_user_put(self):
        """ Test that authenticated users can not put to the endpoint """
        
        # add id to endpoint
        self.endpoint = f"{self.endpoint}1/"
        self.validate_invalid_method("put")
        
    def test_authenticated_user_patch(self):
        
        # add id to endpoint
        self.endpoint = f"{self.endpoint}1/"
        self.validate_invalid_method("patch")

    def test_property_banner_with_single_image(self):
        """ valdiate banner in response with single image in property """
        
        # Delete second property
        self.property_2.delete()
        
        # Add images to property
        image_name = "test.webp"
        property_image = self.create_property_image(
            property=self.property_1,
            image_name=image_name
        )
            
        # Validate banner
        response = self.client.get(
            self.endpoint,
            HTTP_ACCEPT_LANGUAGE="es",
        )
        json_data = response.json()
        result = json_data["results"][0]
        self.assertIn(
            f"/media/property-images/{image_name.replace('.webp', '')}",
            result["banner"]["url"]
        )
        self.assertIn(".webp", result["banner"]["url"])
        self.assertEqual(result["banner"]["alt"], property_image.get_alt_text("es"))

    def test_property_banner_with_many_images(self):
        """ Validate response with property images """
        
        # Add images to property
        property_images = []
        image_names = ["test.webp", "test2.webp"]
        for image_name in image_names:
            property_images.append(
                self.create_property_image(
                    property=self.property_1,
                    image_name=image_name,
                )
            )
            
        # Validate banner
        response = self.client.get(
            self.endpoint,
            HTTP_ACCEPT_LANGUAGE="es",
        )
        json_data = response.json()
        result = json_data["results"][0]
        self.assertIn(
            f"/media/property-images/{image_names[0].replace('.webp', '')}",
            result["banner"]["url"]
        )
        self.assertIn(".webp", result["banner"]["url"])
        self.assertEqual(result["banner"]["alt"], property_images[0].get_alt_text("es"))
    
    def test_inactive_property_not_in_response(self):
        """ Validate that inactive properties are not in response """
        
        # Deactivate property
        self.property_1.active = False
        self.property_1.save()
        
        # Validate response
        response = self.client.get(
            self.endpoint,
            HTTP_ACCEPT_LANGUAGE="es",
        )
        json_data = response.json()
        self.assertEqual(json_data["count"], 1)
        self.assertEqual(len(json_data["results"]), 1)