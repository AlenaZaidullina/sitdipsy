from django.core.management.base import BaseCommand
import asyncio
from bot.views import create_application


class Command(BaseCommand):
    help = 'Run Telegram bot in polling mode'

    def handle(self, *args, **options):
        self.stdout.write("Starting Telegram bot in polling mode...")

        async def run_polling():
            try:

                application = create_application()


                await application.initialize()
                await application.start()

                self.stdout.write(
                    self.style.SUCCESS("✅ Bot started successfully in polling mode!")
                )
                self.stdout.write("🤖 Bot is now listening for messages...")

                # Запускается polling
                await application.updater.start_polling()

                # Бесконечный цикл чтобы бот не завершался
                while True:
                    await asyncio.sleep(3600)  # Спит 1 час

            except KeyboardInterrupt:
                self.stdout.write("Stopping bot...")
                await application.updater.stop()
                await application.stop()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))
            finally:
                if 'application' in locals():
                    await application.shutdown()

        # Запускается асинхронная функция
        asyncio.run(run_polling())