from django.db import models


class Post(models.Model):
    LANGS = (
        ("es", "Español"),
        ("en", "Inglés"),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Título")
    lang = models.CharField(
        max_length=2, choices=LANGS, default="es", verbose_name="Idioma"
    )
    description = models.TextField(
        verbose_name="Descripción corta",
    )
    keywords = models.CharField(
        max_length=255,
        verbose_name="Palabras clave",
        help_text="Separadas por comas",
    )
    author = models.CharField(
        max_length=255, verbose_name="Autor", default="Itimna Team"
    )
    content = models.TextField(verbose_name="Contenido")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name_plural = "Entradas"
        verbose_name = "Entrada"

    def __str__(self):
        return self.title
