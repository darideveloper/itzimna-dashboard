from django.contrib import admin, messages
from properties import models


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "logo",
        "location",
        "show_contact_info",
        "type",
    )
    search_fields = ("name", "description_es", "description_en")


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "details",
    )
    search_fields = ("name__es", "name__en", "details")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "details",
    )
    search_fields = ("name__es", "name__en", "details")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name__es", "name__en")


@admin.register(models.ShortDescription)
class ShortDescriptionAdmin(admin.ModelAdmin):
    list_display = ("description", "__str__",)
    search_fields = ("description__es", "description__en")


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "email",
    )


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "category",
        "location",
        "company",
        "seller",
    )
    search_fields = (
        "name",
        "price",
        "description_es",
        "description_en",
        "company__name",
        "seller__first_name",
        "seller__last_name",
        "seller__email",
    )
    list_filter = (
        "category",
        "location",
        "company",
        "seller",
        "tags",
        "active",
        "featured",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Información de la propiedad",
            {
                "fields": (
                    "name",
                    "slug",
                    "company",
                    "location",
                    "seller",
                    "category",
                    "tags",
                    "price",
                    "meters",
                    "active",
                    "featured",
                    "short_description",
                    "google_maps_src",
                    "review_name",
                    "review_rating",
                    "description_es",
                    "description_en",
                ),
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):

        # Catch error if the google maps src is not valid
        try:
            obj.save()
        except Exception as e:
            messages.set_level(request, messages.WARNING)
            self.message_user(request, f"Error: {e}", level="ERROR")
            return


@admin.register(models.PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "image",
    )
    search_fields = ("property__name", "alt_text__es", "alt_text__en")
    list_filter = (
        "property",
        "created_at",
        "updated_at",
    )
