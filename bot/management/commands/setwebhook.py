from django.core.management.base import BaseCommand
import requests
from django.conf import settings


class Command(BaseCommand):
    help = 'Set Telegram webhook URL'

    def handle(self, *args, **options):
        webhook_url = f"{settings.WEBHOOK_URL}/bot/webhook/"

        response = requests.post(
            f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook',
            json={
                'url': webhook_url,
                'secret_token': settings.TELEGRAM_WEBHOOK_SECRET,
                'drop_pending_updates': True
            }
        )

        if response.json().get('ok'):
            self.stdout.write(self.style.SUCCESS('Webhook set successfully!'))
        else:
            self.stdout.write(self.style.ERROR('Failed to set webhook'))
            self.stdout.write(self.style.ERROR(str(response.json())))