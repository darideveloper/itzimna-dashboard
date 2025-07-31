from django.test import TestCase

from properties import models as properties_models
from translations import models as translations_models
from blog import models as blog_models
from content import models as content_models

from utils.media import get_test_image


class TestPropertiesModelsBase(TestCase):
    """Validate model custom methods"""

    def create_translation(
        self, key: str, es: str = "Traducción de prueba", en: str = "Test translation"
    ) -> translations_models.Translation:
        """Create a translation object

        Args:
            key (str): Translation key
            es (str): Spanish translation
            en (str): English translation

        Returns:
            Translation: Translation object created
        """

        return translations_models.Translation.objects.create(
            key=key,
            es=es,
            en=en,
        )

    def create_location(
        self,
        name_es: str = "Ubicación de prueba",
        name_en: str = "Test location",
        details: str = "",
    ) -> properties_models.Location:
        """Create a location object

        Args:
            name_es (str): Spanish location name
            name_en (str): English location name
            details (str): Location details

        Returns:
            properties_models.Location: Location object created
        """

        location, _ = properties_models.Location.objects.get_or_create(
            name=self.create_translation(name_es, name_es, name_en),
            details=details,
        )

        return location

    def create_category(
        self,
        name_es: str = "Categoria de prueba",
        name_en: str = "Test category",
        details: str = "",
    ) -> properties_models.Category:
        """Create a category object

        Args:
            name_es (str): Spanish category name
            name_en (str): English category name
            details (str): Category details

        Returns:
            properties_models.Category: Category object created
        """

        return properties_models.Category.objects.create(
            name=self.create_translation("category_test", name_es, name_en),
            details=details,
        )

    def create_seller(
        self,
        first_name: str = "Test",
        last_name: str = "Seller",
        phone: str = "123456789",
    ) -> properties_models.Seller:
        """Create a seller object

        Args:
            first_name (str): Seller first name
            last_name (str): Seller last name
            phone (str): Seller phone

        Returns:
            properties_models.Seller: Seller object created
        """

        return properties_models.Seller.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            has_whatsapp=True,
        )

    def create_company(
        self,
        name: str = "Company test",
        type: str = "House",
        logo_name: str = "logo.webp",
        banner_name: str = "banner.webp",
        location: properties_models.Location = None,
        description_es: str = "Descripción de prueba",
        description_en: str = "Test description",
        google_maps_src: str = "https://www.google.com/maps/embed?pb=!1m.",
        phone: str = "123456789",
        email: str = "test@gmail.com",
        social_media: str = "https://www.instagram.com/test/",
        show_contact_info: bool = True,
    ) -> properties_models.Company:
        """Create a company object

        Args:
            name (str): Company name
            type (str): Properties type
            logo_name (str): Logo image name
            banner_name (str): Banner image name
            location (properties_models.Location): Location object
            description_es (str): Spanish description
            description_en (str): English description
            google_maps_src (str): Google Maps source
            phone (str): Company phone
            email (str): Company email
            social_media (str): Company social media
            show_contact_info (bool): Show contact info (default: True)

        Returns:
            properties_models.Company: Company object created
        """

        # Create location if not provided
        if not location:
            location = self.create_location(f"ubicación {name}", f"location {name}")

        return properties_models.Company.objects.create(
            name=name,
            type=type,
            logo=get_test_image(logo_name),
            banner=get_test_image(banner_name),
            location=location,
            description_es=description_es,
            description_en=description_en,
            google_maps_src=google_maps_src,
            phone=phone,
            email=email,
            social_media=social_media,
            show_contact_info=show_contact_info,
        )

    def create_short_description(
        self,
        name: str = "short_description_test",
        es: str = "Descripción corta de prueba",
        en: str = "Test short description",
    ) -> properties_models.ShortDescription:
        """Create a short description object

        Args:
            key (str): Short description key
            es (str): Spanish short description
            en (str): English short description

        Returns:
            properties_models.ShortDescription: Short description object created
        """

        return properties_models.ShortDescription.objects.create(
            description=self.create_translation(name, es, en),
            details="",
        )

    def create_property(
        self,
        name: str = "Property test",
        company: properties_models.Company = None,
        location: properties_models.Location = None,
        category: properties_models.Category = None,
        seller: properties_models.Seller = None,
        short_description: properties_models.ShortDescription = None,
        price: float = 1000,
        meters: float = 100,
        active: bool = True,
        review_name: str = "Test review name",
        review_rating: float = 4.5,
        review_count: int = 10,
        description_es: str = "Descripción de la propiedad",
        description_en: str = "Property description",
        google_maps_src: str = "https://www.google.com/maps/embed?pb=!1m.",
    ) -> properties_models.Property:
        """Create a property object

        Args:
            name (str): Property name
            company (properties_models.Company): Company object
            location (properties_models.Location): Location object
            category (properties_models.Category): Category object
            seller (properties_models.Seller): Seller object
            price (float): Property price
            meters (float): Property meters
            active (bool): Active property
            description_es (str): Spanish description
            description_en (str): English description

        Returns:
            properties_models.Property: Property object created
        """

        if not company:
            company = self.create_company()

        if not location:
            location = self.create_location()

        if not category:
            category = self.create_category()

        if not seller:
            seller = self.create_seller()

        if not short_description:
            short_description = self.create_short_description(
                name=f"short_description {name}"
            )

        return properties_models.Property.objects.create(
            name=name,
            company=company,
            location=location,
            seller=seller,
            category=category,
            price=price,
            meters=meters,
            active=active,
            description_es=description_es,
            description_en=description_en,
            short_description=short_description,
            google_maps_src=google_maps_src,
            review_name=review_name,
            review_rating=review_rating,
            review_count=review_count,
        )

    def create_property_image(
        self,
        property: properties_models.Property = None,
        image_name: str = "test.webp",
        alt_text_es: str = "Texto alternativo",
        alt_text_en: str = "Alt text",
        show_gallery: bool = True,
    ) -> properties_models.PropertyImage:
        """Create a property image object

        Args:
            property (properties_models.Property): Property object
            image_name (str): Image source
            alt_text_es (str): Spanish alt text
            alt_text_en (str): English alt text
            show_gallery (bool): Show in gallery

        Returns:
            properties_models.PropertyImage: Property image object created
        """

        if not property:
            property = self.create_property()

        image_file = get_test_image(image_name)

        property_image = properties_models.PropertyImage.objects.create(
            property=property,
            alt_text=self.create_translation(
                f"alt_text_test {image_name}", alt_text_es, alt_text_en
            ),
            show_gallery=show_gallery,
        )
        property_image.image = image_file
        property_image.save()

        return property_image

    def create_tag(
        self,
        name: str = "Tag test",
        es: str = "Etiqueta de prueba",
        en: str = "Test tag",
    ) -> properties_models.Tag:
        """Create a tag object

        Args:
            name (str): Tag name
            es (str): Spanish tag name
            en (str): English tag name

        Returns:
            properties_models.Tag: Tag object created
        """

        return properties_models.Tag.objects.create(
            name=self.create_translation(name, es, en),
        )


