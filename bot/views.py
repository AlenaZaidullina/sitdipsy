import json
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import asyncio

from .services.bot_handlers import (start,
                                    handle_main_menu,
                                    handle_test_confirmation,
                                    handle_start_button,
                                    handle_main_reply_button,
                                    handle_contact_button,
                                    handle_consultation_issue,
                                    handle_anxiety_booking,
                                    handle_take_test_button,
                                    handle_test_selection,
                                    handle_test_result_level,
                                    handle_guide_request,
                                    handle_checklist_request,
                                    handle_memo_request,
                                    handle_about_method_request,
                                    handle_about_consultation_request,
                                    handle_main_menu_callback,
                                    handle_subscribe_materials,
                                    handle_unsubscribe_materials,
                                    unsubscribe_command,
                                    handle_test_completion,
                                    handle_subscribe_dates,
                                    handle_unsubscribe_dates
                                    )


def create_application():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # Основные обработчики callback_data
    application.add_handler(CallbackQueryHandler(handle_checklist_request, pattern='^get_checklist$'))
    application.add_handler(CallbackQueryHandler(handle_memo_request, pattern='^get_memo$'))
    application.add_handler(CallbackQueryHandler(handle_guide_request, pattern='^get_guide$'))
    application.add_handler(CallbackQueryHandler(handle_test_confirmation, pattern='^(test_yes|test_no)$'))
    application.add_handler(CallbackQueryHandler(handle_consultation_issue,
                                                 pattern='^(issue_anxiety|issue_depression|issue_procrastination|issue_other)$'))
    application.add_handler(CallbackQueryHandler(handle_anxiety_booking, pattern='^(anxiety_book)$'))
    application.add_handler(CallbackQueryHandler(handle_test_selection, pattern='^(test_bai|test_bdi|test_cognitive)$'))
    application.add_handler(
        CallbackQueryHandler(handle_test_result_level, pattern='^(result_high|result_medium|result_low)$'))
    application.add_handler(CallbackQueryHandler(handle_about_method_request, pattern='^about_method$'))
    application.add_handler(CallbackQueryHandler(handle_about_consultation_request, pattern='^about_consultation$'))
    application.add_handler(CallbackQueryHandler(handle_main_menu, pattern='^take_test$'))
    application.add_handler(CallbackQueryHandler(handle_main_menu, pattern='^book_consultation$'))
    application.add_handler(CallbackQueryHandler(handle_subscribe_materials, pattern='^subscribe_materials$'))
    application.add_handler(CallbackQueryHandler(handle_main_menu_callback, pattern='^main_menu$'))
    application.add_handler(CallbackQueryHandler(handle_unsubscribe_materials, pattern='^unsubscribe_materials$'))
    application.add_handler(CallbackQueryHandler(handle_test_completion, pattern='^test_completed$'))
    application.add_handler(CallbackQueryHandler(handle_subscribe_dates, pattern='^subscribe_dates$'))
    application.add_handler(CallbackQueryHandler(handle_unsubscribe_dates, pattern='^unsubscribe_dates$'))



    # Обработчики для reply-кнопок
    application.add_handler(MessageHandler(filters.Text(["🚀 Начать работу", "Начать работу"]), handle_start_button))
    application.add_handler(
        MessageHandler(filters.Text(["📋 Главное меню", "Главное меню", "меню"]), handle_main_reply_button))
    application.add_handler(
        MessageHandler(filters.Text(["📞 Связаться со мной", "Связаться", "📞 Связаться с психологом"]), handle_contact_button))
    application.add_handler(
        MessageHandler(filters.Text(["🧪 Пройти тесты", "Пройти тесты", "тесты"]), handle_take_test_button))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))

    return application


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
        if secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
            return HttpResponseForbidden('Invalid secret token')

        try:
            # Создаем и инициализируем application для каждого запроса
            application = create_application()
            body = json.loads(request.body.decode('utf-8'))
            update = Update.de_json(body, application.bot)

            async def process():
                await application.initialize()
                await application.process_update(update)
                await application.shutdown()

            asyncio.run(process())

        except Exception as e:
            print(f"Error processing update: {e}")

        return HttpResponse('OK')