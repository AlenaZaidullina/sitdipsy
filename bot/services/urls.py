from django.conf import settings


class BotURLs:
    """Класс для управления всеми URL бота"""

    @staticmethod
    def consultation_page():
        return settings.CONSULTATION_PAGE_URL

    @staticmethod
    def booking():
        return settings.BOOKING_URL

    @staticmethod
    def work_stages():
        return settings.WORK_STAGES_URL

    @staticmethod
    def consultation_rules():
        return settings.CONSULTATION_RULES_URL

    @staticmethod
    def get_website_url_with_referral():
        base_url = BotURLs.consultation_page()
        return f"{base_url}?source=telegram_bot"