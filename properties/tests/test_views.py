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

    def test_get_details_related_properties_company(self):
        """Validate related properties in details, based in company
        Expect 6 properties from the same company
        """

        # Delete all properties
        models.Property.objects.all().delete()

        properties_related_ids = []
        properties_no_related_ids = []

        location = models.Location.objects.all().first()
        category = models.Category.objects.all().first()
        seller = models.Seller.objects.all().first()

        company_a = self.create_company(
            "Company single property test A", location=location
        )
        company_b = self.create_company(
            "Company single property test B", location=location
        )

        # Create a set of properties with the same company
        for id in range(7):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_a,
                location=location,
                category=category,
                seller=seller,
            )
            properties_related_ids.append(property.id)

        # Create second set of properties with the same company
        for id in range(7, 13):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_b,
                location=location,
                category=category,
                seller=seller,
            )
            properties_no_related_ids.append(property.id)

        # Make request
        first_property = models.Property.objects.first()
        response = self.client.get(
            f"{self.endpoint}{first_property.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate related properties
        self.assertEqual(len(json_data["related_properties"]), 6)
        for related_property in json_data["related_properties"]:
            # Validate id of each property
            self.assertIn(related_property["id"], properties_related_ids)
            self.assertNotIn(related_property["id"], properties_no_related_ids)

    def test_get_details_related_properties_company_less_six(self):
        """Validate related properties in details, based in company
        with less than six properties from same company
        Expect all properties from the same company
        """

        # Delete all properties
        models.Property.objects.all().delete()

        properties_related_ids = []
        properties_no_related_ids = []

        location = models.Location.objects.all().first()
        category = models.Category.objects.all().first()
        seller = models.Seller.objects.all().first()

        company_a = self.create_company(
            "Company single property test A", location=location
        )
        company_b = self.create_company(
            "Company single property test B", location=location
        )

        # Create a set of properties with the same company
        for id in range(2):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_a,
                location=location,
                category=category,
                seller=seller,
            )
            properties_related_ids.append(property.id)

        # Create second set of properties with the same company
        for id in range(7, 13):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_b,
                location=location,
                category=category,
                seller=seller,
            )
            properties_no_related_ids.append(property.id)

        # Make request
        first_property = models.Property.objects.first()
        response = self.client.get(
            f"{self.endpoint}{first_property.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate related properties
        self.assertEqual(len(json_data["related_properties"]), 1)
        for related_property in json_data["related_properties"]:
            # Validate id of each property
            self.assertIn(related_property["id"], properties_related_ids)
            self.assertNotIn(related_property["id"], properties_no_related_ids)

    def test_get_details_related_properties_tag(self):
        """Validate related properties in details, based in tags
        Expect 6 properties with the same tag
        """

        # Delete all properties
        models.Property.objects.all().delete()
        models.Tag.objects.all().delete()

        properties_related_ids = []
        properties_no_related_ids = []

        location = models.Location.objects.all().first()
        category = models.Category.objects.all().first()
        seller = models.Seller.objects.all().first()

        # Create a set of properties with the same tags
        tag_a = self.create_tag("Tag single property test A", "A")
        tag_b = self.create_tag("Tag single property test B", "B")

        for id in range(7):
            company = self.create_company(
                f"Company single property test {id}", location=location
            )
            property = self.create_property(
                name=f"Property single test {id}",
                company=company,
                location=location,
                category=category,
                seller=seller,
            )
            property.tags.add(tag_a)
            property.save()
            properties_related_ids.append(property.id)

        for id in range(7, 13):
            company = self.create_company(
                f"Company single property test {id}", location=location
            )
            property = self.create_property(
                name=f"Property single test {id}",
                company=company,
                location=location,
                category=category,
                seller=seller,
            )
            property.tags.add(tag_b)
            property.save()
            properties_no_related_ids.append(property.id)

        # Make request
        first_property = models.Property.objects.first()
        print(first_property.tags.all())
        response = self.client.get(
            f"{self.endpoint}{first_property.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate related properties
        self.assertEqual(len(json_data["related_properties"]), 6)
        print(json_data["related_properties"])
        for related_property in json_data["related_properties"]:
            # Validate id of each property
            self.assertIn(related_property["id"], properties_related_ids)
            self.assertNotIn(related_property["id"], properties_no_related_ids)

    def test_get_details_related_properties_comapany_and_tag(self):
        """Validate related properties in details, based in company and tags
        Expect 2 properties from the same company and 4 properties with the same tag
        """

        # Delete all properties
        models.Property.objects.all().delete()
        models.Tag.objects.all().delete()

        properties_related_ids = []
        properties_no_related_ids = []

        location = models.Location.objects.all().first()
        category = models.Category.objects.all().first()
        seller = models.Seller.objects.all().first()

        # base companies and tags
        company_a = self.create_company(
            "Company single property test A", location=location
        )
        company_b = self.create_company(
            "Company single property test B", location=location
        )
        company_c = self.create_company(
            "Company single property test C", location=location
        )
        tag_a = self.create_tag("Tag single property test A")
        tag_b = self.create_tag("Tag single property test B")
        tag_c = self.create_tag("Tag single property test C")

        # Create 3 properties with tag_a and company_a
        for id in range(3):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_a,
                location=location,
                category=category,
                seller=seller,
            )
            property.tags.add(tag_a)
            property.save()
            properties_related_ids.append(property.id)

        # Create 4 properties with tag_b and company_b
        for id in range(3, 7):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_b,
                location=location,
                category=category,
                seller=seller,
            )
            property.tags.add(tag_b)
            property.save()
            properties_related_ids.append(property.id)

        # Create 2 properties with tag_c and company_c
        for id in range(7, 9):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_c,
                location=location,
                category=category,
                seller=seller,
            )
            property.tags.add(tag_c)
            property.save()
            properties_no_related_ids.append(property.id)

        # Change first property to company_b
        first_property = models.Property.objects.first()
        first_property.company = company_b
        first_property.save()

        # Make request
        response = self.client.get(
            f"{self.endpoint}{first_property.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate related properties (tag_a and company_b)
        self.assertEqual(len(json_data["related_properties"]), 6)
        for related_property in json_data["related_properties"]:
            # Validate id of each property
            self.assertIn(related_property["id"], properties_related_ids)
            self.assertNotIn(related_property["id"], properties_no_related_ids)

    def test_get_details_related_properties_no_data(self):
        """Validate related properties in details, with no related properties"""

        # Delete all properties
        models.Property.objects.all().delete()
        models.Tag.objects.all().delete()

        location = models.Location.objects.all().first()
        category = models.Category.objects.all().first()
        seller = models.Seller.objects.all().first()

        # base companies and tags
        company_a = self.create_company(
            "Company single property test A", location=location
        )
        company_b = self.create_company(
            "Company single property test B", location=location
        )
        company_c = self.create_company(
            "Company single property test C", location=location
        )
        tag_a = self.create_tag("Tag single property test A")
        tag_b = self.create_tag("Tag single property test B")
        tag_c = self.create_tag("Tag single property test C")

        # Create 3 properties with tag_a and company_a
        for id in range(3):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_a,
                location=location,
                category=category,
                seller=seller,
            )
            property.tags.add(tag_a)
            property.save()

        # Create 4 properties with tag_b and company_b
        for id in range(3, 7):
            property = self.create_property(
                name=f"Property test {id}",
                company=company_b,
                location=location,
                category=category,
                seller=seller,
            )
            property.tags.add(tag_b)
            property.save()

        # Change first property to company_c and tag_c
        first_property = models.Property.objects.first()
        first_property.company = company_c
        first_property.tags.remove(tag_a)
        first_property.tags.add(tag_c)
        first_property.save()

        # Make request
        response = self.client.get(
            f"{self.endpoint}{first_property.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate related properties (tag_a and company_b)
        self.assertEqual(len(json_data["related_properties"]), 0)

    def test_get_details_related_properties_inner_data(self):
        """Validate specific details of related properties"""

        # Delete all properties
        models.Property.objects.all().delete()

        location = models.Location.objects.all().first()
        category = models.Category.objects.all().first()
        seller = models.Seller.objects.all().first()
        tag_a = self.create_tag("Tag single property test A")
        tag_b = self.create_tag("Tag single property test B")

        company_a = self.create_company(
            "Company single property test A", location=location
        )

        # Create 2 properties with the same company
        short_description_1 = self.create_short_description(
            "Short description 1", "Short description 1"
        )
        property_1 = self.create_property(
            name="Property test 1",
            company=company_a,
            location=location,
            category=category,
            seller=seller,
            short_description=short_description_1,
            price=100000,
            meters=100,
            active=True,
            description_en="Description in English 1",
            description_es="Descripción en Español 1",
        )
        property_1.tags.add(tag_a)
        property_1.save()

        short_description_2 = self.create_short_description(
            "Short description 2", "Short description 2"
        )
        property_2 = self.create_property(
            name="Property test 2",
            company=company_a,
            location=location,
            category=category,
            seller=seller,
            short_description=short_description_2,
            price=200000,
            meters=200,
            active=True,
            description_en="Description in English 2",
            description_es="Descripción en Español 2",
        )
        property_2.tags.add(tag_b)
        property_2.save()

        # Make request
        response = self.client.get(
            f"{self.endpoint}{property_1.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate related properties
        self.assertEqual(len(json_data["related_properties"]), 1)

        # Validate related property data
        related_property = json_data["related_properties"][0]
        self.assertEqual(related_property["id"], property_2.id)
        self.assertEqual(related_property["name"], property_2.name)
        self.assertEqual(
            related_property["location"], property_2.location.get_name("es")
        )
        self.assertEqual(
            related_property["category"], property_2.category.get_name("es")
        )
        self.assertEqual(related_property["seller"], property_2.seller.get_full_name())
        self.assertEqual(
            related_property["short_description"],
            property_2.short_description.description.es,
        )
        self.assertEqual(related_property["price"], property_2.get_price_str())
        self.assertEqual(related_property["meters"], f"{property_2.meters}.00")
        self.assertEqual(related_property["tags"][0]["id"], tag_b.id)
        
        # Validate missing fields
        self.assertNotIn("description", related_property)
        self.assertNotIn("created_at", related_property)
        self.assertNotIn("updated_at", related_property)
        self.assertNotIn("google_maps_src", related_property)

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
            self.assertEqual(len(json_data), 22)

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


class CompanyViewSetTestCase(TestPropertiesViewsBase):

    def setUp(self):
        # Set endpoint
        super().setUp(endpoint="/api/companies/")

        # Create many companies
        for lang in self.langs:
            companies_num = 10
            for company_num in range(companies_num):
                self.create_company(
                    f"Compañía de prueba {company_num} {lang}",
                    f"Test company {company_num} {lang}",
                    location=self.create_location(
                        f"Ubicación de prueba {company_num} {lang}",
                        f"Test location {company_num} {lang}",
                    ),
                )

    def test_get_summary(self):
        """test enpoint list view response"""

        for lang in self.langs:

            response = self.client.get(
                self.endpoint + "?summary=true&page-size=9999",
                HTTP_ACCEPT_LANGUAGE=lang,
            )

            # Check response
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Validate response lenght
            json_data = response.json()
            results = json_data["results"]
            self.assertGreaterEqual(len(results), 10)

            # Validate each company
            for company_json in results:

                company = models.Company.objects.get(id=company_json["id"])

                self.assertEqual(company_json["name"], company.name)
                self.assertEqual(company_json["type"], company.type)
                self.assertEqual(company_json["slug"], company.slug)
                self.assertIn(company.logo.url, company_json["logo"])
                self.assertIn(company.banner.url, company_json["banner"])
                self.assertEqual(
                    company_json["location"], company.location.get_name(lang)
                )

    def test_get_summary_only_required_data(self):
        """test enpoint list view response with a company only with required data"""

        # Delete all companies
        models.Company.objects.all().delete()

        # Create company only with required data
        company = self.create_company("test single company required data")
        company.banner = None
        company.location = None
        company.save()

        # Get data from api
        response = self.client.get(
            self.endpoint + "?summary=true&page-size=9999",
            HTTP_ACCEPT_LANGUAGE="es",
        )
        json_data = response.json()
        results = json_data["results"]
        self.assertEqual(len(results), 1)

        # Validate company data
        company_json = results[0]
        self.assertEqual(company_json["name"], company.name)
        self.assertEqual(company_json["type"], company.type)
        self.assertEqual(company_json["slug"], company.slug)
        self.assertIn(company.logo.url, company_json["logo"])
        self.assertIsNone(company_json["banner"])
        self.assertEqual(company_json["location"], "")

    def test_get_details(self):
        """Get company full data"""

        # Make request
        for lang in self.langs:
            response = self.client.get(
                self.endpoint + "?details=true&page-size=9999",
                HTTP_ACCEPT_LANGUAGE=lang,
            )

            # Check response
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Validate response extra content
            json_data = response.json()
            results = json_data["results"]
            self.assertGreaterEqual(len(results), 10)

            # Validate each company
            for company_json in results:

                company = models.Company.objects.get(id=company_json["id"])

                self.assertEqual(company_json["name"], company.name)
                self.assertEqual(company_json["type"], company.type)
                self.assertEqual(company_json["slug"], company.slug)
                self.assertIn(company.logo.url, company_json["logo"])
                self.assertIn(company.banner.url, company_json["banner"])
                self.assertEqual(
                    company_json["location"], company.location.get_name(lang)
                )
                self.assertEqual(
                    company_json["description"],
                    company.get_description(lang),
                )
                self.assertEqual(
                    company_json["google_maps_src"], company.google_maps_src
                )
                self.assertEqual(company_json["phone"], company.phone)
                self.assertEqual(company_json["email"], company.email)
                self.assertEqual(company_json["social_media"], company.social_media)
                self.assertEqual(
                    company_json["show_contact_info"], company.show_contact_info
                )

    def test_get_details_only_required_data(self):
        """Get company full data with only required data"""

        # Delete all companies
        models.Company.objects.all().delete()

        # Create company only with required data
        company = self.create_company("test single company required data")
        company.banner = None
        company.location = None
        company.description_es = None
        company.description_en = None
        company.google_maps_src = None
        company.phone = None
        company.email = None
        company.social_media = None
        company.save()

        # Make request
        response = self.client.get(
            self.endpoint + "?details=true&page-size=9999",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()
        results = json_data["results"]
        self.assertEqual(len(results), 1)

        # Validate each company
        company_json = results[0]
        self.assertEqual(company_json["name"], company.name)
        self.assertEqual(company_json["type"], company.type)
        self.assertEqual(company_json["slug"], company.slug)
        self.assertIn(company.logo.url, company_json["logo"])
        self.assertIsNone(company_json["banner"])
        self.assertEqual(company_json["location"], "")
        self.assertEqual(company_json["description"], "")
        self.assertEqual(company_json["google_maps_src"], None)
        self.assertEqual(company_json["phone"], None)
        self.assertEqual(company_json["email"], None)
        self.assertEqual(company_json["social_media"], None)
        self.assertEqual(company_json["show_contact_info"], True)

    def test_get_details_single(self):
        """Get company full data for a single company"""

        company = self.create_company("Company single test")

        # Make request
        response = self.client.get(
            f"{self.endpoint}{company.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate company data
        self.assertEqual(json_data["name"], company.name)
        self.assertEqual(json_data["type"], company.type)
        self.assertEqual(json_data["slug"], company.slug)
        self.assertIn(company.logo.url, json_data["logo"])
        self.assertIn(company.banner.url, json_data["banner"])
        self.assertEqual(json_data["location"], company.location.get_name("es"))
        self.assertEqual(
            json_data["description"],
            company.get_description("es"),
        )
        self.assertEqual(json_data["google_maps_src"], company.google_maps_src)
        self.assertEqual(json_data["phone"], company.phone)
        self.assertEqual(json_data["email"], company.email)
        self.assertEqual(json_data["social_media"], company.social_media)
        self.assertEqual(json_data["show_contact_info"], company.show_contact_info)

    def test_get_details_related_single_property(self):
        """Get company full data for a single company with a related property"""

        # Delete all properties
        models.Property.objects.all().delete()

        # Create property and company
        location = models.Location.objects.all().first()
        category = models.Category.objects.all().first()
        seller = models.Seller.objects.all().first()
        company = self.create_company("Company single property test", location=location)
        property = self.create_property(
            name="Property single test a",
            company=company,
            location=location,
            category=category,
            seller=seller,
        )
        property.save()
        banner = self.create_property_image(property=property)

        # Make request
        response = self.client.get(
            f"{self.endpoint}{company.id}/?details=true",
            HTTP_ACCEPT_LANGUAGE="es",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Validate company data
        self.assertEqual(len(json_data["related_properties"]), 1)

        property_json = json_data["related_properties"][0]
        self.assertEqual(property_json["id"], property.id)
        self.assertEqual(property_json["name"], property.name)
        self.assertEqual(property_json["location"], property.location.get_name("es"))
        self.assertEqual(property_json["seller"], property.seller.get_full_name())
        self.assertEqual(property_json["category"], property.category.name.es)
        self.assertEqual(property_json["tags"], [])
        self.assertEqual(
            property_json["short_description"],
            getattr(property.short_description.description, "es"),
        )
        self.assertIn(banner.image.url, property_json["banner"]["url"])
        self.assertEqual(property_json["banner"]["alt"], banner.get_alt_text("es"))
        self.assertEqual(property_json["price"], property.get_price_str())
        self.assertEqual(property_json["meters"], f"{property.meters}.00")
        self.assertEqual(property_json["google_maps_src"], property.google_maps_src)
        self.assertEqual(property_json["tags"], [])

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
