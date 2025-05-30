from django.db import models
from translations import models as translation_models


class BestDevelopmentsImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(
        upload_to="best_developments_gallery_images/", verbose_name="Imagen"
    )
    alt_text = models.ForeignKey(
        translation_models.Translation,
        on_delete=models.SET_NULL,
        related_name="best_developments_image_alt_text",
        null=True,
        blank=True,
        verbose_name="Texto alternativo",
    )

    def __str__(self):
        return self.alt_text.key if self.alt_text.key else f"Image {self.id}"

    class Meta:
        verbose_name = "Imagen de Mejores Desarrollos"
        verbose_name_plural = "Imágenes de Mejores Desarrollos"
