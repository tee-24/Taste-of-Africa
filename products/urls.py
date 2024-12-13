from django.urls import path
from . import views

urlpatterns = [
    path('mains/', views.mains, name='mains'),
]