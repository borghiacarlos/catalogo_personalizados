# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Vamos importar a view do app 'core'
from core import views as core_views

# A view 'index_view' foi movida para o app 'designs'
# Vamos importá-la do lugar certo depois.

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # A URL raiz '/' agora será a nossa galeria de designs.
    # Vamos usar as URLs do app 'designs'.
    path('', include('designs.urls', namespace='designs')), 

    # Incluindo as URLs do nosso app de pedidos
    path('sacola/', include('orders.urls', namespace='orders')),

    # NOVO: Incluindo as URLs do nosso app de produtos
    path('produtos/', include('products.urls', namespace='products')),

    path('orcamento-personalizado/', core_views.quote_request_view, name='quote_request'),
]

# Configuração para servir arquivos de mídia (uploads) em modo de desenvolvimento.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)