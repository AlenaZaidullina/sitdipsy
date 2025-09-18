from django.shortcuts import render
from .models import Testimonial


def moms_channel(request):
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')

    context = {
        'testimonials': testimonials
    }

    return render(request, 'moms_channel_app/channel.html', context)