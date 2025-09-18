import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from main_app.models import Education, EducationAchievement, DiplomaImage, ServiceQuery, ExcludeService
from .factories import EducationFactory, EducationAchievementFactory, DiplomaImageFactory, ServiceQueryFactory, \
    ExcludeServiceFactory


@pytest.mark.django_db
class TestEducationModel:
    """Тесты для модели Education"""

    def test_create_education(self):
        education = EducationFactory()
        assert education.pk is not None
        assert education.year is not None
        assert education.is_active is True

    def test_education_str(self):
        education = EducationFactory(year="2023")
        assert str(education) == "2023"

    def test_education_ordering(self):
        education1 = EducationFactory(order=2)
        education2 = EducationFactory(order=1)

        educations = Education.objects.all()
        assert educations[0].order == 1
        assert educations[1].order == 2

    def test_education_meta(self):
        assert Education._meta.verbose_name == "Год обучения"
        assert Education._meta.verbose_name_plural == "Годы обучения"
        assert Education._meta.ordering == ['order']


@pytest.mark.django_db
class TestEducationAchievementModel:
    """Тесты для модели EducationAchievement"""

    def test_create_achievement(self):
        achievement = EducationAchievementFactory()
        assert achievement.pk is not None
        assert achievement.education is not None

    def test_achievement_str(self):
        achievement = EducationAchievementFactory(title="Test Achievement")
        assert str(achievement) == "Test Achievement"

    def test_achievement_ordering(self):
        education = EducationFactory()
        achievement1 = EducationAchievementFactory(education=education, order=2)
        achievement2 = EducationAchievementFactory(education=education, order=1)

        achievements = EducationAchievement.objects.filter(education=education)
        assert achievements[0].order == 1
        assert achievements[1].order == 2

    def test_achievement_meta(self):
        assert EducationAchievement._meta.verbose_name == "Достижение/Сертификат"
        assert EducationAchievement._meta.verbose_name_plural == "Достижения/Сертификаты"


@pytest.mark.django_db
class TestDiplomaImageModel:
    """Тесты для модели DiplomaImage"""

    def test_create_diploma_image(self):
        diploma = DiplomaImageFactory()
        assert diploma.pk is not None
        assert diploma.achievement is not None
        assert diploma.image is not None

    def test_diploma_image_str(self):
        achievement = EducationAchievementFactory(title="Test Achievement")
        diploma = DiplomaImageFactory(achievement=achievement, order=1)
        assert "Изображение 1 для Test Achievement" in str(diploma)

    def test_diploma_ordering(self):
        achievement = EducationAchievementFactory()
        diploma1 = DiplomaImageFactory(achievement=achievement, order=2)
        diploma2 = DiplomaImageFactory(achievement=achievement, order=1)

        diplomas = DiplomaImage.objects.filter(achievement=achievement)
        assert diplomas[0].order == 1
        assert diplomas[1].order == 2

    def test_diploma_meta(self):
        assert DiplomaImage._meta.verbose_name == "Изображение диплома"
        assert DiplomaImage._meta.verbose_name_plural == "Изображения дипломов"


@pytest.mark.django_db
class TestServiceQueryModel:
    """Тесты для модели ServiceQuery"""

    def test_create_service_query(self):
        service = ServiceQueryFactory()
        assert service.pk is not None
        assert service.title is not None

    def test_service_query_str(self):
        service = ServiceQueryFactory(title="Test Service")
        assert str(service) == "Test Service"

    def test_service_query_ordering(self):
        service1 = ServiceQueryFactory(order=2)
        service2 = ServiceQueryFactory(order=1)

        services = ServiceQuery.objects.all()
        assert services[0].order == 1
        assert services[1].order == 2

    def test_service_query_meta(self):
        assert ServiceQuery._meta.verbose_name == "Запрос для работы"
        assert ServiceQuery._meta.verbose_name_plural == "Запросы для работы"


@pytest.mark.django_db
class TestExcludeServiceModel:
    """Тесты для модели ExcludeService"""

    def test_create_exclude_service(self):
        exclude = ExcludeServiceFactory()
        assert exclude.pk is not None
        assert exclude.title is not None

    def test_exclude_service_str(self):
        exclude = ExcludeServiceFactory(title="Test Exclude")
        assert str(exclude) == "Test Exclude"

    def test_exclude_service_ordering(self):
        exclude1 = ExcludeServiceFactory(order=2)
        exclude2 = ExcludeServiceFactory(order=1)

        excludes = ExcludeService.objects.all()
        assert excludes[0].order == 1
        assert excludes[1].order == 2

    def test_exclude_service_meta(self):
        assert ExcludeService._meta.verbose_name == "Исключенное направление"
        assert ExcludeService._meta.verbose_name_plural == "Исключенные направления"