# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.cart_detail_view, name='cart_detail'),
    path('remove/<int:tier_id>/', views.remove_from_cart_view, name='remove_from_cart'),

    # URL para adicionar itens COM um design
    path('add/<int:design_id>/<int:tier_id>/', views.add_to_cart_view, name='add_to_cart_with_design'),

    # NOVA URL: Para adicionar itens SEM um design
    path('add/<int:tier_id>/', views.add_to_cart_view, name='add_to_cart_without_design'),

    # NOVA ROTA para o envio do formulário da sacola
    path('submit/', views.submit_cart_view, name='submit_cart'),
]