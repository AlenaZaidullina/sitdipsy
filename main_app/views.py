from django.db import models
from django.shortcuts import render
from .models import Education, ServiceQuery, ExcludeService, EducationAchievement


def index(request):
    #  годы обучения с активными достижениями и их изображениями
    education_items = Education.objects.filter(is_active=True).prefetch_related(
        models.Prefetch(
            'achievements',
            queryset=EducationAchievement.objects.filter(is_active=True)
            .prefetch_related('diploma_images')
            .order_by('order')
        )
    ).order_by('order')

    # активные сервисные запросы
    service_queries = ServiceQuery.objects.filter(is_active=True).order_by('order')

    # исключенные сервисы
    exclude_service = ExcludeService.objects.filter(is_active=True).order_by('order')

    return render(request, 'main_app/index.html', {
        'education_items': education_items,
        'service_queries': service_queries,
        'exclude_service': exclude_service,
    })




