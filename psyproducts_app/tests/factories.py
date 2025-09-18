import factory
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from psyproducts_app.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: f'Test Product {n}')
    description = factory.Faker('text', max_nb_chars=200)
    is_free = False
    price = factory.LazyFunction(lambda: Decimal('100.00'))

    # Простое создание файла без сложной логики
    @factory.lazy_attribute
    def document_file(self):
        return SimpleUploadedFile(
            "test_document.pdf",
            b"file_content",
            content_type="application/pdf"
        )

class ProductWithoutFileFactory(factory.django.DjangoModelFactory):
    """Фабрика для продуктов без файла"""
    class Meta:
        model = Product
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: f'Test Product No File {n}')
    description = factory.Faker('text', max_nb_chars=200)
    is_free = True
    price = Decimal('0.00')
    document_file = None  # Явно устанавливаем None