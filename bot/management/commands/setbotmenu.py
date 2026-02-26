from django.core.management.base import BaseCommand
from telegram import Bot, BotCommand
from django.conf import settings
import asyncio
import requests

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Устанавливается меню бота...')

        async def set_menu():
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

            # Список команд для меню
            commands = [
                BotCommand("menu", "📋Главное меню"),
                BotCommand("subscribe", "💡 Подписаться на рассылку"),
                BotCommand("unsubscribe", "🔕 Отписаться от рассылки"),
                BotCommand("appointment", "📅 Записаться на консультацию")
            ]

            await bot.set_my_commands(commands)

            self.stdout.write(self.style.SUCCESS("Меню бота установлено"))
            self.stdout.write("Команды которые теперь доступны:")

            for cmd in commands:
                self.stdout.write(f"   /{cmd.command} - {cmd.description}")

            result = await bot.get_my_commands()
            self.stdout.write(f"\n📊 Всего команд установлено: {len(result)}")

        asyncio.run(set_menu())


