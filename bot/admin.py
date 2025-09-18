from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Client, ContentBlock, ConsultationRequest, NewsletterMaterial

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'first_name', 'last_name', 'created_at', 'subscribed_to_newsletter')
    list_filter = ('created_at', 'subscribed_to_newsletter')
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name')

@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'is_active')
    list_filter = ('content_type', 'is_active')
    list_editable = ('is_active',)


@admin.register(NewsletterMaterial)
class NewsletterMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'is_active', 'created_at')
    list_filter = ('content_type', 'is_active')
    list_editable = ('is_active',)
    actions = ['send_to_subscribers']  # Действие для отправки

    def send_to_subscribers(self, request, queryset):
        """ Действие для отправки материалов подписчикам"""
        from .services.tasks import send_newsletter_material_task

        for material in queryset:
            if material.is_active:
                send_newsletter_material_task.delay(material.id)

        self.message_user(request, f"Материалы отправляются подписчикам")
        return HttpResponseRedirect(reverse('admin:bot_newslettermaterial_changelist'))

    send_to_subscribers.short_description = "Отправить выбранные материалы подписчикам"



@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('client', 'primary_issue', 'status', 'created_at')
    list_filter = ('status', 'primary_issue', 'created_at')
    list_editable = ('status',)
