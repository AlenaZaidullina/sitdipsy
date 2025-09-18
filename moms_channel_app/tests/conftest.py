import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from moms_channel_app.models import Testimonial


@pytest.fixture
def testimonial_data():
    """Фикстура с данными для тестового отзыва"""
    return {
        'alt_text': 'Test testimonial',
        'order': 1,
        'is_active': True
    }


@pytest.fixture
def create_testimonial(testimonial_data):
    """Фикстура для создания тестового отзыва"""

    def _create_testimonial(**kwargs):
        data = testimonial_data.copy()
        data.update(kwargs)

        # Создаем mock изображение
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        return Testimonial.objects.create(
            image=image,
            **data
        )

    return _create_testimonial


@pytest.fixture
def active_testimonial(create_testimonial):
    """Активный отзыв"""
    return create_testimonial(is_active=True)


@pytest.fixture
def inactive_testimonial(create_testimonial):
    """Неактивный отзыв"""
    return create_testimonial(is_active=False)