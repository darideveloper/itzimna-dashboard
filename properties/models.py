from django.db import models


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nombre de la empresa'
    )
    details = models.TextField(
        null=True,
        blank=True,
        verbose_name='Detalles adicionales'
    )
    logo = models.ImageField(
        upload_to='logos/',
        null=True,
        blank=True,
        verbose_name='Logo (opcional)'
    )

    class Meta:
        verbose_name_plural = 'Empresas'
        verbose_name = 'Empresa'

    def __str__(self):
        return self.name


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nombre de la ubicación')
    details = models.TextField(
        null=True,
        blank=True,
        verbose_name='Detalles adicionales'
    )

    class Meta:
        verbose_name_plural = 'Ubicaciones'
        verbose_name = 'Ubicación'

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nombre de la categoría'
    )
    details = models.TextField(
        null=True,
        blank=True,
        verbose_name='Detalles adicionales'
    )

    class Meta:
        verbose_name_plural = 'Categorías'
        verbose_name = 'Categoría'

    def __str__(self):
        return self.name


class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, verbose_name='Nombre del vendedor')
    last_name = models.CharField(max_length=255, verbose_name='Apellido del vendedor')
    phone = models.CharField(
        unique=True,
        max_length=255,
        verbose_name='Teléfono del vendedor'
    )
    has_whatsapp = models.BooleanField(default=False, verbose_name='Tiene WhatsApp')
    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico del vendedor'
    )

    class Meta:
        verbose_name_plural = 'Vendedores'
        verbose_name = 'Vendedor'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        verbose_name='Nombre del desarrollo o propiedad'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Ubicación'
    )
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        verbose_name='Vendedor'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Categoría'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    meters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Metros cuadrados'
    )
    active = models.BooleanField(default=True, verbose_name='Activo')
    description = models.TextField(verbose_name='Descripción')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name_plural = 'Propiedades'
        verbose_name = 'Propiedad'
        
    def __str__(self):
        return self.name