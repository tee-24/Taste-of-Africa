from django.shortcuts import render
from .models import Product


def mains(request):
    """ A view to show all mains, including sorting """

    # Filter products by category 'mains'
    products = Product.objects.filter(category=1)

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)

