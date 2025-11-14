import pytest
from django.urls import reverse
from main_app.models import Education, ServiceQuery, ExcludeService
from .factories import EducationFactory, EducationAchievementFactory, ServiceQueryFactory, ExcludeServiceFactory


@pytest.mark.django_db
class TestIndexView:
    """Тесты для представления index"""

    def test_index_view_status_code(self, client):
        """Тест статус кода главной страницы"""
        response = client.get(reverse('index'))
        assert response.status_code == 200

    def test_index_view_template(self, client):
        """Тест используемого шаблона"""
        response = client.get(reverse('index'))
        assert 'main_app/index.html' in [t.name for t in response.templates]

    def test_index_view_context_data(self, client):
        """Тест контекстных данных"""
        # Создаем тестовые данные
        education = EducationFactory(is_active=True)
        achievement = EducationAchievementFactory(education=education, is_active=True)
        service_query = ServiceQueryFactory(is_active=True)
        exclude_service = ExcludeServiceFactory(is_active=True)

        response = client.get(reverse('index'))

        # Проверяем наличие контекстных переменных
        assert 'education_items' in response.context
        assert 'service_queries' in response.context
        assert 'exclude_service' in response.context

        # Проверяем данные в контексте
        education_items = list(response.context['education_items'])
        service_queries = list(response.context['service_queries'])
        exclude_services = list(response.context['exclude_service'])

        assert len(education_items) == 1
        assert len(service_queries) == 1
        assert len(exclude_services) == 1

    def test_index_view_only_active_items(self, client):
        """Тест что отображаются только активные элементы"""
        # Создаем активные и неактивные элементы
        EducationFactory(is_active=True)
        EducationFactory(is_active=False)

        ServiceQueryFactory(is_active=True)
        ServiceQueryFactory(is_active=False)

        ExcludeServiceFactory(is_active=True)
        ExcludeServiceFactory(is_active=False)

        response = client.get(reverse('index'))

        # Проверяем что только активные элементы в контексте
        assert response.context['education_items'].count() == 1
        assert response.context['service_queries'].count() == 1
        assert response.context['exclude_service'].count() == 1

    def test_index_view_ordering(self, client):
        """Тест порядка отображения"""
        # Создаем элементы в разном порядке
        EducationFactory(order=3, is_active=True)
        EducationFactory(order=1, is_active=True)
        EducationFactory(order=2, is_active=True)

        response = client.get(reverse('index'))
        education_items = list(response.context['education_items'])

        # Проверяем порядок (по возрастанию order)
        assert education_items[0].order == 1
        assert education_items[1].order == 2
        assert education_items[2].order == 3

    def test_index_view_empty_data(self, client):
        """Тест с пустыми данными"""
        # Убедимся что нет данных
        Education.objects.all().delete()
        ServiceQuery.objects.all().delete()
        ExcludeService.objects.all().delete()

        response = client.get(reverse('index'))

        # Проверяем что контекстные переменные существуют но пустые
        assert response.context['education_items'].count() == 0
        assert response.context['service_queries'].count() == 0
        assert response.context['exclude_service'].count() == 0
        assert response.status_code == 200

    def test_index_view_achievements_ordering(self, client):
        """Тест порядка достижений внутри образования"""
        education = EducationFactory(is_active=True)
        EducationAchievementFactory(education=education, order=3, is_active=True)
        EducationAchievementFactory(education=education, order=1, is_active=True)
        EducationAchievementFactory(education=education, order=2, is_active=True)

        response = client.get(reverse('index'))
        education_item = response.context['education_items'].first()
        achievements = list(education_item.achievements.all())

        # Проверяем порядок достижений
        assert achievements[0].order == 1
        assert achievements[1].order == 2
        assert achievements[2].order == 3