from django.db import models


class TranslationGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nombre del grupo'
    )

    class Meta:
        verbose_name = 'Grupo de traducción'
        verbose_name_plural = 'Grupos de traducción'

    def __str__(self):
        return self.name


class Translation(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(
        TranslationGroup,
        on_delete=models.CASCADE,
        verbose_name='Grupo de traducción',
        null=True,
        blank=True
    )
    key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Clave'
    )
    es = models.CharField(
        max_length=255,
        verbose_name='Español',
        help_text='Texto original en español'
    )
    en = models.CharField(
        max_length=255,
        verbose_name='Inglés',
        help_text='Traducción al inglés'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )

    class Meta:
        verbose_name = 'Traducción'
        verbose_name_plural = 'Traducciones'

    def __str__(self):
        return f"{self.group} - {self.key}"