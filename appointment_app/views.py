from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from .models import Appointment, AvailableDate, AvailableTime, TelegramNotification, Consent
from datetime import datetime, date
from django.contrib import messages
from django.shortcuts import redirect
import requests
import json
from django.conf import settings
import logging
from django.db import transaction
from django.views.generic import TemplateView
from bot.services.urls import BotURLs
from asgiref.sync import sync_to_async


logger = logging.getLogger(__name__)


def consent_form(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')

        if not full_name:
            messages.error(request, 'Пожалуйста, введите ваше ФИО')
            return render(request, 'appointment_app/consent_form.html')

        # Сохраняется согласие в БД
        Consent.objects.create(
            full_name=full_name,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        # Сохраняется в сессии, что согласие получено
        request.session['pd_consent_given'] = True
        request.session['pd_consent_name'] = full_name
        request.session['pd_consent_time'] = timezone.now().isoformat()

        messages.success(request, 'Согласие на обработку персональных данных успешно предоставлено')
        return redirect('/#appointment')

    return render(request, 'appointment_app/consent_form.html')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@ensure_csrf_cookie
def appointment(request):

    # Проверяется, дано ли согласие
    if not request.session.get('pd_consent_given'):
        messages.error(request, 'Для записи на консультацию необходимо сначала дать согласие на обработку персональных данных')
        return redirect('consent_form')


    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST

            full_name = data.get('full_name')
            phone = data.get('phone')
            consultation_type = data.get('consultation_type')
            selected_datetime = data.get('selected_date')

            if not all([full_name, phone, consultation_type, selected_datetime]):
                return JsonResponse({'status': 'error', 'message': 'Заполните все поля'}, status=400)

            # Парсим дату и время
            date_part, time_part = selected_datetime.split(', ')
            day, month = date_part.split()
            month_map = {
                'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
                'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
            }
            month_num = month_map.get(month.lower(), 1)
            day_num = int(day)
            current_year = datetime.now().year
            date_obj = date(current_year, month_num, day_num)
            time_obj = datetime.strptime(time_part, '%H:%M').time()

            # АТОМАРНАЯ операция: проверка и бронирование времени
            with transaction.atomic():
                # Ищет AvailableDate для указанной даты
                available_date = AvailableDate.objects.filter(
                    date=date_obj,
                    is_available=True
                ).first()

                if not available_date:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Выбранная дата недоступна'
                    }, status=400)


                available_time = AvailableTime.objects.select_for_update().filter(
                    date=available_date,
                    time=time_obj,
                    is_booked=False
                ).first()

                if not available_time:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Выбранное время уже занято или недоступно'
                    }, status=400)

                # Создается запись
                appointment = Appointment.objects.create(
                    full_name=full_name,
                    phone=phone,
                    consultation_type=consultation_type,
                    date=date_obj,
                    time=time_obj,
                    pd_consent=data.get('pd_consent', False)
                )

                # Помечает время как забронированное
                available_time.is_booked = True
                available_time.booked_at = timezone.now()
                available_time.save()

            # Отправляется уведомление в Telegram
            send_telegram_notification(appointment)

            return JsonResponse({
                'status': 'success',
                'message': 'Запись успешно создана',
                'appointment_id': appointment.id
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Неверный формат данных'
            }, status=400)
        except Exception as e:
            logger.error(f"Error creating appointment: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Ошибка при создании записи. Попробуйте еще раз.'
            }, status=400)

    return render(request, 'appointment_app/appointment.html')


def get_available_dates(request):
    try:
        today = timezone.now().date()
        # Получает даты, у которых есть доступные временные слоты
        available_dates = AvailableDate.objects.filter(
            date__gte=today,
            is_available=True
        ).filter(
            available_times__is_booked=False
        ).distinct().values_list('date', flat=True)

        dates = [date.strftime('%Y-%m-%d') for date in available_dates]
        return JsonResponse({
            'status': 'success',
            'available_dates': dates
        })
    except Exception as e:
        logger.error(f"Error in get_available_dates: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def get_available_times(request, date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        available_date = AvailableDate.objects.filter(
            date=date_obj,
            is_available=True
        ).first()

        if not available_date:
            return JsonResponse({
                'status': 'error',
                'message': 'Дата недоступна',
                'available_times': []
            }, status=200)

        times = AvailableTime.objects.filter(
            date=available_date,
            is_booked=False
        ).values_list('time', flat=True)

        times_list = [time.strftime('%H:%M') for time in times]
        return JsonResponse({
            'status': 'success',
            'available_times': times_list
        })
    except Exception as e:
        logger.error(f"Error in get_available_times: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def send_telegram_notification(appointment):
    try:
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        chat_ids = TelegramNotification.objects.filter(is_active=True).values_list('chat_id', flat=True)

        if not bot_token or not chat_ids:
            return False

        message = (
            f"📅 Новая запись на консультацию:\n\n"
            f"👤 Имя: {appointment.full_name}\n"
            f"📞 Телефон: {appointment.phone}\n"
            f"🕒 Тип: {appointment.get_consultation_type_display()}\n"
            f"📅 Дата: {appointment.date.strftime('%d.%m.%Y')}\n"
            f"⏰ Время: {appointment.time.strftime('%H:%M')}\n\n"
            f"Для подтверждения перейдите в админ-панель."
        )

        for chat_id in chat_ids:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message}
            requests.post(url, data=data)

        return True
    except Exception as e:
        logger.error(f"Telegram notification error: {str(e)}")
        return False


async def send_new_dates_notification(new_dates):
    try:
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if not bot_token:
            logger.warning("TELEGRAM_BOT_TOKEN не установлен. Уведомления не отправлены.")
            return False

        # Импортирует модель из бота
        from bot.models import NewDatesSubscription

        # Получает активных подписчиков
        subscribers = await sync_to_async(NewDatesSubscription.objects.filter)(
            is_active=True
        )
        subscribers = await sync_to_async(list)(subscribers)

        if not subscribers:
            logger.info("Нет активных подписчиков для уведомлений")
            return False

        dates_list = "\n".join([f"• {date.strftime('%d.%m.%Y')}" for date in new_dates])
        message = (
            "📢 Появились новые даты для консультаций:\n\n"
            f"{dates_list}\n\n"
            "Записаться можно на сайте:\n"
            f"{BotURLs.consultation_page()}"
        )

        for subscription in subscribers:
            try:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = {
                    'chat_id': subscription.client.telegram_id,
                    'text': message
                }
                response = requests.post(url, data=data)
                response.raise_for_status()
            except Exception as e:
                logger.error(f"Ошибка отправки уведомления для {subscription.client.telegram_id}: {e}")
                # Деактивируем подписку при ошибке
                subscription.is_active = False
                await sync_to_async(subscription.save)()

        return True
    except Exception as e:
        logger.error(f"New dates notification error: {str(e)}")
        return False


class PrivacyPolicyView(TemplateView):
    template_name = "appointment_app/privacy_policy.html"