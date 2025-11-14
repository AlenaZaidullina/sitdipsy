import pytest
from datetime import date, time, timedelta
from appointment_app.models import Appointment, AvailableDate, AvailableTime, Consent, TelegramNotification


@pytest.mark.django_db
class TestAppointmentModel:
    def test_create_appointment(self):
        """Тест создания записи на консультацию"""
        appointment = Appointment.objects.create(
            full_name="Иванов Иван Иванович",
            phone="+79161234567",
            consultation_type="first",
            date=date.today() + timedelta(days=1),
            time=time(10, 0),
            pd_consent=True
        )

        assert appointment.full_name == "Иванов Иван Иванович"
        assert appointment.phone == "+79161234567"
        assert appointment.consultation_type == "first"
        assert appointment.pd_consent is True
        assert str(appointment) == f"{appointment.full_name} - {appointment.date} {appointment.time}"

    def test_appointment_str_representation(self):
        """Тест строкового представления записи"""
        appointment = Appointment.objects.create(
            full_name="Петров Петр",
            phone="+79161234568",
            consultation_type="follow",
            date=date(2024, 1, 15),
            time=time(14, 30),
            pd_consent=True
        )

        expected_str = "Петров Петр - 2024-01-15 14:30:00"
        assert str(appointment) == expected_str


@pytest.mark.django_db
class TestAvailableDateModel:
    def test_create_available_date(self):
        """Тест создания доступной даты"""
        available_date = AvailableDate.objects.create(
            date=date.today() + timedelta(days=2),
            is_available=True
        )

        assert available_date.is_available is True
        assert available_date.date > date.today()

    def test_available_date_str_representation(self):
        """Тест строкового представления даты"""
        test_date = date(2024, 12, 25)
        available_date = AvailableDate.objects.create(
            date=test_date,
            is_available=True
        )

        assert str(available_date) == "25.12.2024"


@pytest.mark.django_db
class TestAvailableTimeModel:
    def test_create_available_time(self, available_date):
        """Тест создания доступного времени"""
        available_time = AvailableTime.objects.create(
            date=available_date,
            time=time(9, 0),
            is_booked=False
        )

        assert available_time.time == time(9, 0)
        assert available_time.is_booked is False


@pytest.mark.django_db
class TestConsentModel:
    def test_create_consent(self):
        """Тест создания согласия"""
        consent = Consent.objects.create(
            full_name="Сидорова Мария",
            ip_address="192.168.1.1",
            user_agent="Test User Agent",
            is_active=True
        )

        assert consent.full_name == "Сидорова Мария"
        assert consent.ip_address == "192.168.1.1"
        assert consent.is_active is True
        assert "Сидорова Мария" in str(consent)


@pytest.mark.django_db
class TestTelegramNotificationModel:
    def test_create_telegram_notification(self):
        """Тест создания телеграм уведомления"""
        notification = TelegramNotification.objects.create(
            chat_id="123456789",
            is_active=True
        )

        assert notification.chat_id == "123456789"
        assert notification.is_active is True
        assert str(notification) == "123456789"


# Фикстуры для тестов
@pytest.fixture
def available_date():
    return AvailableDate.objects.create(
        date=date.today() + timedelta(days=1),
        is_available=True
    )


@pytest.fixture
def appointment():
    return Appointment.objects.create(
        full_name="Тестовый Клиент",
        phone="+79161234567",
        consultation_type="first",
        date=date.today() + timedelta(days=3),
        time=time(11, 0),
        pd_consent=True
    )