from rest_framework import status
from core.test_base.test_views import TestPropertiesViewsBase

from properties import models
from utils.whatsapp import get_whatsapp_link


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

                # Validate each general property
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
                self.assertIn("google.com/maps", result["google_maps_src"])

                # Validate tags
                tags_models = property.tags.all()
                self.assertEqual(len(result["tags"]), tags_models.count())
                for tag_models in tags_models:
                    tag_result = list(
                        filter(lambda tag: tag["id"] == tag_models.id, result["tags"])
                    )[0]
                    self.assertEqual(tag_result["name"], getattr(tag_models.name, lang))

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

    def test_get_summary(self):
        """get summary data with serializer PropertyNameSerializer"""

        # Make request
        response = self.client.get(
            self.endpoint + "?summary=true",
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

            # Format date time
            datetime = property.updated_at.astimezone().strftime("%Y-%m-%dT%H:%M:%S")

            # Get property data from api
            property_data = json_data["results"][property_index]

            self.assertEqual(property_data["id"], property.id)
            self.assertEqual(property_data["name"], property.name)
            self.assertEqual(property_data["slug"], property.slug)
            self.assertEqual(
                property_data["updated_at"].split(".")[0], datetime.split(".")[0]
            )
            self.assertEqual(
                property_data["location"], property.location.get_name("es")
            )
            self.assertEqual(property_data["company"], property.company.name)

    def test_get_details(self):
        """Get properties full data"""

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

                # Validate each property main data
                result = list(
                    filter(lambda result: result["id"] == property.id, results)
                )[0]
                self.assertEqual(result["name"], property.name)
                self.assertEqual(
                    result["location"], getattr(property.location.name, lang)
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
                self.assertEqual(result["featured"], property.featured)
                self.assertEqual(
                    result["created_at"].split(".")[0],
                    property.created_at.astimezone().strftime("%Y-%m-%dT%H:%M:%S"),
                )
                self.assertEqual(
                    result["updated_at"].split(".")[0],
                    property.updated_at.astimezone().strftime("%Y-%m-%dT%H:%M:%S"),
                )

                # Validate property description
                self.assertEqual(
                    result["description"],
                    property.get_description(lang),
                )

                # Validate property images
                property_images = models.PropertyImage.objects.filter(property=property)
                self.assertEqual(len(result["images"]), property_images.count())
                for image in property_images:
                    image_result = list(
                        filter(lambda img: img["id"] == image.id, result["images"])
                    )[0]
                    self.assertIn(
                        f"/media/{image.image.name}",
                        image_result["url"],
                    )
                    self.assertEqual(image_result["alt"], image.get_alt_text(lang))

                # Validate seller data
                seller = property.seller
                self.assertEqual(result["seller"]["id"], seller.id)
                self.assertEqual(result["seller"]["first_name"], seller.first_name)
                self.assertEqual(result["seller"]["last_name"], seller.last_name)
                self.assertEqual(result["seller"]["email"], seller.email)
                self.assertEqual(result["seller"]["phone"], seller.phone)
                self.assertEqual(result["seller"]["has_whatsapp"], seller.has_whatsapp)
                self.assertEqual(
                    result["seller"]["whatsapp"], get_whatsapp_link(seller.phone)
                )

    def test_get_details_single(self):
        """Test authenticated user get single property request"""

        # Make request
        response = self.client.get(
            f"{self.endpoint}{self.property_1.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate property data
        self.assertEqual(json_data["id"], self.property_1.id)
        self.assertEqual(json_data["name"], self.property_1.name)
        self.assertEqual(json_data["location"], self.property_1.location.get_name("es"))
        self.assertEqual(json_data["category"], self.property_1.category.name.es)
        self.assertEqual(json_data["price"], self.property_1.get_price_str())
        self.assertEqual(json_data["meters"], f"{self.property_1.meters}.00")
        self.assertEqual(
            json_data["short_description"],
            getattr(self.property_1.short_description.description, "es"),
        )
        self.assertEqual(json_data["featured"], self.property_1.featured)
        self.assertEqual(
            json_data["created_at"].split(".")[0],
            self.property_1.created_at.astimezone().strftime("%Y-%m-%dT%H:%M:%S"),
        )
        self.assertEqual(
            json_data["updated_at"].split(".")[0],
            self.property_1.updated_at.astimezone().strftime("%Y-%m-%dT%H:%M:%S"),
        )
        self.assertEqual(
            json_data["description"],
            self.property_1.get_description("es"),
        )

        # Validate property images
        property_images = models.PropertyImage.objects.filter(property=self.property_1)
        self.assertEqual(len(json_data["images"]), property_images.count())
        for image in property_images:
            image_result = list(
                filter(lambda img: img["id"] == image.id, json_data["images"])
            )[0]
            self.assertIn(
                f"/media/{image.image.name}",
                image_result["url"],
            )
            self.assertEqual(image_result["alt"], image.get_alt_text("es"))

        # Validate seller data
        self.assertEqual(json_data["seller"]["id"], self.property_1.seller.id)
        self.assertEqual(
            json_data["seller"]["first_name"], self.property_1.seller.first_name
        )
        self.assertEqual(
            json_data["seller"]["last_name"], self.property_1.seller.last_name
        )
        self.assertEqual(json_data["seller"]["email"], self.property_1.seller.email)
        self.assertEqual(json_data["seller"]["phone"], self.property_1.seller.phone)
        self.assertEqual(
            json_data["seller"]["has_whatsapp"], self.property_1.seller.has_whatsapp
        )
        self.assertEqual(
            json_data["seller"]["whatsapp"],
            get_whatsapp_link(self.property_1.seller.phone),
        )

    def test_get_details_seller_no_whatsapp(self):
        """valdiate seller's whatsapp in property response with no whatsapp"""

        # Update seller data
        first_property = self.property_1
        first_property.seller.has_whatsapp = False
        first_property.seller.save()

        # Get data from api
        response = self.client.get(
            self.endpoint + "?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )
        json_data = response.json()
        results = json_data["results"]
        first_result = list(
            filter(lambda result: result["id"] == first_property.id, results)
        )[0]

        self.assertEqual(first_result["seller"]["whatsapp"], "")

    def test_filter_location(self):
        """Test filter by location"""

        # Delete second property
        self.property_2.delete()

        # Make request
        response = self.client.get(
            self.endpoint + f"?ubicacion={self.location.id}",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response
        json_data = response.json()
        self.assertEqual(json_data["count"], 1)
        self.assertIsNone(json_data["next"])
        self.assertIsNone(json_data["previous"])
        self.assertEqual(len(json_data["results"]), 1)

        # Validate property
        property = json_data["results"][0]
        self.assertEqual(property["name"], self.property_1.name)
        self.assertEqual(property["location"], self.location.get_name("es"))

    def test_filter_location_empty(self):
        """Test filter by location with no properties"""

        # Make request
        location_2 = self.create_location("Location 2", "Location 2")
        response = self.client.get(
            self.endpoint + f"?ubicacion={location_2.id}",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response
        json_data = response.json()
        self.assertEqual(json_data["count"], 0)
        self.assertIsNone(json_data["next"])
        self.assertIsNone(json_data["previous"])
        self.assertEqual(len(json_data["results"]), 0)

    def test_filter_size(self):
        """Test filter by from and to size"""

        size_from = 0
        size_to = 200

        # Make request
        response = self.client.get(
            self.endpoint + f"?metros-desde={size_from}&metros-hasta={size_to}",
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

    def test_filter_size_empty(self):
        """Test filter by from and to size with no properties"""

        size_from = 0
        size_to = 1

        # Make request
        response = self.client.get(
            self.endpoint + f"?metros-desde={size_from}&metros-hasta={size_to}",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response
        json_data = response.json()
        self.assertEqual(json_data["count"], 0)
        self.assertIsNone(json_data["next"])
        self.assertIsNone(json_data["previous"])
        self.assertEqual(len(json_data["results"]), 0)

    def test_filter_price(self):
        """Test filter by from and to price"""

        price_from = 0
        price_to = 200000

        # Make request
        response = self.client.get(
            self.endpoint + f"?precio-desde={price_from}&precio-hasta={price_to}",
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

    def test_filter_price_empty(self):
        """Test filter by from and to price with no properties"""

        price_from = 0
        price_to = 1

        # Make request
        response = self.client.get(
            self.endpoint + f"?precio-desde={price_from}&precio-hasta={price_to}",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response
        json_data = response.json()
        self.assertEqual(json_data["count"], 0)
        self.assertIsNone(json_data["next"])
        self.assertIsNone(json_data["previous"])
        self.assertEqual(len(json_data["results"]), 0)


class LocationViewSetTestCase(TestPropertiesViewsBase):

    def setUp(self):

        # Set endpoint
        super().setUp(endpoint="/api/locations/")

        # Create other locations
        locations_num = 20
        for location_num in range(locations_num):
            self.create_location(
                f"Nueva Ubicación de prueba {location_num}",
                f"New test location {location_num}",
            )

    def test_get(self):
        """test enpoint list view response"""

        for lang in self.langs:

            response = self.client.get(
                self.endpoint,
                HTTP_ACCEPT_LANGUAGE=lang,
            )

            # Check response
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Validate response lenght
            json_data = response.json()
            self.assertEqual(len(json_data), 21)

            # Validate each location
            for location_json in json_data:

                location = models.Location.objects.get(id=location_json["id"])

                self.assertEqual(location_json["name"], getattr(location.name, lang))

    def test_no_data(self):
        """Validate response where there is no locations"""

        # Delete all locations
        models.Location.objects.all().delete()

        # Get data
        response = self.client.get(
            self.endpoint,
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response lenght
        json_data = response.json()
        self.assertEqual(len(json_data), 0)
