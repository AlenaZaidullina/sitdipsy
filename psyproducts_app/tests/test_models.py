from decimal import Decimal
from psyproducts_app.models import Product
from .factories import ProductFactory


class TestProductModel:
    """Тесты для модели Product"""

    def test_create_product(self, db):
        """Тест создания продукта"""
        product = ProductFactory()
        assert product.pk is not None
        assert product.name.startswith('Test Product')
        assert isinstance(product.price, Decimal)

    def test_product_str_representation(self, db):
        """Тест строкового представления продукта"""
        product = ProductFactory(name="Test Product")
        assert str(product) == "Test Product"

    def test_free_product_validation(self, db):
        """Тест валидации бесплатного продукта"""
        product = ProductFactory(is_free=True, price=Decimal('0.00'))
        assert product.is_free is True
        assert product.price == Decimal('0.00')

    def test_paid_product_validation(self, db):
        """Тест валидации платного продукта"""
        product = ProductFactory(is_free=False, price=Decimal('100.50'))
        assert product.is_free is False
        assert product.price == Decimal('100.50')

    def test_product_ordering(self, db):
        """Тест порядка сортировки продуктов"""
        product1 = ProductFactory()
        product2 = ProductFactory()

        products = Product.objects.all()
        # Проверяется что сортировка по убыванию created_at
        assert products[0].created_at >= products[1].created_at


    def test_product_with_file(self, db):
        """Тест продукта с файлом"""
        # Создается продукт с файлом напрямую
        from django.core.files.uploadedfile import SimpleUploadedFile

        product = Product.objects.create(
            name="Product With File",
            description="With file here",
            is_free=True,
            price=Decimal('0.00'),
            document_file=SimpleUploadedFile(
                "test_file.pdf", b"content", content_type="application/pdf"
            )
        )
        assert product.document_file  # True если файл есть
        assert product.document_file.name.startswith('products/documents/')

    def test_product_meta_options(self, db):
        """Тест мета-опций модели"""
        assert Product._meta.verbose_name == "Продукт"
        assert Product._meta.verbose_name_plural == "Продукты"
        assert Product._meta.ordering == ['-created_at']

    def test_product_field_characteristics(self, db):
        """Тест характеристик полей модели"""
        product = ProductFactory()

        # Проверка максимальной длины
        assert product._meta.get_field('name').max_length == 200

        # Проверка verbose names
        assert product._meta.get_field('name').verbose_name == "Название продукта"
        assert product._meta.get_field('description').verbose_name == "Описание"
        assert product._meta.get_field('is_free').verbose_name == "Бесплатный продукт"
        assert product._meta.get_field('price').verbose_name == "Цена"
        assert product._meta.get_field('document_file').verbose_name == "Файл методички"

        # Проверка Decimal характеристики
        assert product._meta.get_field('price').max_digits == 10
        assert product._meta.get_field('price').decimal_places == 2