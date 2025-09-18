import pytest
import tempfile
import os
from django.conf import settings
from django.test import override_settings
from datetime import timezone


# Создается временная папка для медиафайлов тестов
@pytest.fixture(scope='session')
def temp_media_root():
    with tempfile.TemporaryDirectory() as temp_dir:
        with override_settings(MEDIA_ROOT=temp_dir):
            yield temp_dir

# Фикстура для клиента
@pytest.fixture
def client():
    from django.test import Client
    return Client()

# Фикстура для пользователя
@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

# Фикстура для superuser
@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        username='admin',
        password='adminpass123',
        email='admin@example.com'
    )


@pytest.fixture
def client_with_consent(client):
    """Клиент с установленным согласием"""
    session = client.session
    session['pd_consent_given'] = True
    session['pd_consent_name'] = 'Test User'
    session['pd_consent_time'] = timezone.now().isoformat()
    session.save()
    return client