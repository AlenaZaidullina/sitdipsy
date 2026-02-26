from django.db import models


class Appointment(models.Model):
    CONSULTATION_TYPES = [
        ('first', 'Первичная консультация (90 мин)'),
        ('follow', 'Повторная консультация (60 мин)'),
    ]

    full_name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=20)
    consultation_type = models.CharField('Тип консультации', max_length=10, choices=CONSULTATION_TYPES)
    date = models.DateField('Дата консультации')
    time = models.TimeField('Время консультации')
    created_at = models.DateTimeField('Дата создания записи', auto_now_add=True)
    is_paid = models.BooleanField('Оплачено', default=False)
    is_confirmed = models.BooleanField('Подтверждено', default=False)
    notes = models.TextField('Заметки', blank=True)
    pd_consent = models.BooleanField('Согласие на обработку ПД получено', default=False)


    class Meta:
        verbose_name = 'Запись на консультацию'
        verbose_name_plural = 'Записи на консультации'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.full_name} - {self.date} {self.time}"


class AvailableDate(models.Model):
    date = models.DateField('Доступная дата', unique=True)
    is_available = models.BooleanField('Доступна', default=True)

    class Meta:
        verbose_name = 'Доступная дата'
        verbose_name_plural = 'Доступные даты'
        ordering = ['date']

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')

class AvailableTime(models.Model):
    date = models.ForeignKey(AvailableDate, on_delete=models.CASCADE, related_name='available_times')
    time = models.TimeField('Доступное время')
    is_booked = models.BooleanField('Забронировано', default=False)
    booked_at = models.DateTimeField('Когда забронировано', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    #  вложенный класс - класс внутри класса
    class Meta:
        verbose_name = 'Доступное время'
        verbose_name_plural = 'Доступное время'
        ordering = ['date', 'time']
        unique_together = ('date', 'time')

    def __str__(self):
        return f"{self.date} - {self.time.strftime('%H:%M')}"

class TelegramNotification(models.Model):
    chat_id = models.CharField('Chat ID', max_length=50)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Telegram уведомление'
        verbose_name_plural = 'Telegram уведомления'

    def __str__(self):
        return self.chat_id

class NewDatesSubscriber(models.Model):
    chat_id = models.CharField('Chat ID', max_length=50, unique=True)
    subscribed_at = models.DateTimeField('Дата подписки', auto_now_add=True)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Подписчик на новые даты'
        verbose_name_plural = 'Подписчики на новые даты'

    def __str__(self):
        return f"{self.chat_id} (активна: {'да' if self.is_active else 'нет'})"




class Consent(models.Model):
    full_name = models.CharField('ФИО', max_length=255)
    ip_address = models.GenericIPAddressField('IP адрес', protocol='both')
    user_agent = models.TextField('User Agent', blank=True)
    created_at = models.DateTimeField('Дата подписания', auto_now_add=True)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Согласие на обработку ПДн'
        verbose_name_plural = 'Согласия на обработку ПДн'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"