import pytest
from unittest.mock import AsyncMock, Mock, patch



class TestStartHandler:
    """Тесты для обработчика команды /start"""

    @pytest.mark.asyncio
    async def test_start_new_user(self, mock_update, mock_context, mock_models, mock_sync_to_async):
        """Тест команды /start для нового пользователя"""
        from bot.services.bot_handlers import start

        # Настройка моков
        mock_client_instance = Mock()
        mock_models['Client'].objects.get_or_create.return_value = (mock_client_instance, True)
        mock_update.message.reply_text = AsyncMock()

        # Вызов функции
        await start(mock_update, mock_context)

        # Проверки
        mock_models['Client'].objects.get_or_create.assert_called_once()
        assert mock_update.message.reply_text.call_count == 2
        # Проверяет аргументы вызовов
        calls = mock_update.message.reply_text.call_args_list
        assert 'Привет' in calls[0][0][0]  # Первое сообщение
        assert 'Выберите действие' in calls[1][0][0]  # Второе сообщение

    @pytest.mark.asyncio
    async def test_start_existing_user(self, mock_update, mock_context, mock_models, mock_sync_to_async):
        """Тест команды /start для существующего пользователя"""
        from bot.services.bot_handlers import start

        # Настройка моков
        mock_client_instance = Mock()
        mock_models['Client'].objects.get_or_create.return_value = (mock_client_instance, False)
        mock_update.message.reply_text = AsyncMock()

        # Вызов функции
        await start(mock_update, mock_context)

        # Проверки
        mock_models['Client'].objects.get_or_create.assert_called_once()
        assert mock_update.message.reply_text.call_count == 2


class TestMainMenuHandlers:
    """Тесты для обработчиков главного меню"""

    @pytest.mark.asyncio
    async def test_handle_main_menu_take_test(self, mock_callback_query, mock_context, mock_sync_to_async):
        """Тест выбора 'Пройти тесты' в главном меню"""
        from bot.services.bot_handlers import handle_main_menu

        # Мокируем query как атрибут update
        mock_update = Mock()
        mock_update.callback_query = mock_callback_query
        mock_callback_query.data = 'take_test'
        mock_callback_query.answer = AsyncMock()
        mock_callback_query.edit_message_text = AsyncMock()

        await handle_main_menu(mock_update, mock_context)

        mock_callback_query.answer.assert_called_once()
        mock_callback_query.edit_message_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_main_menu_book_consultation(self, mock_callback_query, mock_context, mock_sync_to_async):
        """Тест выбора 'Записаться на консультацию' в главном меню"""
        from bot.services.bot_handlers import handle_main_menu

        # Мокирует query как атрибут update
        mock_update = Mock()
        mock_update.callback_query = mock_callback_query
        mock_callback_query.data = 'book_consultation'
        mock_callback_query.answer = AsyncMock()
        mock_callback_query.edit_message_text = AsyncMock()

        await handle_main_menu(mock_update, mock_context)

        mock_callback_query.answer.assert_called_once()
        mock_callback_query.edit_message_text.assert_called_once()


class TestContentHandlers:
    """Тесты для обработчиков контента"""

    @pytest.mark.asyncio
    async def test_handle_guide_request(self, mock_callback_query, mock_context, mock_models, mock_sync_to_async):
        """Тест запроса гида"""
        from bot.services.bot_handlers import handle_guide_request

        # Мокируем query как атрибут update
        mock_update = Mock()
        mock_update.callback_query = mock_callback_query
        mock_callback_query.answer = AsyncMock()

        # Мокируем ContentBlock
        mock_content = Mock()
        mock_models['ContentBlock'].objects.get.return_value = mock_content

        # Мокируем send_content_by_type
        with patch('bot.services.bot_handlers.send_content_by_type', new_callable=AsyncMock) as mock_send:
            await handle_guide_request(mock_update, mock_context)

            mock_callback_query.answer.assert_called_once()
            mock_send.assert_called_once_with(mock_update, 'gift_guide', mock_callback_query.message)

    @pytest.mark.asyncio
    async def test_handle_checklist_request(self, mock_callback_query, mock_context, mock_models, mock_sync_to_async):
        """Тест запроса чек-листа"""
        from bot.services.bot_handlers import handle_checklist_request

        # Мокируем query как атрибут update
        mock_update = Mock()
        mock_update.callback_query = mock_callback_query
        mock_callback_query.answer = AsyncMock()

        # Мокируем send_content_by_type
        with patch('bot.services.bot_handlers.send_content_by_type', new_callable=AsyncMock) as mock_send:
            await handle_checklist_request(mock_update, mock_context)

            mock_callback_query.answer.assert_called_once()
            mock_send.assert_called_once_with(mock_update, 'checklist', mock_callback_query.message)


