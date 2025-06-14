from django.shortcuts import render, get_object_or_404
from .models import Design, Category, Color
from products.models import ProductType

def design_gallery_view(request):
    """
    Esta view busca todos os objetos Design, mas agora também aplica
    filtros de categoria e cor baseados nos parâmetros da URL (GET).
    """
    designs = Design.objects.all().order_by('name')
    
    # Busca apenas as categorias que estão ligadas a pelo menos um design.
    # .distinct() garante que cada categoria apareça apenas uma vez.
    all_categories = Category.objects.filter(designs__isnull=False).distinct()

    # Faz o mesmo para as cores.
    all_colors = Color.objects.filter(designs__isnull=False).distinct()

    # E para os tipos de produto, navegando através das relações.
    all_product_types = ProductType.objects.filter(variations__designs__isnull=False).distinct()

    # Pega os valores dos filtros enviados pelo formulário via método GET.
    # request.GET.get('...') retorna o valor ou None se não existir.
    category_id = request.GET.get('category')
    color_id = request.GET.get('color')
    product_type_id = request.GET.get('product_type') # NOVO

    # Aplica os filtros se eles foram selecionados.
    if category_id:
        # Filtra o queryset 'designs' para incluir apenas aqueles que
        # pertencem à categoria com o ID especificado.
        designs = designs.filter(categories__id=category_id)
    
    if color_id:
        # Filtra o queryset 'designs' para incluir apenas aqueles que
        # pertencem à cor com o ID especificado.
        designs = designs.filter(colors__id=color_id)

    if product_type_id:
    # A sintaxe 'available_variations__product_type__id' navega através
    # das relações entre os modelos para encontrar o ID do tipo de produto.
    # .distinct() garante que não teremos designs duplicados nos resultados.
        designs = designs.filter(available_variations__product_type__id=product_type_id).distinct()


    context = {
        'designs': designs,
        'all_categories': all_categories,
        'all_colors': all_colors,
        'all_product_types': all_product_types, # NOVO
        # Passamos os IDs selecionados de volta para o template para
        # que os filtros permaneçam selecionados após a busca.
        'selected_category_id': int(category_id) if category_id else None,
        'selected_color_id': int(color_id) if color_id else None,
        'selected_product_type_id': int(product_type_id) if product_type_id else None, # NOVO
    }
    
    return render(request, 'designs/gallery.html', context)

def design_detail_view(request, design_id):
    """
    Busca um único objeto Design pelo seu ID e o exibe.
    """
    # get_object_or_404 é uma função de atalho do Django.
    # Ela tenta buscar o objeto. Se não encontrar, exibe uma
    # página de "Não Encontrado (404)" automaticamente. É uma ótima prática!
    design = get_object_or_404(Design, id=design_id)
    
    # O contexto passa o objeto 'design' encontrado para o template.
    context = {
        'design': design
    }
    
    return render(request, 'designs/design_detail.html', context)
