import pytest
from django.conf import settings


class TestBotURLs:
    """Тесты для URL утилит"""

    def test_consultation_page_url(self):
        """Тест URL страницы консультации"""
        from bot.services.urls import BotURLs

        url = BotURLs.consultation_page()
        assert url == settings.CONSULTATION_PAGE_URL

    def test_get_website_url_with_referral(self):
        """Тест URL с реферальной меткой"""
        from bot.services.urls import BotURLs

        url = BotURLs.get_website_url_with_referral()
        expected_url = f"{settings.CONSULTATION_PAGE_URL}?source=telegram_bot"
        assert url == expected_url

    def test_booking_url(self):
        """Тест URL бронирования"""
        from bot.services.urls import BotURLs

        url = BotURLs.booking()
        assert url == settings.BOOKING_URL