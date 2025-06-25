from content import models

from core.test_base.test_views import TestContentViewsBase
from core.test_base.test_models import TestPropertiesModelsBase, TestPostsModelBase

from blog import models as blog_models
from properties import models as properties_models
from utils.media import get_media_url


class BestDevelopmentsImageTestCase(TestContentViewsBase):
    """Testing best developments image views"""

    def setUp(self):
        super().setUp(endpoint="/api/best-developments-images/")

    def test_get_one_image(self):
        """Validate response for each lang with a single image"""

        for lang in self.langs:
            response = self.client.get(self.endpoint, HTTP_ACCEPT_LANGUAGE=lang)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 1)

            # Check image data
            self.assertIn(
                self.best_developments_image.image.url, response.data[0]["image"]
            )
            self.assertEqual(
                response.data[0]["alt_text"],
                getattr(self.best_developments_image.alt_text, lang),
            )

    def test_get_many_images(self):
        """Validate response for each lang with multiple images"""

        # Delete existing images to avoid duplicates
        models.BestDevelopmentsImage.objects.all().delete()

        for image_id in range(20):
            self.create_best_developments_image(
                alt_text_es=f"Texto alternativo en español {image_id}",
                alt_text_en=f"Alternative text in English {image_id}",
                translation_key_posfix=image_id,
            )

        for lang in self.langs:
            response = self.client.get(self.endpoint, HTTP_ACCEPT_LANGUAGE=lang)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 20)

            for image_json in response.data:
                image_obj = models.BestDevelopmentsImage.objects.get(
                    id=image_json["id"]
                )
                self.assertIn(image_obj.image.url, image_json["image"])
                self.assertEqual(
                    image_json["alt_text"],
                    getattr(image_obj.alt_text, lang),
                )

    def test_get_no_images(self):
        """Validate response when no images are available"""

        models.BestDevelopmentsImage.objects.all().delete()

        for lang in self.langs:
            response = self.client.get(self.endpoint, HTTP_ACCEPT_LANGUAGE=lang)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 0)