class TestSubscriptionHandlers:
    """Тесты для обработчиков подписок"""

    @pytest.mark.asyncio
    async def test_handle_subscribe_materials_new(self, mock_callback_query, mock_context, mock_models, mock_sync_to_async):
        """Тест подписки на материалы (новый пользователь)"""
        from bot.services.bot_handlers import handle_subscribe_materials

        # Мокируем query как атрибут update
        mock_update = Mock()
        mock_update.callback_query = mock_callback_query

        mock_client = Mock()
        mock_client.subscribed_to_newsletter = False
        mock_models['Client'].objects.get.return_value = mock_client
        mock_callback_query.answer = AsyncMock()
        mock_callback_query.edit_message_text = AsyncMock()

        await handle_subscribe_materials(mock_update, mock_context)

        mock_models['Client'].objects.get.assert_called_once_with(telegram_id=123456789)
        assert mock_client.subscribed_to_newsletter is True
        mock_callback_query.edit_message_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_unsubscribe_materials(self, mock_callback_query, mock_context, mock_models, mock_sync_to_async):
        """Тест отписки от материалов"""
        from bot.services.bot_handlers import handle_unsubscribe_materials

        # Мокируем query как атрибут update
        mock_update = Mock()
        mock_update.callback_query = mock_callback_query

        mock_client = Mock()
        mock_client.subscribed_to_newsletter = True
        mock_models['Client'].objects.get.return_value = mock_client
        mock_callback_query.answer = AsyncMock()
        mock_callback_query.edit_message_text = AsyncMock()

        await handle_unsubscribe_materials(mock_update, mock_context)

        mock_models['Client'].objects.get.assert_called_once_with(telegram_id=123456789)
        assert mock_client.subscribed_to_newsletter is False
        mock_callback_query.edit_message_text.assert_called_once()


class TestTestHandlers:
    """Тесты для обработчиков тестов"""

    @pytest.mark.asyncio
    async def test_handle_test_confirmation_yes(self, mock_callback_query, mock_context, mock_sync_to_async):
        """Тест подтверждения прохождения теста (да)"""
        from bot.services.bot_handlers import handle_test_confirmation

        # Мокируем query как атрибут update
        mock_update = Mock()
        mock_update.callback_query = mock_callback_query

        mock_callback_query.data = 'test_yes'
        mock_callback_query.answer = AsyncMock()
        mock_callback_query.message.reply_text = AsyncMock()

        await handle_test_confirmation(mock_update, mock_context)

        mock_callback_query.answer.assert_called_once()
        mock_callback_query.message.reply_text.assert_called()

    @pytest.mark.asyncio
    async def test_handle_test_selection(self, mock_callback_query, mock_context, mock_sync_to_async):
        """Тест выбора теста"""
        from bot.services.bot_handlers import handle_test_selection

        # Мокируем query как атрибут update
        mock_update = Mock()
        mock_update.callback_query = mock_callback_query

        mock_callback_query.data = 'test_bai'
        mock_callback_query.answer = AsyncMock()
        mock_callback_query.message.reply_text = AsyncMock()

        await handle_test_selection(mock_update, mock_context)

        mock_callback_query.answer.assert_called_once()
        assert mock_context.user_data['selected_test'] == 'test_bai'
        assert mock_context.user_data['test_name'] == 'Шкала тревоги Бека (BAI)'
        mock_callback_query.message.reply_text.assert_called()