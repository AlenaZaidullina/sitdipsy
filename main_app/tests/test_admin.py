import pytest
from django.contrib.admin.sites import site
from main_app.models import Education, EducationAchievement, ServiceQuery, ExcludeService
from main_app.admin import EducationAdmin, EducationAchievementAdmin, ServiceQueryAdmin, ExcludeServiceAdmin


@pytest.mark.django_db
class TestAdmin:
    """Тесты для админки"""

    def test_education_admin_registered(self):
        """Тест, что модель Education зарегистрирована в админке"""
        assert Education in site._registry

    def test_education_achievement_admin_registered(self):
        """Тест, что модель EducationAchievement зарегистрирована в админке"""
        assert EducationAchievement in site._registry

    def test_service_query_admin_registered(self):
        """Тест, что модель ServiceQuery зарегистрирована в админке"""
        assert ServiceQuery in site._registry

    def test_exclude_service_admin_registered(self):
        """Тест, что модель ExcludeService зарегистрирована в админке"""
        assert ExcludeService in site._registry

    def test_education_admin_config(self):
        """Тест конфигурации EducationAdmin"""
        admin = EducationAdmin(Education, site)
        assert admin.list_display == ('year', 'order', 'is_active')
        assert admin.list_editable == ('order', 'is_active')
        assert hasattr(admin, 'inlines')

    def test_education_achievement_admin_config(self):
        """Тест конфигурации EducationAchievementAdmin"""
        admin = EducationAchievementAdmin(EducationAchievement, site)
        assert admin.list_display == ('title', 'education', 'order', 'is_active')
        assert admin.list_editable == ('order', 'is_active')
        assert admin.list_filter == ('education', 'is_active')
        assert admin.search_fields == ('title', 'description')
        assert hasattr(admin, 'inlines')

    def test_service_query_admin_config(self):
        """Тест конфигурации ServiceQueryAdmin"""
        admin = ServiceQueryAdmin(ServiceQuery, site)
        assert admin.list_display == ('title', 'order', 'is_active')
        assert admin.list_editable == ('order', 'is_active')
        assert admin.search_fields == ('title', 'description')
        assert admin.list_filter == ('is_active',)

    def test_exclude_service_admin_config(self):
        """Тест конфигурации ExcludeServiceAdmin"""
        admin = ExcludeServiceAdmin(ExcludeService, site)
        assert admin.list_display == ('title', 'order', 'is_active')
        assert admin.list_editable == ('order', 'is_active')
        assert admin.search_fields == ('title', 'description')
        assert admin.list_filter == ('is_active',)