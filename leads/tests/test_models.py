from django.test import TestCase
from django.core import mail
from django.conf import settings

from leads import models


class LeadTestCase(TestCase):
    """Test model custom methods"""

    def setUp(self):
        pass

    def test_get_clean_phone(self):
        """Test clean phone method"""

        # Create lead
        no_clean_phone = "+1 (123) 456- 78.90"
        lead = models.Lead.objects.create(
            name="John Doe",
            email="test@gmail.com",
            phone=no_clean_phone,
            message="Hello, World!",
        )

        # Validate phone
        whatsapp_link = "https://wa.me/5211234567890"
        self.assertEqual(lead.get_whatsapp_link(), whatsapp_link)

    def test_send_notification_email(self):
        """Test send notification email method"""

        # Create lead
        lead = models.Lead.objects.create(
            name="John Doe",
            email="test@gmail.com",
            phone="+1 (123) 456- 78.90",
            message="Hello, World!",
        )
        
        # Delete old emails
        mail.outbox = []

        # Send notification email
        lead.send_notification_email()
        self.assertEqual(len(mail.outbox), 1)

        # Validate email content
        email_data = mail.outbox[-1]
        self.assertEqual(email_data.subject, "Nuevo Lead")
        self.assertEqual(email_data.to, settings.EMAILS_LEADS_NOTIFICATIONS)
        self.assertIn(
            "Nuevo Lead: John Doe - test@gmail.com - +1 (123) 456- 78.90",
            email_data.body,
        )
        self.assertIn("/admin/leads/lead/", email_data.body)
        
    def test_save_send_notification_email(self):
        """Test auto send notification email method when creating a lead"""

        # Create lead
        models.Lead.objects.create(
            name="John Doe",
            email="test@gmail.com",
            phone="+1 (123) 456- 78.90",
            message="Hello, World!",
        )
        
        # Validate email was sent
        self.assertEqual(len(mail.outbox), 1)
        
    def test_save_no_send_notification_email_if_exists(self):
        """Test no send notification email method if lead already exists"""

        # Create lead
        lead = models.Lead.objects.create(
            name="John Doe",
            email="test@gmail.com",
            phone="+1 (123) 456- 78.90",
            message="Hello, World!",
        )
        
        # delete old emails
        mail.outbox = []
        
        # save lead
        lead.save()
        
        # validate email was not sent
        self.assertEqual(len(mail.outbox), 0)
