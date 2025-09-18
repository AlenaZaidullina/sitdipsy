from django.db import models

class MainAppIndex(models.Model):
    name = models.CharField('имя', max_length=100)

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'

    def __str__(self):
        return self.name

class Education(models.Model):
    year = models.CharField(max_length=50, verbose_name="Год/Период")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Год обучения"
        verbose_name_plural = "Годы обучения"
        ordering = ['order']

    def __str__(self):
        return f"{self.year}"

class EducationAchievement(models.Model):
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255, verbose_name='Название достижения')
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        verbose_name = "Достижение/Сертификат"
        verbose_name_plural = "Достижения/Сертификаты"
        ordering = ['order']

    def __str__(self):
        return self.title

class DiplomaImage(models.Model):
    achievement = models.ForeignKey(EducationAchievement, on_delete=models.CASCADE, related_name='diploma_images')
    image = models.ImageField(upload_to='diplomas/', verbose_name='Изображение диплома')
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Изображение диплома"
        verbose_name_plural = "Изображения дипломов"
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['achievement', 'order'],
                name='unique_diploma_image_order'
            )
        ]

    def __str__(self):
        return f"Изображение {self.order} для {self.achievement.title}"

class ServiceQuery(models.Model):
    title = models.CharField('Название запроса', max_length=100)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Запрос для работы"
        verbose_name_plural = "Запросы для работы"
        ordering = ['order']

    def __str__(self):
        return self.title

class ExcludeService(models.Model):
    title = models.CharField('Название направления', max_length=100)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField(verbose_name='Активно', default=True)
    order = models.PositiveIntegerField(verbose_name='Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Исключенное направление'
        verbose_name_plural = 'Исключенные направления'
        ordering = ['order']

    def __str__(self):
        return self.title