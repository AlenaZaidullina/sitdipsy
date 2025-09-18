from django.contrib import admin
from .models import Testimonial

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_preview', 'alt_text', 'order', 'created_at', 'is_active']
    list_display_links = ['id', 'image_preview']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['image_preview']
    search_fields = ['alt_text']

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 50px;" />'
        return "Нет изображения"
    image_preview.short_description = 'Превью'
    image_preview.allow_tags = True

admin.site.register(Testimonial, TestimonialAdmin)
