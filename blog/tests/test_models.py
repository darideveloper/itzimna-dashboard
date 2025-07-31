from blog import models
from django.test import TestCase


class PostTestCase(TestCase):
    """ Test Post model """

    def test_save_slug_generation(self):
        """ Test slug generation """
        post = models.Post.objects.create(title="Test Post")
        self.assertEqual(post.slug, "test-post")
        
    def test_save_slug_generation_with_existing_slug(self):
        """ Test slug generation with existing slug """
        post = models.Post.objects.create(title="Test Post")
        post.save()
        post = models.Post.objects.create(title="Test Post")
        self.assertEqual(post.slug, "test-post-1")