class TestPostsModelBase(TestCase):
    """Test blog models"""

    def create_post(
        self,
        title: str = "Post test",
        lang: str = "es",
        description: str = "Test description",
        keywords: str = "test, keywords",
        author: str = "Itzimna Team",
        content: str = "#Test \n**conten**t",
    ) -> blog_models.Post:
        """Create a post object"""

        return blog_models.Post.objects.create(
            title=title,
            lang=lang,
            description=description,
            keywords=keywords,
            author=author,
            content=content,
        )

    def create_image(
        self,
        post: blog_models.Post = None,
        name: str = "Image test",
        image_name: str = "test.webp",
    ) -> blog_models.Image:
        """Create a image object"""

        if not post:
            post = self.create_post()

        image_file = get_test_image(image_name)

        return blog_models.Image.objects.create(
            name=name,
            image=image_file,
        )


class TestSearchLinkModelBase(TestCase):
    """Test search links models"""
    
    def create_translation(
        self, key: str, es: str = "Traducción de prueba", en: str = "Test translation"
    ) -> translations_models.Translation:
        """Create a translation object

        Args:
            key (str): Translation key
            es (str): Spanish translation
            en (str): English translation

        Returns:
            Translation: Translation object created
        """

        return translations_models.Translation.objects.create(
            key=key,
            es=es,
            en=en,
        )

    def create_search_link(
        self,
        title: translations_models.Translation = None,
        description: translations_models.Translation = None,
        url: str = "https://www.google.com",
        image_name: str = "test.webp",
    ) -> content_models.SearchLink:
        """Create a search link object"""
        
        if not title:
            title = self.create_translation(f"search link {image_name}")
            
        if not description:
            description = self.create_translation(f"search link {image_name}")

        image_file = get_test_image(image_name)

        return content_models.SearchLink.objects.create(
            title=title,
            description=description,
            url=url,
            image=image_file,
        )


class TestContentModelBase(TestCase):
    """Test content models"""

    def create_best_developments_image(
        self,
        image_name: str = "best_development_image.webp",
        alt_text_es: str = "Imagen de mejor desarrollo",
        alt_text_en: str = "Best development image",
        translation_key_posfix: str = "",
    ) -> content_models.BestDevelopmentsImage:
        """Create a BestDevelopmentsImage object"""

        image_file = get_test_image(image_name)

        return content_models.BestDevelopmentsImage.objects.create(
            image=image_file,
            alt_text=translations_models.Translation.objects.create(
                key=f"best_development_image_{image_name}_{translation_key_posfix}",
                es=alt_text_es,
                en=alt_text_en,
            ),
        )
