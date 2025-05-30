from django.contrib import admin
from content import models


@admin.register(models.BestDevelopmentsImage)
class BestDevelopmentsImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "alt_text"]
    search_fields = ["alt_text"]
