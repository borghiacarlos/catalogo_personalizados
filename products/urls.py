# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # As rotas mais específicas vêm primeiro.
    path('contratar-design/', views.product_type_gallery_view, {'is_design_service': True}, name='hire_design_gallery'),
    path('contratar-design/<slug:slug>/', views.product_variation_list_view, {'is_design_service': True}, name='hire_design_variation_list'),
    
    # As rotas mais genéricas vêm depois.
    path('', views.product_type_gallery_view, name='product_type_gallery'),
    path('<slug:slug>/', views.product_variation_list_view, name='product_variation_list'),
]