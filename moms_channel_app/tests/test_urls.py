import pytest
from django.urls import reverse, resolve
from moms_channel_app import views

pytestmark = pytest.mark.django_db


class TestUrls:
    def test_moms_channel_url(self):
        """Тест URL для страницы канала мам"""
        path = reverse('moms_channel')

        assert path == '/channel/'
        assert resolve(path).func == views.moms_channel

    def test_moms_channel_url_resolution(self):
        """Тест разрешения URL"""
        resolver = resolve('/channel/')

        assert resolver.func == views.moms_channel
        assert resolver.url_name == 'moms_channel'