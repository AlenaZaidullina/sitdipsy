from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_free', 'price', 'created_at')
    list_filter = ('is_free',)
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'is_free', 'price', 'document_file')
