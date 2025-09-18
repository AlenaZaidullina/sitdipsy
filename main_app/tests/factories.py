import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from main_app.models import Education, EducationAchievement, DiplomaImage, ServiceQuery, ExcludeService


class EducationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Education

    year = factory.Faker('year')
    is_active = True
    order = factory.Sequence(int)


class EducationAchievementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EducationAchievement

    education = factory.SubFactory(EducationFactory)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text', max_nb_chars=200)
    is_active = True
    order = factory.Sequence(int)


class DiplomaImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DiplomaImage

    achievement = factory.SubFactory(EducationAchievementFactory)
    image = factory.LazyAttribute(lambda _: SimpleUploadedFile(
        "test_diploma.jpg", b"file_content", content_type="image/jpeg"
    ))
    order = factory.Sequence(int)


class ServiceQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServiceQuery

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=150)
    is_active = True
    order = factory.Sequence(int)


class ExcludeServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExcludeService

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=150)
    is_active = True
    order = factory.Sequence(int)