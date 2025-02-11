from rest_framework import status
from core.test_base.test_views import TestPropertiesViewsBase


class PropertyViewSetTestCase(TestPropertiesViewsBase):

    def setUp(self):
        # Set endpoint
        super().setUp(endpoint="/api/properties/")

    def test_get(self):
        """Test authenticated user get request in eng and es
        to render properti main data
        """

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
                    result["location"], getattr(property.location.name, lang)
                )
                self.assertEqual(
                    result["seller"],
                    f"{property.seller.first_name} {property.seller.last_name}",
                )
                self.assertEqual(
                    result["category"], getattr(property.category.name, lang)
                )
                self.assertEqual(result["price"], property.get_price_str())
                self.assertEqual(result["meters"], f"{property.meters}.00")
                self.assertEqual(
                    result["short_description"],
                    getattr(property.short_description.description, lang),
                )

    def test_property_banner_with_single_image(self):
        """valdiate banner in response with single image in property"""

        # Delete second property
        self.property_2.delete()

        # Add images to property
        image_name = "test.webp"
        property_image = self.create_property_image(
            property=self.property_1, image_name=image_name
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
            result["banner"]["url"],
        )
        self.assertIn(".webp", result["banner"]["url"])
        self.assertEqual(result["banner"]["alt"], property_image.get_alt_text("es"))

    def test_property_banner_with_many_images(self):
        """Validate response with property images"""

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
        result = json_data["results"][1]
        self.assertIn(
            f"/media/property-images/{image_names[0].replace('.webp', '')}",
            result["banner"]["url"],
        )
        self.assertIn(".webp", result["banner"]["url"])
        self.assertEqual(result["banner"]["alt"], property_images[0].get_alt_text("es"))

    def test_inactive_property_not_in_response(self):
        """Validate that inactive properties are not in response"""

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

    def test_featured_property_in_response(self):
        """Validate that featured properties are in response"""

        # Deactivate property
        self.property_1.featured = True
        self.property_1.save()

        # Validate response
        response = self.client.get(
            self.endpoint + "?featured=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )
        json_data = response.json()
        self.assertEqual(json_data["count"], 1)
        self.assertEqual(len(json_data["results"]), 1)

    def test_page_size_1(self):
        """Test if the page size is set to 1"""

        self.endpoint += "?page-size=1"

        # Make request
        response = self.client.get(
            self.endpoint,
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_order_by_updated_at(self):
        """Test if the properties are ordered by updated_at"""

        # Update property 1
        self.property_1.name = "Updated name"
        self.property_1.save()

        # Validate property 1 is first
        response = self.client.get(
            self.endpoint,
            HTTP_ACCEPT_LANGUAGE="es",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"][0]["name"], self.property_1.name)

        # Update property 2
        self.property_2.name = "Updated name 2"
        self.property_2.save()

        # Validate property 2 is first
        response = self.client.get(
            self.endpoint,
            HTTP_ACCEPT_LANGUAGE="es",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"][0]["name"], self.property_2.name)

    def test_get_only_names(self):
        """Test if only names are returned"""

        # Make request
        response = self.client.get(
            self.endpoint + "?only-names=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response
        json_data = response.json()
        self.assertEqual(json_data["count"], 2)
        self.assertIsNone(json_data["next"])
        self.assertIsNone(json_data["previous"])
        self.assertEqual(len(json_data["results"]), 2)

        # Validate each result
        properties = [self.property_2, self.property_1]
        for property in properties:
            property_index = properties.index(property)
            data = {
                "id": property.id,
                "name": property.name,
            }
            self.assertEqual(json_data["results"][property_index], data)

    def test_get_details(self):
        """Get properties full data"""

        # Make request
        for lang in self.langs:
            response = self.client.get(
                self.endpoint + "?details=true",
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
                    result["location"], getattr(property.location.name, lang)
                )
                self.assertEqual(
                    result["seller"],
                    f"{property.seller.first_name} {property.seller.last_name}",
                )
                self.assertEqual(
                    result["category"], getattr(property.category.name, lang)
                )
                self.assertEqual(result["price"], property.get_price_str())
                self.assertEqual(result["meters"], f"{property.meters}.00")
                self.assertEqual(result["active"], property.active)
                self.assertEqual(
                    result["short_description"],
                    getattr(property.short_description.description, lang),
                )
                self.assertEqual(
                    result["description"],
                    property.get_description(lang),
                )
                self.assertEqual(result["featured"], property.featured)
                self.assertEqual(
                    result["created_at"].split(".")[0],
                    property.created_at.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
                )
                self.assertEqual(
                    result["updated_at"].split(".")[0],
                    property.updated_at.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
                )
