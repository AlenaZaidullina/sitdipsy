import pytest
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.test import RequestFactory
from moms_channel_app.models import Testimonial
from moms_channel_app.admin import TestimonialAdmin

pytestmark = pytest.mark.django_db


class TestTestimonialAdmin:
    def test_admin_list_display(self, create_testimonial):
        """Тест отображаемых полей в админке"""
        testimonial = create_testimonial()

        admin = TestimonialAdmin(Testimonial, site)

        expected_list_display = ['id', 'image_preview', 'alt_text', 'order', 'created_at', 'is_active']
        assert admin.list_display == expected_list_display

    def test_admin_list_editable(self):
        """Тест редактируемых полей в админке"""
        admin = TestimonialAdmin(Testimonial, site)

        expected_list_editable = ['order', 'is_active']
        assert admin.list_editable == expected_list_editable

    def test_admin_search_fields(self):
        """Тест полей поиска"""
        admin = TestimonialAdmin(Testimonial, site)

        expected_search_fields = ['alt_text']
        assert admin.search_fields == expected_search_fields

    def test_admin_image_preview(self, create_testimonial):
        """Тест превью изображения в админке"""
        testimonial = create_testimonial()

        admin = TestimonialAdmin(Testimonial, site)
        preview = admin.image_preview(testimonial)

        # Проверяем, что возвращается HTML с изображением
        assert 'img' in preview
        assert 'src' in preview

    def test_admin_image_preview_no_image(self):
        """Тест превью без изображения"""
        testimonial = Testimonial()  # Без изображения

        admin = TestimonialAdmin(Testimonial, site)
        preview = admin.image_preview(testimonial)

        assert preview == "Нет изображения"

    @pytest.mark.skip("Требует настройки аутентификации")
    def test_admin_changelist_view(self, admin_client, create_testimonial):
        """Тест просмотра списка в админке"""
        create_testimonial()

        url = '/admin/moms_channel_app/testimonial/'
        response = admin_client.get(url)

        assert response.status_code == 200