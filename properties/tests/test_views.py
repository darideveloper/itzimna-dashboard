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
                    result["description"],
                    getattr(property, f"description_{lang}")
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
