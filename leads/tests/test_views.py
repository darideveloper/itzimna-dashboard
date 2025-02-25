from rest_framework import status

from core.test_base.test_views import TestPropertiesViewsBase
from leads import models


class LeadViewTestCase(TestPropertiesViewsBase):
    
    def setUp(self):
        """ Initialize test data """
        
        # Endpoint
        # Create admin user + properties data
        super().setUp(endpoint="/api/leads/")
        
        # Set restricted methods to test
        self.restricted_post = False
        
        self.data = {
            "name": "John Doe",
            "email": "test@gmail.com",
            "message": "Hello, World!",
            "property": 1
        }
        
    def test_post(self):
        """ Submit valid data to endpoint in post """
        
        # Make request
        response = self.client.post(self.endpoint, self.data)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.data["name"])
        self.assertEqual(response.data["email"], self.data["email"])
        self.assertEqual(response.data["message"], self.data["message"])
        self.assertEqual(response.data["property"], int(self.data["property"]))
        
        # Validate new lead in database
        self.assertEqual(models.Lead.objects.count(), 1)
        lead = models.Lead.objects.first()
        self.assertEqual(lead.name, self.data["name"])
        self.assertEqual(lead.email, self.data["email"])
        self.assertEqual(lead.message, self.data["message"])
        self.assertEqual(lead.property.id, int(self.data["property"]))
        
    def test_post_missing_fields(self):
        """ Try to send data with missing required fields """
        
        # Make request without data
        response = self.client.post(self.endpoint, {})
        
        # Validate response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["data"]["name"][0], "Este campo es requerido.")
        self.assertEqual(response.data["data"]["email"][0], "Este campo es requerido.")
        self.assertEqual(response.data["data"]["message"][0], "Este campo es requerido.")
        
    def test_post_invalid_property_id(self):
        """ Try to send data with invalid property id """
        
        # Update data with invalid property id
        new_id = 3
        self.data["property"] = new_id
        
        # Make request
        response = self.client.post(self.endpoint, self.data)
        
        # Validate response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["data"]["property"][0],
            f'Clave primaria "{new_id}" inválida - objeto no existe.'
        )
        
    def test_post_invalid_email(self):
        """ Try to send data with invalid property id """
        
        # Update data with invalid property id
        new_email = "test"
        self.data["email"] = new_email
        
        # Make request
        response = self.client.post(self.endpoint, self.data)
        
        # Validate response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["data"]["email"][0],
            'Introduzca una dirección de correo electrónico válida.'
        )
