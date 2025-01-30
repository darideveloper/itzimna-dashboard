from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status

from core.test_base.test_models import TestPropertiesModelsBase


class TestPropertiesViewsBase(TestPropertiesModelsBase, APITestCase):
    """Base class for testing views"""

    def setUp(self, endpoint="/api/"):
        """ Initialize test data """
        
        # Create initial data
        self.location = self.create_location()
        self.category = self.create_category()
        self.seller = self.create_seller()
        self.company = self.create_company()
        self.property_1 = self.create_property(
            name="Test property 1",
            company=self.company,
            location=self.location,
            category=self.category,
            seller=self.seller,
        )
        self.property_2 = self.create_property(
            name="Test property 2",
            company=self.company,
            location=self.location,
            category=self.category,
            seller=self.seller,
        )
        
        # Create user and login
        user = User.objects.create_superuser(
            username="admin",
            email="test@gmail.com",
            password="test pass",
        )
        self.token = str(AccessToken.for_user(user))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        
        # Save endpoint
        self.endpoint = endpoint
        
        # Global data
        self.langs = ["es", "en"]
        
    def validate_invalid_method(self, method: str):
        """ Validate that the given method is not allowed on the endpoint """
        
        response = getattr(self.client, method)(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        