class SearchViewSetTestCase(
    TestContentViewsBase, TestPropertiesModelsBase, TestPostsModelBase
):
    """Testing search viewset"""

    def setUp(self):
        super().setUp(endpoint="/api/search/")

        self.company = self.create_company()
        self.location = self.create_location()
        self.category = self.create_category()
        self.seller = self.create_seller()
        self.short_description = self.create_short_description()

        # Create 4 properties and 4 posts
        for index in range(4):
            self.create_property(
                name=f"property {index}",
                company=self.company,
                location=self.location,
                category=self.category,
                seller=self.seller,
                short_description=self.short_description,
            )
            self.create_post()

    def test_get_post_property(self):
        """Validate post and property in results"""

        random_post_id = blog_models.Post.objects.order_by("?").first().id
        random_property_id = properties_models.Property.objects.order_by("?").first().id

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        results = json_data["results"]
        self.assertEqual(len(results), 8)

        # validate that ids are in results
        ids_posts = [result["id"] for result in results if result["type"] == "post"]
        ids_properties = [
            result["id"] for result in results if result["type"] == "property"
        ]

        self.assertIn(random_post_id, ids_posts)
        self.assertIn(random_property_id, ids_properties)

    def test_get_post_data(self):
        """Validate post detail data"""

        # update post and query
        random_post = blog_models.Post.objects.order_by("?").first()
        random_post.save()

        response = self.client.get(self.endpoint, HTTP_ACCEPT_LANGUAGE="es")
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        results = json_data["results"]
        first_result = results[0]

        # Validate post data
        self.assertEqual(first_result["id"], random_post.id)
        self.assertEqual(first_result["title"], random_post.title)
        self.assertEqual(first_result["image"], random_post.banner_image_url)
        self.assertEqual(first_result["description"], random_post.description)
        self.assertEqual(first_result["extra"]["author"], random_post.author)

    def test_get_property_data(self):
        """Validate property detail data"""

        # update property and query
        random_property = properties_models.Property.objects.order_by("?").first()
        random_property.save()

        # Add image to property
        banner_image = self.create_property_image(property=random_property)

        response = self.client.get(self.endpoint, HTTP_ACCEPT_LANGUAGE="es")
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        results = json_data["results"]
        first_result = results[0]

        # Validate property data
        self.assertEqual(first_result["id"], random_property.id)
        self.assertEqual(first_result["title"], random_property.name)
        self.assertEqual(first_result["image"], get_media_url(banner_image.image))
        self.assertEqual(
            first_result["description"], random_property.get_short_description("es")
        )
        self.assertEqual(
            first_result["extra"]["price"], random_property.get_price_str()
        )
        self.assertEqual(first_result["extra"]["meters"], random_property.meters)

    def test_get_no_results(self):
        """Validate no results when no posts or properties are found"""

        # Delete post and property
        properties_models.Property.objects.all().delete()
        blog_models.Post.objects.all().delete()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        self.assertEqual(len(json_data["results"]), 0)

    def test_get_sorting(self):
        """Validate sorting by date"""

        # Get a random post and update
        random_post = blog_models.Post.objects.order_by("?").first()
        random_post.title = "Test post"
        random_post.save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)

        # Validate random post as first result
        json_data = response.json()
        self.assertEqual(json_data["results"][0]["id"], random_post.id)

    def test_get_pagination(self):
        """Validate pagination filter working"""

        # Create 8 more post and property
        for index in range(4, 8):
            self.create_property(
                name=f"property {index}",
                company=self.company,
                location=self.location,
                category=self.category,
                seller=self.seller,
                short_description=self.short_description,
            )
            self.create_post(title=f"post {index}")

        first_post = blog_models.Post.objects.order_by("id").first()
        first_property = properties_models.Property.objects.order_by("id").first()

        # Query with pagination
        response = self.client.get(self.endpoint, {"page": 2})

        # Validate last post and property are in results
        json_data = response.json()
        results = json_data["results"]
        results_ids = [result["id"] for result in results]
        self.assertIn(first_post.id, results_ids)
        self.assertIn(first_property.id, results_ids)

    def test_get_filter_by_lang(self):
        """Validate filtering by lang"""

        # Delete all posts and properties
        blog_models.Post.objects.all().delete()
        properties_models.Property.objects.all().delete()

        # Create 4 posts and 4 properties
        post = self.create_post(title="post lang")
        property = self.create_property(
            name="property lang",
            company=self.company,
            location=self.location,
            category=self.category,
            seller=self.seller,
            short_description=self.short_description,
        )

        for lang in self.langs:
            response = self.client.get(self.endpoint, HTTP_ACCEPT_LANGUAGE=lang)
            self.assertEqual(response.status_code, 200)

            json_data = response.json()
            results = json_data["results"]
            
            # Validate only reqturn post in "es" query
            if lang == "es":
                self.assertEqual(len(results), 2)
            else:
                self.assertEqual(len(results), 1)

            result_posts = [result for result in results if result["type"] == "post"]
            result_properties = [
                result for result in results if result["type"] == "property"
            ]

            # Validate post description
            if lang == "es":
                self.assertEqual(result_posts[0]["description"], post.description)
            else:
                self.assertEqual(len(result_posts), 0)

            # Validate property lang description
            self.assertEqual(
                result_properties[0]["description"], property.get_short_description(lang)
            )

    def test_get_filter_query_post_title(self):
        """Validate filtering by query"""
        
        # Update first post title
        first_post = blog_models.Post.objects.order_by("id").first()
        first_post.title = "Test post title example "
        first_post.save()
        
        # Query with query
        response = self.client.get(self.endpoint, {"q": "title"})
        self.assertEqual(response.status_code, 200)
        
        # Validate first post is in results
        json_data = response.json()
        results = json_data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], first_post.id)

    def test_get_filter_query_no_results(self):
        """Validate no results when no posts or properties are found"""
        pass

    def test_get_filter_query_pagination(self):
        """Validate pagination filter working"""
        pass
