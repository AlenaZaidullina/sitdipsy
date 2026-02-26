import pytest
from django.urls import reverse, resolve
from main_app import views


@pytest.mark.django_db
class TestUrls:
    """Тесты для URL-маршрутов"""

    def test_index_url(self):
        """Тест URL для главной страницы"""
        path = reverse('index')
        assert path == '/'
        assert resolve(path).func == views.index

    def test_index_url_resolution(self):
        """Тест разрешения URL"""
        resolver = resolve('/')
        assert resolver.func == views.index
        assert resolver.url_name == 'index'

    def test_url_patterns(self):
        """Тест всех URL паттернов"""
        from main_app import urls

        # Проверяет, что есть только один URL паттерн
        assert len(urls.urlpatterns) == 1

        # Проверяет конкретный паттерн
        pattern = urls.urlpatterns[0]
        assert pattern.pattern._route == ''
        assert pattern.name == 'index'
        assert pattern.callback == views.index