from django.contrib import admin
from .models import Appointment, AvailableDate, AvailableTime, TelegramNotification, NewDatesSubscriber, Consent
import csv
from django.http import HttpResponse
from bot.services.notifications import NotificationService
import asyncio



@admin.register(NewDatesSubscriber)
class NewDatesSubscriberAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'subscribed_at', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('chat_id',)

class AvailableTimeInline(admin.TabularInline):
    model = AvailableTime
    extra = 1
    min_num = 1


class AvailableDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'is_available', 'times_count')
    list_filter = ('is_available',)
    search_fields = ('date',)
    inlines = [AvailableTimeInline]
    actions = ['make_available', 'make_unavailable']

    def times_count(self, obj):
        return obj.available_times.count()

    times_count.short_description = 'Кол-во временных слотов'

    def make_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, "Выбранные даты стали доступными")

    make_available.short_description = "Сделать выбранные даты доступными"

    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, "Выбранные даты стали недоступными")

    make_unavailable.short_description = "Сделать выбранные даты недоступными"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Отправляем уведомления только для новых доступных дат
        if obj.is_available and not change:
            # Запускаем асинхронную задачу
            async def send_notification_async():
                await NotificationService.send_new_dates_notification([obj.date])

            # Запускаем в отдельном потоке
            import threading
            def run_async():
                asyncio.run(send_notification_async())

            thread = threading.Thread(target=run_async)
            thread.start()



class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'consultation_type', 'date', 'time', 'pd_consent', 'is_paid', 'is_confirmed', 'created_at')
    list_filter = ('consultation_type', 'is_paid', 'is_confirmed', 'date')
    search_fields = ('full_name', 'phone')
    list_editable = ('is_paid', 'is_confirmed')
    readonly_fields = ('created_at', 'pd_consent')
    actions = ['export_as_csv', 'confirm_selected', 'mark_as_paid']

    def confirm_selected(self, request, queryset):
        queryset.update(is_confirmed=True)
        self.message_user(request, "Выбранные записи подтверждены")

    confirm_selected.short_description = "Подтвердить выбранные записи"

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
        self.message_user(request, "Выбранные записи отмечены как оплаченные")

    mark_as_paid.short_description = "Отметить как оплаченные"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Экспортировать выбранные записи в CSV"


class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'is_booked')
    list_filter = ('date', 'is_booked')
    search_fields = ('date__date',)
    list_editable = ('is_booked',)


class TelegramNotificationAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'is_active')
    list_editable = ('is_active',)


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'ip_address', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('full_name', 'ip_address')
    readonly_fields = ('created_at', 'ip_address', 'user_agent')



admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AvailableDate, AvailableDateAdmin)
admin.site.register(AvailableTime, AvailableTimeAdmin)
admin.site.register(TelegramNotification, TelegramNotificationAdmin)