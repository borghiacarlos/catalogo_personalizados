# designs/urls.py

from django.urls import path
from . import views

app_name = 'designs'

urlpatterns = [
    # URL da nossa galeria (continua a mesma)
    path('', views.design_gallery_view, name='gallery'),
    
    # NOVA URL: Para a página de detalhe de um design específico.
    # <int:design_id> é um "conversor de caminho". Ele captura um número
    # da URL e o passa para a nossa view como um argumento chamado 'design_id'.
    path('designs/<int:design_id>/', views.design_detail_view, name='detail'),
]
