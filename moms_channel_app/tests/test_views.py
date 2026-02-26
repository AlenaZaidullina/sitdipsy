import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestMomsChannelView:
    def test_moms_channel_view_status_code(self, client):
        """Тест статус кода главной страницы"""
        url = reverse('moms_channel')
        response = client.get(url)

        assert response.status_code == 200

    def test_moms_channel_view_template(self, client):
        """Тест используемого шаблона"""
        url = reverse('moms_channel')
        response = client.get(url)

        assert 'moms_channel_app/channel.html' in [t.name for t in response.templates]

    def test_moms_channel_view_context(self, client, create_testimonial):
        """Тест контекста представления"""
        # активные и неактивные отзывы
        active_testimonial = create_testimonial(is_active=True)
        inactive_testimonial = create_testimonial(is_active=False)

        url = reverse('moms_channel')
        response = client.get(url)


        assert 'testimonials' in response.context


        testimonials = response.context['testimonials']
        assert active_testimonial in testimonials
        assert inactive_testimonial not in testimonials

    def test_moms_channel_view_ordering(self, client, create_testimonial):
        """Тест порядка отзывов в представлении"""

        testimonial1 = create_testimonial(order=2, is_active=True)
        testimonial2 = create_testimonial(order=1, is_active=True)

        url = reverse('moms_channel')
        response = client.get(url)

        testimonials = list(response.context['testimonials'])


        assert testimonials[0].order <= testimonials[1].order

    def test_empty_testimonials(self, client):
        """Тест пустого списка отзывов"""
        url = reverse('moms_channel')
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context['testimonials']) == 0