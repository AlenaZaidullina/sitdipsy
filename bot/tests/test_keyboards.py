import pytest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class TestKeyboards:
    """Тесты для клавиатур"""

    def test_main_menu_keyboard(self):
        """Тест главного меню клавиатуры"""
        from bot.services.keyboards import main_menu_keyboard

        keyboard = main_menu_keyboard()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 6
        assert keyboard.inline_keyboard[0][0].text == "🔍 Узнать уровень тревоги/депрессии"
        assert keyboard.inline_keyboard[0][0].callback_data == 'take_test'

    def test_test_confirmation_keyboard(self):
        """Тест клавиатуры подтверждения теста"""
        from bot.services.keyboards import test_confirmation_keyboard

        keyboard = test_confirmation_keyboard()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 2
        assert keyboard.inline_keyboard[0][0].text == "Да"
        assert keyboard.inline_keyboard[0][0].callback_data == 'test_yes'
        assert keyboard.inline_keyboard[1][0].text == "Нет"
        assert keyboard.inline_keyboard[1][0].callback_data == 'test_no'

    def test_consultation_issue_keyboard(self):
        """Тест клавиатуры выбора проблемы"""
        from bot.services.keyboards import consultation_issue_keyboard

        keyboard = consultation_issue_keyboard()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 6
        assert keyboard.inline_keyboard[0][0].text == "Тревога/страхи"
        assert keyboard.inline_keyboard[0][0].callback_data == 'issue_anxiety'

    def test_tests_keyboard(self):
        """Тест клавиатуры выбора тестов"""
        from bot.services.keyboards import tests_keyboard

        keyboard = tests_keyboard()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 3
        assert keyboard.inline_keyboard[0][0].text == "🧪 Шкала тревоги Бека (BAI)"
        assert keyboard.inline_keyboard[0][0].callback_data == 'test_bai'