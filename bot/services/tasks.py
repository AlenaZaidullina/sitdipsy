from celery import shared_task
from telegram import Bot
from django.conf import settings
from asgiref.sync import sync_to_async
from .keyboards import main_menu_keyboard
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from .urls import BotURLs

@shared_task
def send_follow_up_message(chat_id):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        async def send_message():
            await bot.send_message(
                chat_id=chat_id,
                text="Как вам материал? Если хотите разобрать вашу ситуацию индивидуально, запишитесь на консультацию",
                reply_markup=main_menu_keyboard()
            )

        # Запускается асинхронная функция в синхронном контексте
        import asyncio
        asyncio.run(send_message())

    except Exception as e:
        print(f"Error sending follow-up message: {e}")


@shared_task
def send_anxiety_followup(chat_id, client_id):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        async def send_message():
            keyboard = [
                [InlineKeyboardButton("📅 Записаться сейчас", url=BotURLs.consultation_page())]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await bot.send_message(
                chat_id=chat_id,
                text="Как прошла самодиагностика? Если хотите обсудить результаты и начать работу с тревогой, "
                     "запишитесь на консультацию👇",
                reply_markup=reply_markup
            )

            # Обновляется статус в базе
            from ..models import ConsultationRequest
            request = await sync_to_async(ConsultationRequest.objects.get)(client__telegram_id=client_id)
            request.status = 'followup_sent'
            await sync_to_async(request.save)()

        asyncio.run(send_message())
    except Exception as e:
        print(f"Error sending anxiety follow-up: {e}")



@shared_task
def send_newsletter_material_task(material_id):
    """Отправляет конкретный материал всем подписанным пользователям"""
    from ..models import Client, NewsletterMaterial

    try:
        material = NewsletterMaterial.objects.get(id=material_id, is_active=True)
    except NewsletterMaterial.DoesNotExist:
        return

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    # Найти всех подписанных пользователей
    subscribed_clients = Client.objects.filter(subscribed_to_newsletter=True)

    for client in subscribed_clients:
        try:
            async def send_material():
                if material.content:
                    await bot.send_document(
                        chat_id=client.telegram_id,
                        document=material.content,
                        caption=f"📬 {material.title}\n\n{material.content}"
                    )
                else:
                    await bot.send_message(
                        chat_id=client.telegram_id,
                        text=f"📬 {material.title}\n\n{material.content}"
                    )

            asyncio.run(send_material())

        except Exception as e:
            print(f"Error sending to {client.telegram_id}: {e}")