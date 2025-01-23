from django.contrib import admin
from translations import models


@admin.register(models.TranslationGroup)
class TranslationGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    

@admin.register(models.Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('group', 'key', 'es', 'en', 'updated_at')
    search_fields = ('key', 'es', 'en')
    list_filter = ('group', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (
            'Información de la traducción',
            {
                'fields': (
                    'key',
                    'group',
                    ('es', 'en'),
                )
            }
        ),
        (
            'Fechas',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )
    list_max_show_all = 29
    list_editable = ('es', 'en')
    list_display_links = ('key',)