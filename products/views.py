from django.shortcuts import (
    render, redirect, reverse, get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.core.mail import send_mail
from .models import Product, Review, Favourites
from .forms import ProductForm, ContactForm

import os


def category_view(request, category_id):
    """ A view to show products by category, including sorting """
    products = Product.objects.filter(category=category_id)
    category_id = 'all'

    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    context = {'products': products}
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.filter(approved=True)
    context = {
        'product': product,
        'reviews': reviews
        }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        messages.error(
            request, 'Failed to add product. Please ensure the form is valid.'
        )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {'form': form}
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        messages.error(
            request,
            'Failed to update product. Please ensure the form is valid.'
        )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {'form': form, 'product': product}
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    category = product.category
    category_id = category.id if category else None

    product.delete()
    messages.success(request, 'Product deleted!')

    if category_id:
        return redirect(reverse('category_view', args=[category_id]))
    return redirect(reverse('category_view', kwargs={'category_id': 'all'}))


@login_required
def add_review(request, product_id):
    """ Add a review for a product """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Create the review
        Review.objects.create(
            user=request.user, product=product, rating=rating, comment=comment
        )
        return redirect('product_detail', product_id=product_id)

    context = {'product': product}
    return render(request, 'products/product_detail.html', context)


@login_required
def toggle_favourite(request, product_id):
    """ Add or remove a product from favourites """
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        favourite, created = Favourites.objects.get_or_create(
            user=request.user, product=product
        )
        if not created:
            favourite.delete()
        return redirect('product_detail', product_id=product_id)
    return redirect('login')


@login_required
def favourites(request):
    """ View to display the products that the user has marked as favourites """
    user_favourites = Favourites.objects.filter(user=request.user)
    favourite_products = [favourite.product for favourite in user_favourites]

    context = {'favourite_products': favourite_products}
    return render(request, 'products/favourites.html', context)


def contact_us(request):
    """ Contact form submission handler """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            admin_email = (
                'boutiqueado@example.com'
                if 'DEVELOPMENT' in os.environ
                else os.environ.get('EMAIL_HOST_USER')
            )

            send_mail(
                f"New Contact Us Message: {contact_message.subject}",
                contact_message.message,
                contact_message.email,
                [admin_email],
                fail_silently=False,
            )
            messages.success(request,
            'Your message has been sent successfully!')

            return redirect('contact_us')
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'products/contact_us.html', context)
