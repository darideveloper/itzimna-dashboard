from django.contrib import admin
from content import models


@admin.register(models.BestDevelopmentsImage)
class BestDevelopmentsImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "alt_text"]
    search_fields = ["alt_text__es", "alt_text__en"]


@admin.register(models.SearchLink)
class SearchLinkAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "url"]
    search_fields = ["title__es", "title__en", "description__es", "description__en"]
