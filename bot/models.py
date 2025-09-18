from django.db import models


class Client(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name="ID пользователя Telegram")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата первого взаимодействия")
    subscribed_to_newsletter = models.BooleanField(default=False, verbose_name="Подписан на рассылку")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.first_name} ({self.telegram_id})" if self.first_name else f"Клиент {self.telegram_id}"


class ContentBlock(models.Model):
    CONTENT_TYPES = (
        ('gift_guide', 'Бесплатный гайд (лид-магнит)'),
        ('checklist', 'Чек-лист'),
        ('memo', 'Памятка'),
        ('about_method', 'О методе КПТ'),
        ('about_consultation', 'О консультациях'),
    )
    name = models.CharField(max_length=255, verbose_name="Название материала")
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, verbose_name="Тип контента")
    description = models.TextField(verbose_name="Описание (для админки)")
    file = models.FileField(upload_to='content/%Y/%m/%d/', blank=True, null=True, verbose_name="Файл")
    text = models.TextField(blank=True, null=True, verbose_name="Текст контента")
    telegram_command_trigger = models.CharField(max_length=50, blank=True, null=True,
                                                verbose_name="Команда в боте для вызова")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Блок контента"
        verbose_name_plural = "Блоки контента"

    def __str__(self):
        return f"{self.get_content_type_display()}: {self.name}"


class NewsletterMaterial(models.Model):
    MATERIAL_TYPES = (
        ('article', 'Статья'),
        ('tip', 'Совет'),
        ('exercise', 'Упражнение'),
        ('video', 'Видео'),
        ('audio', 'Аудио'),
        )

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content_type = models.CharField(max_length=20, choices=MATERIAL_TYPES, verbose_name="Тип материала")
    content = models.FileField(upload_to='newsletter/%Y/%m/%d/', blank=True, null=True, verbose_name="Файл")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Материал рассылки"
        verbose_name_plural = "Материалы рассылки"

    def __str__(self):
        return f"{self.get_content_type_display()}: {self.title}"




class ConsultationRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('contacted', 'Связались'),
        ('completed', "Консультация состоялась"),
        ('cancelled', 'Отменена'),
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='consultation_requests',
                               verbose_name="Клиент")
    primary_issue = models.CharField(max_length=255, blank=True, null=True, verbose_name="Основная проблема")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус заявки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Запрос на консультацию"
        verbose_name_plural = "Запросы на консультацию"

    def __str__(self):
        return f"Запрос от {self.client} ({self.status})"



class NewDatesSubscription(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='dates_subscription')
    is_active = models.BooleanField(default=True, verbose_name="Подписка активна")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Подписка на новые даты"
        verbose_name_plural = "Подписки на новые даты"

    def __str__(self):
        return f"Подписка {self.client} ({'активна' if self.is_active else 'неактивна'})"