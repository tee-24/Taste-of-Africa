from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
     path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
     path('<int:product_id>/review/', views.add_review, name='add_review')
]
