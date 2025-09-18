import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from django.conf import settings


@pytest.fixture(autouse=True)
def setup_settings():
    """Настройка настроек для тестов"""
    settings.TELEGRAM_BOT_TOKEN = 'test_token'
    settings.TELEGRAM_WEBHOOK_SECRET = 'test_secret'
    settings.WEBHOOK_URL = 'https://test-webhook.com'
    settings.CONSULTATION_PAGE_URL = 'https://test-consultation.com'
    settings.BOOKING_URL = 'https://test-booking.com'
    settings.WORK_STAGES_URL = 'https://test-work-stages.com'
    settings.CONSULTATION_RULES_URL = 'https://test-rules.com'


@pytest.fixture
def mock_telegram_user():
    """Мок пользователя Telegram"""
    return Mock(
        id=123456789,
        username='testuser',
        first_name='Test',
        last_name='User',
        is_bot=False
    )


@pytest.fixture
def mock_telegram_chat():
    """Мок чата Telegram"""
    return Mock(
        id=123456789,
        type='private'
    )


@pytest.fixture
def mock_telegram_message(mock_telegram_user, mock_telegram_chat):
    """Мок сообщения Telegram"""
    return Mock(
        message_id=1,
        from_user=mock_telegram_user,
        chat=mock_telegram_chat,
        text='/start'
    )


@pytest.fixture
def mock_update(mock_telegram_message):
    """Мок обновления Telegram"""
    update = Mock()
    update.effective_user = mock_telegram_message.from_user
    update.message = mock_telegram_message
    return update


@pytest.fixture
def mock_callback_query(mock_telegram_user, mock_telegram_message):
    """Мок callback query"""
    query = Mock()
    query.from_user = mock_telegram_user
    query.message = mock_telegram_message
    query.data = 'test_data'
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    return query


@pytest.fixture
def mock_context():
    """Мок контекста"""
    context = Mock()
    context.user_data = {}
    return context


@pytest.fixture
def mock_sync_to_async():
    """Мок для sync_to_async"""
    with patch('bot.services.bot_handlers.sync_to_async') as mock_sync:
        # Создаем обертку, которая возвращает асинхронную функцию
        async def async_wrapper(func, *args, **kwargs):
            return func(*args, **kwargs)

        mock_sync.side_effect = lambda func: lambda *args, **kwargs: async_wrapper(func, *args, **kwargs)
        yield mock_sync


@pytest.fixture
def mock_models(mock_sync_to_async):
    """Моки для моделей"""
    with patch('bot.services.bot_handlers.Client') as mock_client, \
            patch('bot.services.bot_handlers.ContentBlock') as mock_content, \
            patch('bot.services.bot_handlers.ConsultationRequest') as mock_request, \
            patch('bot.services.bot_handlers.NewDatesSubscription') as mock_subscription:
        # Настраиваем моки для методов объектов
        mock_client_instance = Mock()
        mock_client_instance.telegram_id = 123456789
        mock_client_instance.username = 'testuser'
        mock_client_instance.first_name = 'Test'
        mock_client_instance.last_name = 'User'

        # Мокируем методы моделей как синхронные функции
        mock_client.objects.get_or_create = Mock(return_value=(mock_client_instance, True))
        mock_client.objects.get = Mock(return_value=mock_client_instance)

        mock_content.objects.get = Mock(return_value=Mock())
        mock_request.objects.get = Mock(return_value=Mock())
        mock_subscription.objects.get_or_create = Mock(return_value=(Mock(), True))
        mock_subscription.objects.get = Mock(return_value=Mock())

        yield {
            'Client': mock_client,
            'ContentBlock': mock_content,
            'ConsultationRequest': mock_request,
            'NewDatesSubscription': mock_subscription
        }