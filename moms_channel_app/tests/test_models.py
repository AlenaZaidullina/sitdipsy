import pytest
from moms_channel_app.models import Testimonial

pytestmark = pytest.mark.django_db


class TestTestimonialModel:
    def test_create_testimonial(self, create_testimonial):
        """Тест создания отзыва"""
        testimonial = create_testimonial(alt_text="Test Alt Text")

        assert testimonial.id is not None
        assert testimonial.alt_text == "Test Alt Text"
        assert testimonial.is_active == True
        assert testimonial.order == 1

    def test_testimonial_str_method(self, create_testimonial):
        """Тест строкового представления модели"""
        testimonial = create_testimonial()

        expected_str = f"Отзыв #{testimonial.id} - {testimonial.created_at.strftime('%d.%m.%Y')}"
        assert str(testimonial) == expected_str

    def test_default_ordering(self, create_testimonial):
        """Тест порядка сортировки по умолчанию"""

        testimonial_low_order = create_testimonial(order=1)
        testimonial_high_order1 = create_testimonial(order=2)
        testimonial_high_order2 = create_testimonial(order=2)

        testimonials = list(Testimonial.objects.all())

        assert testimonials[0].order == 1  # Самый низкий order первый
        assert testimonials[1].order == 2
        assert testimonials[2].order == 2

        # Проверяет, что testimonial с order=1 идет первым
        assert testimonials[0] == testimonial_low_order

        # Среди объектов с одинаковым order=2, более новые идут первыми
        assert testimonial_high_order2.created_at > testimonial_high_order1.created_at
        assert testimonials[1] == testimonial_high_order2  # Более новый first
        assert testimonials[2] == testimonial_high_order1  # Более старый second

    def test_verbose_names(self):
        """Тест verbose names"""
        assert Testimonial._meta.verbose_name == 'Отзыв'
        assert Testimonial._meta.verbose_name_plural == 'Отзывы'

    def test_field_verbose_names(self):
        """Тест verbose names полей"""
        field_verbose_names = {
            'image': 'Изображение отзыва',
            'alt_text': 'Альтернативный текст',
            'order': 'Порядок отображения',
            'created_at': 'Дата создания',
            'is_active': 'Активный'
        }

        for field_name, expected_verbose in field_verbose_names.items():
            field = Testimonial._meta.get_field(field_name)
            assert field.verbose_name == expected_verbose