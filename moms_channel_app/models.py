from django.db import models

class Testimonial(models.Model):
    image = models.ImageField(upload_to='testimonials/', verbose_name='Изображение отзыва')
    alt_text = models.CharField(max_length=255, verbose_name='Альтернативный текст', blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"Отзыв #{self.id} - {self.created_at.strftime('%d.%m.%Y')}"

