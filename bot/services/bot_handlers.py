from telegram import Update
from telegram.ext import ContextTypes
from ..models import Client, ContentBlock, ConsultationRequest, NewDatesSubscription
from .keyboards import (main_menu_keyboard,
                        test_confirmation_keyboard,
                        consultation_issue_keyboard,
                        get_start_keyboard,
                        get_main_reply_keyboard,
                        anxiety_issue_keyboard,
                        depression_issue_keyboard,
                        procrastination_issue_keyboard,
                        other_issue_keyboard,
                        tests_keyboard,
                        test_result_level_keyboard,
                        medium_result_keyboard,
                        low_result_keyboard)
from asgiref.sync import sync_to_async
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from .urls import BotURLs
import logging
from telegram.error import BadRequest

logger = logging.getLogger(__name__)

async def safe_edit_message(query, text, reply_markup=None, parse_mode=None):
    """Безопасное редактирование сообщения с обработкой ошибок"""
    try:
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except BadRequest as e:
        if "Message is not modified" in str(e):
            # Если сообщение не изменилось - игнорирует ошибку
            await query.answer()
        else:
            # Другие ошибки пробрасываем
            raise


def get_start_keyboard():
    """Создает клавиатурную кнопку для старта"""
    keyboard = [
        [KeyboardButton("🚀 Начать работу")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Создаем или получаем клиента
    client, created = await sync_to_async(Client.objects.get_or_create)(
        telegram_id=user.id,
        defaults={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    )

    welcome_text = (
        "👋 Привет! Я Диана, клинический психолог в когнитивно-поведенческом подходе.\n"
        "Помогаю клиентам снижать тревожность, справляться с прокрастинацией и выходить из состояния «как будто жизнь на паузе» с помощью научно доказанных методов."

    )

    # Отправляется сообщение со start-кнопкой
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_start_keyboard()
    )

    # СРАЗУ отправляется reply-кнопки для навигации
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=get_main_reply_keyboard()
    )


async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатие кнопки 'Начать работу'"""
    user = update.effective_user

    client, created = await sync_to_async(Client.objects.get_or_create)(
        telegram_id=user.id,
        defaults={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    )

    welcome_text = (
        "👋 Отлично! Давайте начнем.\n\n"
        "Я помогаю клиентам снижать тревожность, справляться с прокрастинацией и выходить "
        "из состояния «как будто жизнь на паузе» с помощью научно доказанных методов.\n\n"
        "Выберите, что актуально для вас:"
    )

    # Отправляется сообщение с inline-меню
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu_keyboard()
    )




async def handle_main_reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатие reply-кнопки 'Главное меню'"""
    menu_text = (
        "🏠 Главное меню\n\n"
        "Выберите, что вас интересует:"
    )

    # Отправляет inline-клавиатуру с основным меню
    await update.message.reply_text(
        menu_text,
        reply_markup=main_menu_keyboard()
    )


async def handle_contact_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатие reply-кнопки 'Связаться с психологом'"""
    keyboard = [
        [InlineKeyboardButton("📞 Связаться с психологом", url="https://t.me/sitdipsy")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Щёлкните кнопку, чтобы связаться с психологом.", reply_markup=reply_markup)



async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управляет основным потоком взаимодействия пользователя с главным меню бота"""
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == 'take_test':
        await query.edit_message_text(
            "Тесты займут около 10 минут. Результат поможет вам понять, стоит ли обратить внимание на проблеме. Начать?",
            reply_markup=test_confirmation_keyboard()
        )

    elif choice == 'book_consultation':
        await query.edit_message_text(
            "Чтобы подобрать для вас подходящий формат, ответьте на один вопрос: что вас беспокоит больше всего?",
            reply_markup=consultation_issue_keyboard()
        )


async def handle_main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает возврат в главное меню из callback"""
    query = update.callback_query
    await query.answer()

    menu_text = (
        "🏠 Главное меню\n\n"
        "Выберите, что вас интересует:"
    )

    await query.edit_message_text(
        menu_text,
        reply_markup=main_menu_keyboard()
    )




async def handle_test_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает подтверждение прохождения тестов"""
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == 'test_yes':
        test_text = (
            "Выберите тест для прохождения:\n\n"
            "• 🧪 **Шкала тревоги Бека (BAI)** - оценивает уровень тревожности.\n"
            "• 🧪 **Шкала депрессии Бека (BDI)** - определяет уровень депрессии.\n"
            "• 📊 **Опросник когнитивных ошибок** - выявляет распространенные когнитивные искажения.\n\n"
            "После прохождения теста вы сможете выбрать ваш уровень результата.\n\n"
            "‼️Не забудьте нажать кнопку сохранить бланк, либо отправить ссылку на результаты.\n"
        )

        # Отправляется новое сообщение с сохранением reply-клавиатуры
        await query.message.reply_text(
            test_text,
            reply_markup=tests_keyboard(),
            parse_mode='Markdown'
        )

    elif choice == 'test_no':
        keyboard = [
            [InlineKeyboardButton("Да", callback_data='get_guide')],
            [InlineKeyboardButton("Нет", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляется новое сообщение с сохранением reply-клавиатуры
        await query.message.reply_text(
            "Хотите вместо теста получить мини-гайд по самопомощи?",
            reply_markup=reply_markup
        )


async def handle_consultation_issue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """функция направляет пользователей к необходимым инструментам и услугам в зависимости от специфики заявленной ими проблемы"""
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == 'issue_anxiety':
        await query.edit_message_text(
            "Понимаю, тревога и страхи могут сильно влиять на качество жизни. "
            "Предлагаю два варианта:\n\n"
            "• 🧪 Пройти самодиагностику - короткий тест поможет лучше понять ваше состояние.\n"
            "• 📅 Записаться на консультацию - сразу начать работу с психологом\n\n"
            "‼️Не забудьте нажать кнопку сохранить бланк, либо отправить ссылку на результаты.",
            reply_markup=anxiety_issue_keyboard()
        )

    elif choice == 'issue_depression':
        # Аналогично для депрессии
        await query.edit_message_text(
            "Работа с депрессией и апатией требует особого подхода..."
            "Предлагаю два варианта:\n\n"
            "• 🧪 Пройти самодиагностику - короткий тест поможет лучше понять ваше состояние.\n"
            "• 📅 Записаться на консультацию - сразу начать работу с психологом.\n\n"
            "‼️Не забудьте нажать кнопку сохранить бланк, либо отправить ссылку на результаты.",
            reply_markup=depression_issue_keyboard()
        )

    elif choice == 'issue_procrastination':

        await query.edit_message_text(
            "Знакомо чувство, когда важные дела постоянно откладываются? Это нормально, многие сталкиваются с таким!\n"
        "Давайте вместе разберёмся и найдём решение:\n\n"
        "• ✨ Пройдите самодиагностику - всего пара минут помогут определить степень проблемы и первые шаги.\n"
        "• 🌟 Запишитесь на консультацию - я помогу вам разобраться в причинах и найду оптимальные пути преодоления прокрастинации!\n\n"
            "‼️Не забудьте нажать кнопку сохранить бланк, либо отправить ссылку на результаты.",
            reply_markup=procrastination_issue_keyboard()
        )

    elif choice == 'issue_other':

        await query.edit_message_text(
            "🌤️ Каждого из нас периодически посещают разные трудности и переживания — будь то сложности в отношениях, профессиональные вопросы или личные изменения.\n\n"
    "🌟 Важно помнить, что любая проблема имеет своё решение, и поддержка специалиста может стать ключом к лучшему пониманию себя и ситуации.\n\n"
    "👍 Обсудите свою ситуацию со мной, мы вместе попробуем найти выход и создать комфортное пространство для решения ваших вопросов.\n",
            reply_markup=other_issue_keyboard()
        )



async def handle_anxiety_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """обрабатывает выбор опции "Тревога/страхи" """
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("📅 Выбрать время", url=BotURLs.consultation_page())]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "Отлично! Вы можете выбрать удобное время для консультации по ссылке ниже:\n\n"
        "На первой встрече мы:\n"
        "• Разберем вашу ситуацию\n"
        "• Определим цели работы\n"
        "• Наметим план терапии",
        reply_markup=reply_markup
    )

    # Сохраняем запрос в базу
    user = query.from_user
    client = await sync_to_async(Client.objects.get)(telegram_id=user.id)

    consultation_request = ConsultationRequest(
        client=client,
        primary_issue='Тревога/страхи',
        status='new'
    )
    await sync_to_async(consultation_request.save)()



async def handle_take_test_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатие reply-кнопки 'Пройти тесты'"""
    await update.message.reply_text(
        "Тесты займут около 10 минут. Результат поможет вам понять, стоит ли обратить внимание на проблеме. Начать?\n",
        reply_markup=test_confirmation_keyboard()
    )


async def handle_test_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор конкретного теста"""
    query = update.callback_query
    await query.answer()

    test_name = ""
    if query.data == 'test_bai':
        test_name = "Шкала тревоги Бека (BAI)"
        test_url = "https://psytests.org/depr/bai.html"
    elif query.data == 'test_bdi':
        test_name = "Шкала депрессии Бека (BDI)"
        test_url = "https://psytests.org/depr/bdi.html"
    elif query.data == 'test_cognitive':
        test_name = "Опросник когнитивных ошибок"
        test_url = "https://psytests.org/cbt/cmqm.html"

    # Сохраняем информацию о выбранном тесте в контексте
    context.user_data['selected_test'] = query.data
    context.user_data['test_url'] = test_url
    context.user_data['test_name'] = test_name

    # Отправляем сообщение с инструкцией и кнопкой для перехода к тесту
    keyboard = [
        [InlineKeyboardButton(f"🧪 Пройти тест {test_name}", url=test_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем НОВОЕ сообщение с сохранением reply-клавиатуры
    await query.message.reply_text(
        f"Отлично! Вы выбрали: {test_name}\n\n"
        "Нажмите на кнопку ниже, чтобы перейти к тесту. "
        "После прохождения теста вернитесь в бот и нажмите кнопку 'Я прошел тест' для получения результатов:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    # Добавляем кнопку для подтверждения прохождения теста
    confirm_keyboard = [
        [InlineKeyboardButton("✅ Я прошел тест", callback_data='test_completed')]
    ]
    confirm_reply_markup = InlineKeyboardMarkup(confirm_keyboard)

    # Отправляем с сохранением reply-клавиатуры
    await query.message.reply_text(
        "Нажмите кнопку ниже, когда завершите тест:",
        reply_markup=confirm_reply_markup
    )

async def handle_test_completion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает подтверждение прохождения теста"""
    query = update.callback_query
    await query.answer()

    # Отправляем НОВОЕ сообщение с сохранением reply-клавиатуры
    await query.message.reply_text(
        "Какой у вас получился результат теста?",
        reply_markup=test_result_level_keyboard()
    )


async def handle_test_result_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор уровня результата теста"""
    query = update.callback_query
    await query.answer()

    selected_test = context.user_data.get('selected_test', 'unknown_test')
    result_level = query.data

    # Определяем текст в зависимости от уровня результата
    if result_level == 'result_high':
        message_text = (
            "🔴 Высокий уровень\n\n"
            "По результатам теста ваш уровень тревоги/депрессии повышен — это значит, что вам может быть сложно справляться с ежедневными задачами, "
            "а внутреннее напряжение мешает жить полной жизнью. Но хорошая новость: с этим можно работать.\n\n"
            "🌟Что я предлагаю:\n"
            "Консультация(3500 ₽): разберем вашу ситуацию и дам техники для быстрого облегчения состояния.\n\n"
            "👉Сейчас у меня есть свободные окна на этой неделе — успеете записаться?"
        )
        # Клавиатура для высокого уровня
        keyboard = [
            [InlineKeyboardButton("📅 Выбрать время", url=BotURLs.booking())],
            [InlineKeyboardButton("💬 Отправить вопрос", url="https://t.me/sitdipsy")],
            [InlineKeyboardButton("💡 Сначала узнать подробности", url=BotURLs.consultation_rules())]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    elif result_level == 'result_medium':
        message_text = (
            "🟡 Средний уровень\n\n"
            "Ваши результаты показывают умеренные симптомы – возможно, вы замечаете, что:\n\n"
            f"{chr(8226)} Энергии стало меньше, а усталость появляется быстрее\n"
            f"{chr(8226)} Мысли иногда крутятся вокруг тревожных сценариев\n"
            f"{chr(8226)} То, что раньше приносило радость, сейчас кажется «пресным»\n\n"
            "Это не критично, но важно уделить внимание своему состоянию – чтобы оно не влияло на вашу жизнь.\n\n"
            "Что можно сделать прямо сейчас:\n"
            "1️⃣ Бесплатный вариант:\n"
            f"{chr(8226)} Скачайте 🗂️ «Гайд по самопомощи» с техниками КПТ\n"
            "2️⃣ Максимально эффективно:\n"
            f"{chr(8226)} Консультация (60 минут / 3500 ₽ + индивидуальное сопровождение):\n"
            "   ✨ Разберём вашу ситуацию и подберём стратегии,\n"
            "   которые дадут результат."
        )
        reply_markup = medium_result_keyboard()

    else:  # result_low
        message_text = (
            "🟢 Низкий уровень\n\n"
            "Отличные новости! Я рада, что ваши результаты показывают, что уровень тревоги/депрессии в пределах нормы. Это значит, что:\n\n"
            f"{chr(8226)} Вы достаточно устойчивы к стрессу\n"
            f"{chr(8226)} Эмоциональное состояние в целом стабильно\n"
            f"{chr(8226)} Но иногда могут возникать отдельные сложные моменты\n\n"
            "Чтобы сохранить это состояние, рекомендую:\n"
            "✅ Профилактический чек-лист «5 привычек для психического здоровья»\n"
            "✅ Памятку «Как быстро снять стресс» с техниками КПТ\n\n"
            "💡 Если вдруг заметите ухудшение – возвращайтесь! Работать с симптомами на ранней стадии в 3 раза легче."
        )
        reply_markup = low_result_keyboard()

    # Отправляем НОВОЕ сообщение с сохранением reply-клавиатуры
    await query.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    # Сохраняем информацию о результате в базе данных
    user = query.from_user
    try:
        client = await sync_to_async(Client.objects.get)(telegram_id=user.id)
        # Здесь можно сохранить информацию о пройденном тесте и результате
    except Client.DoesNotExist:
        pass



async def send_content_by_type(update: Update, content_type: str, message_obj=None):
    """Отправляет контент по типу"""
    try:
        logger.info(f"Attempting to send content of type: {content_type}")
        # Получаем message_obj правильно
        if message_obj is None:
            if hasattr(update, 'message') and update.message:
                message_obj = update.message
            elif hasattr(update, 'callback_query') and update.callback_query and hasattr(update.callback_query, 'message'):
                message_obj = update.callback_query.message
            elif hasattr(update, 'effective_message'):
                message_obj = update.effective_message
            else:
                print("Cannot get message object")
                return

        content = await sync_to_async(ContentBlock.objects.get)(
            content_type=content_type,
            is_active=True
        )

        if content.file:
            # Отправляем файл
            file_path = content.file.path
            with open(file_path, 'rb') as file:
                await message_obj.reply_document(document=file, caption=content.name)
        elif content.text:
            await message_obj.reply_text(f"**{content.name}**\n\n{content.text}", parse_mode='Markdown')
        else:
            await message_obj.reply_text("Контент временно недоступен.")

        logger.info(f"Successfully sent content: {content_type}")

    except ContentBlock.DoesNotExist:
        logger.error(f"ContentBlock with type {content_type} does not exist")
        if message_obj:
            await message_obj.reply_text("Контент временно недоступен.")
        print(f"ContentBlock with type {content_type} does not exist")
    except Exception as e:
        logger.error(f"Error sending content {content_type}: {e}")
        if message_obj:
            await message_obj.reply_text("Произошла ошибка при отправке контента.")
        print(f"Error sending content: {e}")


async def handle_guide_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает запрос на получение гида"""
    query = update.callback_query
    if query:
        await query.answer()
        message_obj = query.message
    else:
        message_obj = update.message

    await send_content_by_type(update, 'gift_guide', message_obj)


async def handle_checklist_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает запрос на получение чек-листа"""
    query = update.callback_query
    if query:
        await query.answer()
        message_obj = query.message
    else:
        message_obj = update.message

    await send_content_by_type(update, 'checklist', message_obj)


async def handle_memo_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает запрос на получение памятки"""
    query = update.callback_query
    if query:
        await query.answer()
        message_obj = query.message
    else:
        message_obj = update.message

    await send_content_by_type(update, 'memo', message_obj)


async def handle_about_method_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает запрос информации о методе"""
    if hasattr(update, 'callback_query'):
        await update.callback_query.answer()

    # Получаем message_obj правильно (как в handle_guide_request)
    if hasattr(update, 'message'):
        message_obj = update.message
    elif hasattr(update, 'callback_query') and hasattr(update.callback_query, 'message'):
        message_obj = update.callback_query.message
    else:
        message_obj = update.effective_message if hasattr(update, 'effective_message') else None

    if message_obj:
        await send_content_by_type(update, 'about_method', message_obj)


async def handle_about_consultation_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает запрос информации о консультациях"""
    if hasattr(update, 'callback_query'):
        await update.callback_query.answer()

    # Получаем message_obj правильно (как в handle_guide_request)
    if hasattr(update, 'message'):
        message_obj = update.message
    elif hasattr(update, 'callback_query') and hasattr(update.callback_query, 'message'):
        message_obj = update.callback_query.message
    else:
        message_obj = update.effective_message if hasattr(update, 'effective_message') else None

    if message_obj:
        await send_content_by_type(update, 'about_consultation', message_obj)


async def handle_subscribe_materials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        user = query.from_user
        # ИСПРАВЛЕНО: используем get_or_create вместо get
        client, created = await sync_to_async(Client.objects.get_or_create)(
            telegram_id=user.id,
            defaults={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
        client.subscribed_to_newsletter = True
        await sync_to_async(client.save)()

        success_text = "✅ Вы успешно подписались на полезные материалы!"
        await query.edit_message_text(
            text=success_text,
            reply_markup=main_menu_keyboard()
        )
    except BadRequest as e:
        if "Message is not modified" in str(e):
            pass
        else:
            print(f"Error in handle_subscribe_materials: {e}")
    except Exception as e:
        print(f"Error in handle_subscribe_materials: {e}")


async def handle_unsubscribe_materials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        user = query.from_user
        client, created = await sync_to_async(Client.objects.get_or_create)(
            telegram_id=user.id,
            defaults={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
        client.subscribed_to_newsletter = False
        await sync_to_async(client.save)()

        success_text = "✅ Вы отписались от рассылки полезных материалов."
        await query.edit_message_text(
            text=success_text,
            reply_markup=main_menu_keyboard()
        )
    except BadRequest as e:
        if "Message is not modified" in str(e):
            pass
        else:
            print(f"Error in handle_unsubscribe_materials: {e}")
    except Exception as e:
        print(f"Error in handle_unsubscribe_materials: {e}")

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает команду /unsubscribe из текстового сообщения"""
    user = update.effective_user

    try:
        client = await sync_to_async(Client.objects.get)(telegram_id=user.id)

        if not client.subscribed_to_newsletter:
            await update.message.reply_text("ℹ️ Вы и так не подписаны на рассылку полезных материалов.")
            return

        client.subscribed_to_newsletter = False
        await sync_to_async(client.save)()

        await update.message.reply_text(
            "🔕 Вы отписались от рассылки полезных материалов.\n\n"
            "Больше не будете получать:\n"
            "• Статьи по психологии\n"
            "• Практические упражнения\n"
            "• Советы по саморазвитию\n"
            "• Информацию о новых методиках\n\n"
            "Если передумаете - всегда можно подписаться снова через главное меню!"
        )

    except Client.DoesNotExist:
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")


async def handle_subscribe_dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает подписку на уведомления о новых датах"""
    query = update.callback_query
    await query.answer()

    user = query.from_user

    try:
        client = await sync_to_async(Client.objects.get)(telegram_id=user.id)

        # Создаем или обновляем подписку
        subscription, created = await sync_to_async(NewDatesSubscription.objects.get_or_create)(
            client=client,
            defaults={'is_active': True}
        )

        if not created:
            subscription.is_active = True
            await sync_to_async(subscription.save)()

        success_text = (
            "✅ Вы подписались на уведомления о новых датах консультаций!\n\n"
            "Теперь вы будете получать сообщения, когда появятся новые свободные окошки для записи."
        )

        await safe_edit_message(
            query,
            success_text,
            reply_markup=consultation_issue_keyboard()
        )

    except Client.DoesNotExist:
        error_text = "Произошла ошибка. Попробуйте позже."
        await safe_edit_message(
            query,
            error_text,
            reply_markup=consultation_issue_keyboard()
        )


async def handle_unsubscribe_dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает отписку от уведомлений о новых датах"""
    query = update.callback_query
    await query.answer()

    user = query.from_user

    try:
        client = await sync_to_async(Client.objects.get)(telegram_id=user.id)

        try:
            subscription = await sync_to_async(NewDatesSubscription.objects.get)(client=client)
            subscription.is_active = False
            await sync_to_async(subscription.save)()

            success_text = (
                "🔕 Вы отписались от уведомлений о новых датах.\n\n"
                "Больше не будете получать сообщения о новых свободных окошках для консультаций."
            )

            await safe_edit_message(
                query,
                success_text,
                reply_markup=consultation_issue_keyboard()
            )

        except NewDatesSubscription.DoesNotExist:
            await query.answer("Вы и так не подписаны на уведомления о датах.")
            # ВСЕГДА обновляем сообщение
            await safe_edit_message(
                query,
                "ℹ️ Вы и так не подписаны на уведомления о датах.",
                reply_markup=consultation_issue_keyboard()
            )

    except Client.DoesNotExist:
        error_text = "Произошла ошибка. Попробуйте позже."
        await safe_edit_message(
            query,
            error_text,
            reply_markup=consultation_issue_keyboard()
        )