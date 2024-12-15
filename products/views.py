from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Product


from .forms import ProductForm

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


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)