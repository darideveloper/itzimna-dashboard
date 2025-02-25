from django.contrib import admin
from leads import models


@admin.register(models.Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'message', 'property', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_per_page = 10
    list_filter = ['created_at', 'property', 'updated_at', 'property__name']
    readonly_fields = ['created_at', 'updated_at']
