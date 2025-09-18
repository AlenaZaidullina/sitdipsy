import pytest
from decimal import Decimal
from django.urls import reverse
from psyproducts_app.models import Product
from .factories import ProductFactory, ProductWithoutFileFactory

@pytest.mark.django_db
class TestPsyproductsView:
    """Тесты для представления psyproducts"""

    def test_view_url_accessible(self, client):
        """Тест доступности URL"""
        response = client.get(reverse('psyproducts'))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        """Тест использования правильного шаблона"""
        response = client.get(reverse('psyproducts'))
        template_names = [t.name for t in response.templates]
        assert 'psyproducts_app/psyproducts.html' in template_names

    def test_view_context_data(self, client, free_product, paid_product):
        """Тест контекстных данных представления"""
        response = client.get(reverse('psyproducts'))

        assert 'free_products' in response.context
        assert 'paid_products' in response.context

        # Проверяем, что продукты правильно разделены
        free_products = list(response.context['free_products'])
        paid_products = list(response.context['paid_products'])

        assert free_product in free_products
        assert paid_product in paid_products
        assert free_product not in paid_products
        assert paid_product not in free_products

    def test_view_ordering(self, client):
        """Тест порядка отображения продуктов"""
        # Создаем продукты
        product1 = ProductFactory()
        product2 = ProductFactory()

        response = client.get(reverse('psyproducts'))
        all_products = list(response.context['free_products']) + list(response.context['paid_products'])

        # Должно быть хотя бы 2 продукта
        assert len(all_products) >= 2

    def test_empty_products(self, client):
        """Тест отображения при отсутствии продуктов"""
        # Удаляем все продукты
        Product.objects.all().delete()

        response = client.get(reverse('psyproducts'))
        free_products = response.context['free_products']
        paid_products = response.context['paid_products']

        assert len(free_products) == 0
        assert len(paid_products) == 0

    def test_view_with_mixed_products(self, client):
        """Тест со смешанными типами продуктов"""
        # Создаем продукты разных типов с Decimal ценами
        free1 = ProductFactory(is_free=True, price=Decimal('0.00'))
        free2 = ProductWithoutFileFactory()  # Бесплатный без файла
        paid1 = ProductFactory(is_free=False, price=Decimal('100.00'))
        paid2 = ProductFactory(is_free=False, price=Decimal('200.00'))

        response = client.get(reverse('psyproducts'))
        free_products = list(response.context['free_products'])
        paid_products = list(response.context['paid_products'])

        # Должно быть хотя бы по 2 продукта каждого типа
        assert len(free_products) >= 2
        assert len(paid_products) >= 2

    def test_product_count_in_template(self, client, free_product, paid_product):
        """Тест что правильное количество продуктов отображается"""
        response = client.get(reverse('psyproducts'))

        # Проверяем что контекст содержит правильное количество
        assert response.context['free_products'].count() >= 1
        assert response.context['paid_products'].count() >= 1