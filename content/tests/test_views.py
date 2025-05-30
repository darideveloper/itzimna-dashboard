from content import models

from core.test_base.test_views import TestContentViewsBase


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
        """ Validate response for each lang with multiple images """
        
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