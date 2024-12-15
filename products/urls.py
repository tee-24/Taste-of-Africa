from django.urls import path
from . import views

urlpatterns = [
    path('mains/', views.mains, name='mains'),
    path('sides/', views.sides, name='sides'),
    path('drinks/', views.drinks, name='drinks'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product')
]
