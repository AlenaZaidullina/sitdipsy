import pytest
from django.urls import reverse, resolve
from psyproducts_app import views


class TestUrls:
    """Тесты для URL-маршрутов"""

    def test_psyproducts_url(self):
        """Тест URL для страницы продуктов"""
        path = reverse('psyproducts')
        assert path == '/products/'
        assert resolve(path).func == views.psyproducts

    def test_url_resolution(self):
        """Тест разрешения URL"""
        resolver = resolve('/products/')
        assert resolver.func == views.psyproducts
        assert resolver.url_name == 'psyproducts'