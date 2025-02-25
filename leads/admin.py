from django.contrib import admin
from django.utils.html import format_html

from leads import models


@admin.register(models.Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "whatsapp_link",
        "name",
        "message",
        "property",
        "created_at",
    ]
    search_fields = ["name", "email", "message"]
    list_per_page = 10
    list_filter = ["created_at", "property", "updated_at", "property__name"]
    readonly_fields = ["created_at", "updated_at"]

    # Custom fields
    def whatsapp_link(self, obj):
        return format_html(
            f'<a href="{obj.get_whatsapp_link()}" target="_blank">{obj.phone}</a>'
        )
    
    # Names for custom fields
    whatsapp_link.short_description = "WhatsApp"
    whatsapp_link.ordering_field = "phone"