from django.contrib import admin
from blog import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "lang", "created_at")
    search_fields = ("title", "description", "content")
    list_filter = ("lang", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"