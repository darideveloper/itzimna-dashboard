from django.db import models
from django.core.mail import send_mail
from django.conf import settings

from properties import models as property_models
from utils.whatsapp import get_whatsapp_link


class Lead(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    message = models.CharField(max_length=300, verbose_name="Mensaje")
    property = models.ForeignKey(
        property_models.Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Propiedad",
    )
    company = models.ForeignKey(
        property_models.Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Empresa",
    )
    done = models.BooleanField(default=False, verbose_name="Finalizado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    class Meta:
        verbose_name_plural = "Leads"
        verbose_name = "Lead"

    def __str__(self):
        return f"{self.name} - {self.email}"

    def save(self, *args, **kwargs):

        is_new = not self.id

        if is_new:
            # Send message to whatsapp
            self.send_notification_email()

        super().save(*args, **kwargs)

    def get_whatsapp_link(self):

        # Add 521 at the start of the number
        return get_whatsapp_link(self.phone)

    def send_notification_email(self):
        # Send email to admins
        # http://127.0.0.1:8000/admin/leads/lead/9/change/
        admin_lead_link = f"{settings.HOST}/admin/leads/lead/"
        message = f"Nuevo Lead: {self.name} - {self.email} - {self.phone}"
        message += f'\n\n"{self.message}"'
        message += f"\n\nVer todos los leads: {admin_lead_link}"
        
        send_mail(
            subject="Nuevo Lead",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=settings.EMAILS_LEADS_NOTIFICATIONS,
            fail_silently=False,
        )
