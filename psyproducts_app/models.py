from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание", blank=True)
    is_free = models.BooleanField(default=False, verbose_name="Бесплатный продукт")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Цена",
        help_text="Для бесплатных продуктов оставить 0"
    )
    document_file = models.FileField(
        upload_to='products/documents/',
        null=True,
        blank=True,
        verbose_name="Файл методички"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']
