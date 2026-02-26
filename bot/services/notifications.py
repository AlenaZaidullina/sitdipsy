import logging
from django.conf import settings
from asgiref.sync import sync_to_async
from telegram import Bot
from ..models import NewDatesSubscription

logger = logging.getLogger(__name__)


class NotificationService:
    @staticmethod
    async def send_new_dates_notification(new_dates):
        try:
            bot_token = settings.TELEGRAM_BOT_TOKEN
            if not bot_token:
                logger.warning("TELEGRAM_BOT_TOKEN не установлен")
                return False

            # Получает активных подписчиков синхронно
            def get_subscribers_sync():
                return list(NewDatesSubscription.objects.select_related('client')
                          .filter(is_active=True))

            subscribers = await sync_to_async(get_subscribers_sync)()

            if not subscribers:
                logger.info("Нет активных подписчиков")
                return False

            dates_list = "\n".join([f"• {date.strftime('%d.%m.%Y')}" for date in new_dates])
            message = (
                "📢 Появились новые даты для консультаций:\n\n"
                f"{dates_list}\n\n"
                "Записаться можно на сайте:\n"
                f"{settings.CONSULTATION_PAGE_URL}"
            )

            bot = Bot(token=bot_token)

            for subscription in subscribers:
                try:
                    await bot.send_message(
                        chat_id=subscription.client.telegram_id,
                        text=message
                    )
                except Exception as e:
                    logger.error(f"Ошибка отправки для {subscription.client.telegram_id}: {e}")
                    # Деактивирует подписку
                    async def deactivate_sub(sub):
                        sub.is_active = False
                        await sync_to_async(sub.save)()
                    await deactivate_sub(subscription)

            return True

        except Exception as e:
            logger.error(f"Notification error: {str(e)}")
            return False