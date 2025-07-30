from django.contrib import admin

from .models import Product, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("full_path", "name", "short_description", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active", "parent")
    ordering = ("parent__name", "name")

    def full_path(self, obj):
        return obj.get_full_path()

    full_path.short_description = "Category"

    def short_description(self, obj):
        return (
            (obj.description[:50] + "...")
            if obj.description and len(obj.description) > 50
            else obj.description
        )

    short_description.short_description = "Description"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "is_active", "created_at")
    search_fields = ("sku", "name", "description")
    list_filter = ("is_active", "category")
    autocomplete_fields = ("category",)
