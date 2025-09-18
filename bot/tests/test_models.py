import pytest
from unittest.mock import Mock, patch


class TestModels:
    """Тесты для моделей (без обращения к БД)"""

    def test_client_str_representation(self):
        """Тест строкового представления клиента"""
        from bot.models import Client

        client = Client(telegram_id=123456, first_name='Test')
        assert str(client) == 'Test (123456)'

        client_without_name = Client(telegram_id=123456)
        assert str(client_without_name) == 'Клиент 123456'

    def test_content_block_str_representation(self):
        """Тест строкового представления блока контента"""
        from bot.models import ContentBlock

        content = ContentBlock(
            content_type='gift_guide',
            name='Test Guide'
        )

        # Мок для get_content_type_display
        with patch.object(content, 'get_content_type_display', return_value='Бесплатный гайд'):
            assert str(content) == 'Бесплатный гайд: Test Guide'

    def test_consultation_request_str_representation(self):
        """Тест строкового представления запроса на консультацию"""
        from bot.models import ConsultationRequest, Client

        client = Client(telegram_id=123456, first_name='Test')
        request = ConsultationRequest(client=client, status='new')

        assert str(request) == 'Запрос от Test (123456) (new)'

    def test_new_dates_subscription_str_representation(self):
        """Тест строкового представления подписки на даты"""
        from bot.models import NewDatesSubscription, Client

        client = Client(telegram_id=123456, first_name='Test')
        subscription = NewDatesSubscription(client=client, is_active=True)

        assert str(subscription) == 'Подписка Test (123456) (активна)'

        subscription.is_active = False
        assert str(subscription) == 'Подписка Test (123456) (неактивна)'