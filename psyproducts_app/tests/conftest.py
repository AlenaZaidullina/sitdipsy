import pytest
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from psyproducts_app.models import Product


@pytest.fixture
def free_product():
    """Фикстура для бесплатного продукта"""
    return Product.objects.create(
        name="Free Test Product",
        description="Free product description",
        is_free=True,
        price=Decimal('0.00'),  # Исправлено на Decimal
        document_file=SimpleUploadedFile(
            "free_test.pdf", b"free content", content_type="application/pdf"
        )
    )


@pytest.fixture
def paid_product():
    """Фикстура для платного продукта"""
    return Product.objects.create(
        name="Paid Test Product",
        description="Paid product description",
        is_free=False,
        price=Decimal('100.50'),  # Исправлено на Decimal
        document_file=SimpleUploadedFile(
            "paid_test.pdf", b"paid content", content_type="application/pdf"
        )
    )


@pytest.fixture
def product_without_file():
    """Фикстура для продукта без файла"""
    return Product.objects.create(
        name="No File Product",
        description="Product without file",
        is_free=True,
        price=Decimal('0.00'),  # Исправлено на Decimal
        document_file=None
    )