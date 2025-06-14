# products/views.py
from django.shortcuts import render, get_object_or_404
from .models import ProductType

def product_type_gallery_view(request, is_design_service=False):
    """
    Exibe uma galeria com todos os tipos de produtos disponíveis.
    """
    product_types = ProductType.objects.all()
    context = {
        'product_types': product_types,
        'is_design_service': is_design_service, # Passa a flag para o template
    }
    return render(request, 'products/product_type_gallery.html', context)

def product_variation_list_view(request, slug, is_design_service=False):
    """
    Exibe as variações disponíveis para um tipo de produto específico.
    É muito semelhante à nossa página de detalhes do design, mas sem o design.
    """
    product_type = get_object_or_404(ProductType, slug=slug)
    # A lógica para adicionar ao carrinho será um pouco diferente aqui,
    # pois não temos um 'design'. Vamos abordar isso num próximo passo.
    variations = product_type.variations.all()
    
    context = {
        'product_type': product_type,
        'variations': variations, # E passamo-las no contexto.
        'is_design_service': is_design_service,
    }
    return render(request, 'products/product_variation_list.html', context)
