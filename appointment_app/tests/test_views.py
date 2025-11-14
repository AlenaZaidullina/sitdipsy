import pytest
import json
from django.urls import reverse
from django.utils import timezone
from datetime import date, time, timedelta
from appointment_app.models import Appointment, AvailableDate, AvailableTime, Consent


@pytest.mark.django_db
class TestAppointmentViews:
    def test_appointment_view_get(self, client_with_consent):
        """Тест GET запроса к странице записи"""
        response = client_with_consent.get(reverse('appointment'))
        assert response.status_code == 200
        assert 'Запись на консультацию' in response.content.decode()

    def test_available_dates_api(self, client, available_date_with_time):
        """Тест API доступных дат"""
        response = client.get(reverse('available_dates'))
        data = response.json()

        assert response.status_code == 200
        assert data['status'] == 'success'
        assert len(data['available_dates']) >= 1

    def test_available_times_api(self, client, available_date_with_time):
        """Тест API доступного времени"""
        date_str = available_date_with_time.date.strftime('%Y-%m-%d')
        response = client.get(reverse('available_times', args=[date_str]))
        data = response.json()

        assert response.status_code == 200
        assert data['status'] == 'success'
        assert '10:00' in data['available_times']

    def test_consent_form_get(self, client):
        """Тест GET запроса к форме согласия"""
        response = client.get(reverse('consent_form'))
        assert response.status_code == 200
        assert 'Согласие на обработку персональных данных' in response.content.decode()

    def test_consent_form_post_valid(self, client):
        """Тест POST запроса к форме согласия с валидными данными"""
        data = {
            'full_name': 'Иванов Иван Иванович'
        }

        response = client.post(reverse('consent_form'), data)
        assert response.status_code == 302  # Redirect
        assert Consent.objects.count() == 1
        assert Consent.objects.first().full_name == 'Иванов Иван Иванович'

    def test_consent_form_post_invalid(self, client):
        """Тест POST запроса к форме согласия с невалидными данными"""
        data = {
            'full_name': ''  # Пустое имя
        }

        response = client.post(reverse('consent_form'), data)
        assert response.status_code == 200
        assert 'Пожалуйста, введите ваше ФИО' in response.content.decode()
        assert Consent.objects.count() == 0

    def test_privacy_policy_view(self, client):
        """Тест страницы политики конфиденциальности"""
        response = client.get(reverse('privacy_policy'))
        assert response.status_code == 200
        assert 'ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ' in response.content.decode()


@pytest.mark.django_db
class TestAppointmentBooking:
    def test_appointment_booking_with_consent(self, client_with_consent):
        """Тест бронирования с согласием"""
        # Используем конкретную будущую дату
        test_date = date(2025, 1, 5)  # 5 января 2025 года

        available_date = AvailableDate.objects.create(
            date=test_date,
            is_available=True
        )
        available_time = AvailableTime.objects.create(
            date=available_date,
            time=time(14, 0),
            is_booked=False
        )

        # Получаем CSRF токен
        client_with_consent.get(reverse('appointment'))
        csrf_token = client_with_consent.cookies['csrftoken'].value

        # Данные для бронирования
        booking_data = {
            'full_name': 'Иванов Иван',
            'phone': '+79161234567',
            'consultation_type': 'first',
            'selected_date': '5 января, 14:00',
            'pd_consent': True
        }

        response = client_with_consent.post(
            reverse('appointment'),
            json.dumps(booking_data),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token
        )

        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        print(f"Test date: {test_date}")
        print(f"AvailableDate exists: {AvailableDate.objects.filter(date=test_date).exists()}")

        data = response.json()
        assert response.status_code == 200
        assert data['status'] == 'success'
        assert Appointment.objects.count() == 1

        available_time.refresh_from_db()
        assert available_time.is_booked is True


    def test_appointment_booking_without_consent(self, client):
        """Тест бронирования без согласия"""
        # Очистка сессии
        session = client.session
        session.flush()
        session.save()

        response = client.get(reverse('appointment'))
        # Должен быть редирект на форму согласия
        assert response.status_code == 302
        assert 'consent-form' in response.url


# Обновленные фикстуры
@pytest.fixture
def available_date_with_time():
    date_obj = AvailableDate.objects.create(
        date=date.today() + timedelta(days=2),
        is_available=True
    )
    AvailableTime.objects.create(
        date=date_obj,
        time=time(10, 0),
        is_booked=False
    )
    return date_obj

@pytest.fixture
def client_with_consent(client):
    """Клиент с установленным согласием"""
    session = client.session
    session['pd_consent_given'] = True
    session['pd_consent_name'] = 'Test User'
    session['pd_consent_time'] = timezone.now().isoformat()
    session.save()
    return client