from django.db import models
from translations.models import Translation
from slugify import slugify

from utils.google_maps import get_maps_src


class Company(models.Model):

    # Options
    PROPERTY_TYPE_CHOICES = [
        # Residential
        ("house", "Casa"),
        ("townhouse", "Casa adosada"),
        ("condo", "Condominio"),
        ("apartment", "Departamento"),
        ("duplex", "Dúplex / Tríplex / Cuádruplex"),
        ("villa", "Villa"),
        ("penthouse", "Penthouse"),
        ("studio", "Estudio"),
        ("loft", "Loft"),
        ("mobile_home", "Casa móvil / prefabricada"),
        ("tiny_home", "Mini casa"),
        ("cabin", "Cabaña"),
        # Commercial
        ("office", "Oficina"),
        ("retail", "Tienda / Local comercial"),
        ("mall_unit", "Local en centro comercial"),
        ("warehouse", "Bodega / Almacén"),
        ("industrial", "Nave industrial"),
        ("hotel", "Hotel / Motel"),
        ("restaurant", "Restaurante / Bar"),
        ("coworking", "Espacio de coworking"),
        # Land
        ("residential_lot", "Terreno residencial"),
        ("commercial_lot", "Terreno comercial"),
        ("agricultural", "Terreno agrícola"),
        ("industrial_land", "Terreno industrial"),
        ("ranch", "Rancho / Granja"),
        ("forest", "Bosque / Terreno forestal"),
        # Mixed-Use
        ("mixed_use", "Propiedad de uso mixto"),
        # Luxury / Special Use
        ("luxury", "Residencia de lujo"),
        ("beachfront", "Propiedad frente a la playa"),
        ("golf", "Propiedad en campo de golf"),
        ("mountain", "Cabaña en la montaña"),
        ("historic", "Edificio histórico"),
        ("vacation", "Casa de vacaciones / Propiedad turística"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Nombre de la empresa"
    )
    type = models.CharField(
        max_length=50,
        choices=PROPERTY_TYPE_CHOICES,
        default="House",
        verbose_name="Tipo de propiedad",
        help_text="Selecciona el tipo de propiedad que ofrece la empresa",
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name="Slug",
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )
    logo = models.ImageField(
        upload_to="company-photos/",
        verbose_name="Logo de la empresa",
    )
    banner = models.ImageField(
        upload_to="company-banners/",
        null=True,
        blank=True,
        verbose_name="Banner de la empresa",
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ubicación de la empresa",
    )
    description_es = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descripción en español",
    )
    description_en = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descripción en inglés",
    )
    google_maps_src = models.TextField(
        null=True,
        blank=True,
        verbose_name="src de Google Maps",
        help_text="Puedes insertar el iframe completo",
    )
    phone = models.CharField(
        max_length=255,
        verbose_name="Teléfono de la empresa",
        null=True,
        blank=True,
    )
    email = models.EmailField(
        max_length=255,
        verbose_name="Correo electrónico de la empresa",
        null=True,
        blank=True,
    )
    social_media = models.URLField(
        max_length=255,
        verbose_name="Rede sociale de la empresa",
        null=True,
        blank=True,
    )
    show_contact_info = models.BooleanField(
        default=False,
        verbose_name="Mostrar información de contacto",
        help_text="Indica si se mostrará la información de contacto de la empresa",
    )
    promo_active = models.BooleanField(
        default=False,
        verbose_name="Promoción activa",
        help_text="Indica si la empresa tiene una promoción activa",
    )

    class Meta:
        verbose_name_plural = "Empresas"
        verbose_name = "Empresa"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Custom save method"""

        # Generate slug
        self.slug = slugify(self.name)

        # get src from google maps iframe
        if self.google_maps_src:
            self.google_maps_src = get_maps_src(self.google_maps_src)

        super().save(*args, **kwargs)

    def get_description(self, language: str) -> str:
        """Retrieve description in the correct language

        Args:
            language (str): Language to retrieve the description in

        Returns:
            str: Description in the correct language
        """

        return getattr(self, f"description_{language}")


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.OneToOneField(
        Translation,
        on_delete=models.CASCADE,
        verbose_name="Nombre de la ubicación",
    )
    details = models.TextField(
        null=True, blank=True, verbose_name="Detalles adicionales"
    )

    class Meta:
        verbose_name_plural = "Ubicaciones"
        verbose_name = "Ubicación"

    def __str__(self):
        return str(self.name.key)

    def get_name(self, language: str) -> str:
        """Retrieve location name in the correct language

        Args:
            language (str): Language to retrieve the name in

        Returns:
            str: Location name in the correct language
        """
        return getattr(self.name, language)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.OneToOneField(
        Translation,
        on_delete=models.CASCADE,
        verbose_name="Nombre de la categoría",
    )
    details = models.TextField(
        null=True, blank=True, verbose_name="Detalles adicionales"
    )

    class Meta:
        verbose_name_plural = "Categorías"
        verbose_name = "Categoría"

    def __str__(self):
        return str(self.name.key)

    def get_name(self, language: str) -> str:
        """Retrieve category name in the correct language

        Args:
            language (str): Language to retrieve the name in

        Returns:
            str: Category name in the correct language
        """
        return getattr(self.name, language)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.OneToOneField(
        Translation,
        on_delete=models.CASCADE,
        verbose_name="Nombre de la etiqueta",
    )

    class Meta:
        verbose_name_plural = "Etiquetas"
        verbose_name = "Etiqueta"

    def __str__(self):
        return str(self.name.key)

    def get_name(self, language: str) -> str:
        """Retrieve tag name in the correct language

        Args:
            language (str): Language to retrieve the name in

        Returns:
            str: tag name in the correct language
        """
        return getattr(self.name, language)


class ShortDescription(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.OneToOneField(
        Translation, on_delete=models.CASCADE, verbose_name="Descripción corta"
    )
    details = models.TextField(
        null=True, blank=True, verbose_name="Detalles adicionales"
    )

    class Meta:
        verbose_name_plural = "Descripciones cortas"
        verbose_name = "Descripción corta"

    def __str__(self):
        return f"es: {self.description.es} en: {self.description.en}"

    def get_description(self, language: str) -> str:
        """Retrieve short description in the correct language

        Args:
            language (str): Language to retrieve the short description in

        Returns:
            str: Short description in the correct language
        """

        return getattr(self.description, language)


class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, verbose_name="Nombre del vendedor")
    last_name = models.CharField(max_length=255, verbose_name="Apellido del vendedor")
    phone = models.CharField(
        unique=True,
        max_length=255,
        verbose_name="Teléfono del vendedor",
        null=True,
        blank=True,
    )
    has_whatsapp = models.BooleanField(default=False, verbose_name="Tiene WhatsApp")
    email = models.EmailField(
        unique=True, verbose_name="Correo electrónico del vendedor"
    )

    class Meta:
        verbose_name_plural = "Vendedores"
        verbose_name = "Vendedor"

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="Nombre del desarrollo o propiedad", unique=True
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name="Slug",
        unique=True,
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Empresa",
        related_name="related_properties",
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name="Ubicación"
    )
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, verbose_name="Vendedor"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Categoría"
    )
    tags = models.ManyToManyField(
        Tag, verbose_name="Etiquetas", blank=True, related_name="properties"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    meters = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Metros cuadrados"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si se mostrará en la página",
    )
    featured = models.BooleanField(
        default=False,
        verbose_name="Destacado",
        help_text="Indica si se mostrará en la sección de destacados",
    )
    short_description = models.ForeignKey(
        ShortDescription,
        on_delete=models.CASCADE,
        verbose_name="Descripción corta",
        help_text="Descripción corta de la propiedad o desarrollo",
    )
    google_maps_src = models.TextField(
        null=True,
        blank=True,
        verbose_name="src de Google Maps",
        help_text="Puedes insertar el iframe completo",
    )
    description_es = models.TextField(verbose_name="Descripción en español")
    description_en = models.TextField(verbose_name="Descripción en inglés")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name_plural = "Propiedades"
        verbose_name = "Propiedad"

    def __str__(self):
        return f"{self.name} - {self.location}"

    def save(self, *args, **kwargs):
        """Custom save method"""

        # Override slug if not set
        if not self.slug:
            slug = slugify(self.name)
            
            # Validate slug is unique
            extra_slug = 1
            while Property.objects.filter(slug=slug).exists():
                slug = f"{slug}-{extra_slug}"
                extra_slug += 1
            
            self.slug = slug

        # get src from google maps iframe
        if self.google_maps_src:
            self.google_maps_src = get_maps_src(self.google_maps_src)

        # Call parent save method
        super().save(*args, **kwargs)

    def get_description(self, language: str) -> str:
        """Retrieve description in the correct language

        Args:
            language (str): Language to retrieve the description in

        Returns:
            str: Description in the correct language
        """

        return getattr(self, f"description_{language}")

    def get_price_str(self) -> str:
        """Retrieve price as a string

        Returns:
            str: Price as a 1,000.00 string
        """
        return f"{self.price:,.2f}"
    
    def get_short_description(self, language: str) -> str:
        """Retrieve short description in the correct language
        
        Args:
            language (str): Language to retrieve the short description in
        """
        return self.short_description.get_description(language)


class PropertyImage(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, verbose_name="Propiedad"
    )
    image = models.ImageField(upload_to="property-images/", verbose_name="Imagen")
    alt_text = models.OneToOneField(
        Translation,
        on_delete=models.CASCADE,
        verbose_name="Texto alternativo",
        help_text="Texto que se mostrará si la imagen no carga (recomendado para SEO)",
    )
    show_gallery = models.BooleanField(default=True, verbose_name="Mostrar en galería")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name_plural = "Imágenes"
        verbose_name = "Imagen"

    def __str__(self):
        return f"{self.property} - {self.alt_text.key}"

    def get_alt_text(self, language: str) -> str:
        """Retrieve alt text in the correct language

        Args:
            language (str): Language to retrieve the alt text in

        Returns:
            str: Alt text in the correct language
        """
        return getattr(self.alt_text, language)
