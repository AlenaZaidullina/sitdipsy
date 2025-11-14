import pytest
from main_app.models import Education, EducationAchievement, ServiceQuery, ExcludeService


@pytest.fixture
def education_data():
    return {
        'year': '2023',
        'is_active': True,
        'order': 1
    }


@pytest.fixture
def create_education(education_data):
    def _create_education(**kwargs):
        data = education_data.copy()
        data.update(kwargs)
        return Education.objects.create(**data)
    return _create_education


@pytest.fixture
def create_education_with_achievements(create_education):
    def _create_education_with_achievements(achievements_count=2, **kwargs):
        education = create_education(**kwargs)
        for i in range(achievements_count):
            EducationAchievement.objects.create(
                education=education,
                title=f'Achievement {i+1}',
                description=f'Description {i+1}',
                is_active=True,
                order=i+1
            )
        return education
    return _create_education_with_achievements


@pytest.fixture
def service_query_data():
    return {
        'title': 'Test Service Query',
        'description': 'Test description',
        'is_active': True,
        'order': 1
    }


@pytest.fixture
def create_service_query(service_query_data):
    def _create_service_query(**kwargs):
        data = service_query_data.copy()
        data.update(kwargs)
        return ServiceQuery.objects.create(**data)
    return _create_service_query


@pytest.fixture
def exclude_service_data():
    return {
        'title': 'Test Exclude Service',
        'description': 'Test description',
        'is_active': True,
        'order': 1
    }


@pytest.fixture
def create_exclude_service(exclude_service_data):
    def _create_exclude_service(**kwargs):
        data = exclude_service_data.copy()
        data.update(kwargs)
        return ExcludeService.objects.create(**data)
    return _create_exclude_service