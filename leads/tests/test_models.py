from django.test import TestCase

from leads import models


class LeadTestCase(TestCase):
    """ Test model custom methods """
    
    def setUp(self):
        pass
    
    def test_get_clean_phone(self):
        """ Test clean phone method """
        
        # Create lead
        no_clean_phone = "+1 (123) 456- 78.90"
        lead = models.Lead.objects.create(
            name="John Doe",
            email="test@gmail.com",
            phone=no_clean_phone,
            message="Hello, World!"
        )
        
        # Validate phone
        clean_phone = lead.test_get_clean_phone()
        self.assertEqual(clean_phone, "11234567890")