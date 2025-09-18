from django.shortcuts import render
from .models import Product


def psyproducts(request):
    """
        Представление отображает страницы продуктов психологических услуг, разделяя их на бесплатные и платные.
        Собирает товары из базы данных, сортируя по датам добавления, и передает их в шаблон для рендеринга.
    """
    free_products = Product.objects.filter(is_free=True).order_by('-created_at')
    paid_products = Product.objects.filter(is_free=False).order_by('-created_at')

    context = {
        'free_products': free_products,
        'paid_products': paid_products,
    }
    return render(request, 'psyproducts_app/psyproducts.html', context)

