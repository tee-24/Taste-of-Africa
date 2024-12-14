from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Q6D2EHctCDJgekX6S9y4iAMBakq8eQDkPAhrmntZdY36kRNBh5ADQobaCgvvS2piO1c78LL3qY1E2o78Fb45PUe00vNJ1IbDC',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)