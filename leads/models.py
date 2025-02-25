from django.db import models
from properties import models as property_models


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
        verbose_name="Propiedad"
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
        
        super().save(*args, **kwargs)

    def test_get_clean_phone(self) -> str:
        """ Test get clean phone method
        
        Returns:
            str: Clean phone number
        """
        
        clean_chars = [' ', '-', '(', ')', '+', '.']
        clean_phone = self.phone
        for char in clean_chars:
            clean_phone = clean_phone.replace(char, '')
            
        return clean_phone
    
    # def get_whatsapp_link(self):
    #     return f"https://wa.me/{self.phone}"
