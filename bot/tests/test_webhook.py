import pytest
from unittest.mock import Mock, patch, AsyncMock
from django.test import RequestFactory
from django.http import HttpResponseForbidden, HttpResponse
import json


class TestTelegramWebhookView:
    """Тесты для обработки вебхука"""

    @pytest.fixture
    def factory(self):
        return RequestFactory()

    def test_webhook_invalid_secret_token(self, factory):
        """Тест невалидного секретного токена"""
        from bot.views import TelegramWebhookView

        request = factory.post('/webhook/', {}, content_type='application/json')
        request.headers = {'X-Telegram-Bot-Api-Secret-Token': 'invalid_token'}

        view = TelegramWebhookView()
        response = view.post(request)

        assert isinstance(response, HttpResponseForbidden)
        assert response.content == b'Invalid secret token'

    @patch('bot.views.create_application')
    @patch('bot.views.Update')
    @patch('bot.views.asyncio')
    def test_webhook_valid_request(self, mock_asyncio, mock_update, mock_create_application, factory):
        """Тест валидного запроса вебхука"""
        from bot.views import TelegramWebhookView

        # Настройка моков
        mock_application = AsyncMock()
        mock_create_application.return_value = mock_application
        mock_update_instance = Mock()
        mock_update.de_json.return_value = mock_update_instance

        # Создание запроса
        request_data = {'update_id': 1, 'message': {'text': '/start'}}
        request = factory.post('/webhook/', json.dumps(request_data), content_type='application/json')
        request.headers = {'X-Telegram-Bot-Api-Secret-Token': 'test_secret'}

        view = TelegramWebhookView()
        response = view.post(request)

        # Проверки
        assert isinstance(response, HttpResponse)
        assert response.content == b'OK'
        mock_create_application.assert_called_once()
        mock_update.de_json.assert_called_once()

    def test_webhook_invalid_json(self, factory):
        """Тест невалидного JSON"""
        from bot.views import TelegramWebhookView

        request = factory.post('/webhook/', 'invalid json', content_type='application/json')
        request.headers = {'X-Telegram-Bot-Api-Secret-Token': 'test_secret'}

        view = TelegramWebhookView()
        response = view.post(request)

        assert isinstance(response, HttpResponse)
        assert response.content == b'OK'  # Обработка ошибок внутри try-except