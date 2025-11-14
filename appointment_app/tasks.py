from celery import shared_task
from django.utils import timezone
from .models import AvailableTime
from datetime import timedelta


@shared_task
def cleanup_unbooked_times():
    # Очищаем слоты, которые не забронированы на завтра
    times_to_delete = AvailableTime.objects.filter(
        is_booked=False,
        date__date=timezone.now().date() + timedelta(days=1),
        time__gte=timezone.now().time()
    )
    deleted_count = times_to_delete.delete()[0]
    return f"Удалено {deleted_count} слотов."

