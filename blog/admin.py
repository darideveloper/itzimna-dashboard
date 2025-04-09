from django.contrib import admin
from django.utils.html import format_html

from blog import models
from utils.media import get_media_url


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "lang", "created_at")
    search_fields = ("title", "description", "content")
    list_filter = ("lang", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "custom_buttons")
    search_fields = ("name",)
    ordering = ("name",)
    date_hierarchy = "created_at"

    # Custom fields
    def custom_buttons(self, obj):
        """Create custom Imprimir and Ver buttons"""

        return format_html(
            """<button type="button"
                class="copy-btn btn btn-primary my-1 w-120" value-copy="{}">
                Copiar Enlace
            </button>""",
            get_media_url(obj.image),
        )

    # Rename custom fields
    custom_buttons.short_description = "Acciones"
