from django.contrib import admin
from properties import models


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'details',)
    search_fields = ('name', 'details')


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'details',)
    search_fields = ('name', 'details')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'details',)
    search_fields = ('name', 'details')


@admin.register(models.ShortDescription)
class ShortDescriptionAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'email',
    )
    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'email',
    )


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'category',
        'location',
        'company',
        'seller',
    )
    search_fields = (
        'name',
        'price',
        'category__name',
        'location__name',
        'company__name',
        'seller__first_name',
        'seller__last_name',
        'seller__email',
    )
    list_filter = ('category', 'location', 'company', 'seller',)
    readonly_fields = ('created_at', 'updated_at',)
    fieldsets = (
        (
            'Información de la propiedad',
            {
                'fields': (
                    'name',
                    'company',
                    'location',
                    'seller',
                    'category',
                    'price',
                    'meters',
                    'active',
                    'featured',
                    'short_description',
                    ('description_es', 'description_en',)
                ),
            }
        ),
        (
            "Fechas",
            {
                'fields': (
                    'created_at',
                    'updated_at',
                ),
            }
        )
    )
    

@admin.register(models.PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image',)
    search_fields = ('property__name', 'caption',)
    list_filter = ('property', 'created_at', 'updated_at',)