import pytest
from django.contrib.admin.sites import site
from psyproducts_app.models import Product
from psyproducts_app.admin import ProductAdmin


@pytest.mark.django_db
class TestProductAdmin:
    """Тесты для админки продуктов"""

    def test_admin_list_display(self):
        """Тест отображаемых полей в админке"""
        admin = ProductAdmin(Product, site)
        expected_list_display = ('name', 'is_free', 'price', 'created_at')
        assert admin.list_display == expected_list_display

    def test_admin_list_filter(self):
        """Тест фильтров в админке"""
        admin = ProductAdmin(Product, site)
        expected_list_filter = ('is_free',)
        assert admin.list_filter == expected_list_filter

    def test_admin_search_fields(self):
        """Тест полей поиска"""
        admin = ProductAdmin(Product, site)
        expected_search_fields = ('name', 'description')
        assert admin.search_fields == expected_search_fields

    def test_admin_fields(self):
        """Тест полей формы"""
        admin = ProductAdmin(Product, site)
        expected_fields = ('name', 'description', 'is_free', 'price', 'document_file')
        assert admin.fields == expected_fields

    def test_admin_model_registered(self):
        """Тест что модель зарегистрирована в админке"""
        assert Product in site._registry