from django.db import models
from properties import models as property_models


class Lead(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300)
    property = models.ForeignKey(
        property_models.Property, on_delete=models.SET_NULL, null=True, blank=True
    )
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Leads"
        verbose_name = "Lead"
        
    def __str__(self):
        return f"{self.name} - {self.email}"
