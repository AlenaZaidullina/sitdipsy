from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from .urls import BotURLs


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔍 Узнать уровень тревоги/депрессии", callback_data='take_test')],
        [InlineKeyboardButton("📅 Записаться на консультацию", callback_data='book_consultation')],
        [InlineKeyboardButton("🎁 Получить гайд «5 техник КПТ»", callback_data='get_guide')],
        [InlineKeyboardButton("❔ Узнать подробнее про метод", url=BotURLs.consultation_page())],
        [InlineKeyboardButton("💡 Подписаться на полезные материалы", callback_data='subscribe_materials')],
        [InlineKeyboardButton("🔕 Отписаться от рассылки на полезные материалы", callback_data='unsubscribe_materials')]

    ]
    return InlineKeyboardMarkup(keyboard)

def get_start_keyboard():
    """Создает клавиатурную кнопку для старта"""
    keyboard = [
        [KeyboardButton("🚀 Начать работу")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_main_reply_keyboard():
    """Создает постоянную reply-кнопку для главного меню"""
    keyboard = [
        [KeyboardButton("📋 Главное меню")],
        [KeyboardButton("🧪 Пройти тесты")],
        [KeyboardButton("📞 Связаться с психологом")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def test_confirmation_keyboard():
    keyboard = [
        [InlineKeyboardButton("Да", callback_data='test_yes')],
        [InlineKeyboardButton("Нет", callback_data='test_no')]
    ]
    return InlineKeyboardMarkup(keyboard)

def consultation_issue_keyboard():
    keyboard = [
        [InlineKeyboardButton("Тревога/страхи", callback_data='issue_anxiety')],
        [InlineKeyboardButton("Депрессия/апатия", callback_data='issue_depression')],
        [InlineKeyboardButton("Прокрастинация", callback_data='issue_procrastination')],
        [InlineKeyboardButton("Другое", callback_data='issue_other')],
        [InlineKeyboardButton("🔔 Уведомлять о новых датах", callback_data='subscribe_dates')],
        [InlineKeyboardButton("🔕 Не уведомлять о датах", callback_data='unsubscribe_dates')]
    ]
    return InlineKeyboardMarkup(keyboard)

def after_test_high_keyboard():
    keyboard = [
        [InlineKeyboardButton("📅 Выбрать время", url=BotURLs.get_website_url_with_referral())],
        [InlineKeyboardButton("💡 Узнать подробности", url=BotURLs.consultation_page())],
        [InlineKeyboardButton("📩 Отправить вопрос", callback_data='ask_question')]
    ]
    return InlineKeyboardMarkup(keyboard)

def anxiety_issue_keyboard():
    keyboard = [
        [InlineKeyboardButton("📅 Записаться на консультацию", url=BotURLs.get_website_url_with_referral())],
        [InlineKeyboardButton("🧪 Самодиагностика", url='https://psytests.org/depr/bai.html')]
    ]
    return InlineKeyboardMarkup(keyboard)

def depression_issue_keyboard():
    keyboard = [
        [InlineKeyboardButton("📅 Записаться на консультацию", url=BotURLs.get_website_url_with_referral())],
        [InlineKeyboardButton("🧪 Самодиагностика", url='https://psytests.org/depr/bdi.html')]
    ]
    return InlineKeyboardMarkup(keyboard)

def procrastination_issue_keyboard():
    keyboard = [
        [InlineKeyboardButton("📅 Записаться на консультацию", url=BotURLs.get_website_url_with_referral())],
        [InlineKeyboardButton("🧪 Шкала тревоги Бека", url='https://psytests.org/depr/bai.html')],
        [InlineKeyboardButton("🧪 Шкала депресии Бека", url='https://psytests.org/depr/bdi.html')]
    ]
    return InlineKeyboardMarkup(keyboard)

def other_issue_keyboard():
    keyboard = [
        [InlineKeyboardButton("Обсудить с психологом", url='https://t.me/sitdipsy')],
        [InlineKeyboardButton("📋 Главное меню", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)


def tests_keyboard():
    """Создает клавиатуру с кнопками для различных тестов"""
    keyboard = [
        [InlineKeyboardButton("🧪 Шкала тревоги Бека (BAI)", callback_data='test_bai')],
        [InlineKeyboardButton("🧪 Шкала депрессии Бека (BDI)", callback_data='test_bdi')],
        [InlineKeyboardButton("📊 Опросник когнитивных ошибок", callback_data='test_cognitive')]
    ]
    return InlineKeyboardMarkup(keyboard)


def test_result_level_keyboard():
    """Клавиатура для выбора уровня тревоги/депрессии после теста"""
    keyboard = [
        [InlineKeyboardButton("🔴 У меня высокий уровень тревоги/депрессии", callback_data='result_high')],
        [InlineKeyboardButton("🟡 У меня средний уровень тревоги/депрессии", callback_data='result_medium')],
        [InlineKeyboardButton("🟢 У меня низкий уровень тревоги/депрессии", callback_data='result_low')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Для среднего уровня результата
def medium_result_keyboard():
    keyboard = [
        [InlineKeyboardButton("📥 Скачать чек-лист", callback_data='get_checklist')],
        [InlineKeyboardButton("📅 Записаться на консультацию", url=BotURLs.get_website_url_with_referral())],
        [InlineKeyboardButton("❔ Как это поможет именно мне", url=BotURLs.work_stages())]
    ]
    return InlineKeyboardMarkup(keyboard)

# Для низкого уровня результата
def low_result_keyboard():
    keyboard = [
        [InlineKeyboardButton("📥 Скачать чек-лист", callback_data='get_checklist')],
        [InlineKeyboardButton("🧠 Получить памятку", callback_data='get_memo')],
        [InlineKeyboardButton("💡 Подписаться на полезные материалы", callback_data='subscribe_materials')]
    ]
    return InlineKeyboardMarkup(keyboard)