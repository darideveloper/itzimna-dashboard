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

    def get_alt_text(self, language: str) -> str:
        """Retrieve alt text in the specified language.

        Args:
            language (str): Language code (e.g., 'en', 'es').

        Returns:
            str: Alt text in the specified language.
        """
        return getattr(self.alt_text, language) if self.alt_text else ""


class SearchLinks(models.Model):
    """
    Model to store additional search links for the SearchViewSet
    """

    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(
        translation_models.Translation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Título",
        related_name="search_links_title",
    )
    image = models.ImageField(upload_to="search_links_images/", verbose_name="Imagen")
    description = models.ForeignKey(
        translation_models.Translation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Descripción",
        related_name="search_links_description",
    )
    url = models.URLField(
        verbose_name="URL",
        help_text="Url completa (https://www.google.com)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación",
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Enlace de Búsqueda"
        verbose_name_plural = "Enlaces de Búsqueda"
