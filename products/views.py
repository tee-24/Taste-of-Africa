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

def sides(request):
    """ A view to show all sides, including sorting """


    # Filter products by category 'sides'
    products = Product.objects.filter(category=2)


    context = {
        'products': products,
    }


    return render(request, 'products/products.html', context)


def drinks(request):
    """ A view to show all drinks, including sorting """


    # Filter products by category 'drinks'
    products = Product.objects.filter(category=3)


    context = {
        'products': products,
    }


    return render(request, 'products/products.html', context)