from core.test_base.test_admin import TestAdminBase
from leads import models


class LeadAdminTestCase(TestAdminBase):
    
    def setUp(self):
        
        # Create user and login
        super().setUp()
        
        # Save endpoint
        self.endpoint = "/admin/leads/lead/"
        
        # Create lead+
        self.lead = models.Lead.objects.create(
            name="John Doe",
            email="test@gmail.com",
            message="Hello, World!",
            phone="+1(123)456-7890",
        )
        
    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)
        
    def test_list_view_custom_fields(self):
        """ Valdiate custom fields (whatsapp_link) in list view """
        
        response = self.client.get(self.endpoint)
        
        # Validate whatsapp link
        self.assertContains(response, self.lead.phone)
        self.assertContains(response, self.lead.get_whatsapp_link())