from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from products.models import PriceTier
from designs.models import Design
import decimal # Importe o módulo decimal
from django.core.mail import send_mail
from django.conf import settings

@require_POST # Garante que esta view só possa ser acedida com um pedido POST.
# O design_id agora é opcional, com um valor padrão de None.
def add_to_cart_view(request, tier_id, design_id=None):
    """
    Adiciona um produto à sacola de orçamento.
    Agora lida com casos com e sem um design associado.
    """
    cart = request.session.get('cart', {})
    tier = get_object_or_404(PriceTier, id=tier_id)
    
    # Verifica se o pedido é para um serviço de design
    is_design_service = request.POST.get('is_design_service')

    # Prepara os dados do item.
    item_data = {
        'variation_name': tier.product_variation.name,
        'quantity': tier.quantity,
        'price': str(tier.price),
        'tier_id': tier.id,
    }

    if is_design_service:
        item_data['design_fee'] = str(tier.product_variation.product_type.design_creation_fee)

    # Se um design_id foi fornecido, adicione os detalhes do design.
    if design_id:
        design = get_object_or_404(Design, id=design_id)
        item_data['design_id'] = design.id
        item_data['design_name'] = design.name
        item_data['image_url'] = design.image.url if design.image else ''
    else:
        # Se não houver design, podemos definir valores padrão ou nulos.
        product_type = tier.product_variation.product_type
        item_data['design_id'] = None
        item_data['design_name'] = "Arte personalizada"
        item_data['image_url'] = product_type.image.url if product_type.image else None

    # Usa o ID do tier como chave na sacola.
    tier_id_str = str(tier.id)
    cart[tier_id_str] = item_data
    
    request.session['cart'] = cart
    
    # Prepara a mensagem de sucesso e o redirecionamento.
    cart_url = reverse('orders:cart_detail')
    success_message = f'Item adicionado! <a href="{cart_url}" class="alert-link">Ver sacola</a>.'
    messages.success(request, mark_safe(success_message))
    
    # Redireciona de volta para a página correta.
    if design_id:
        return redirect('designs:detail', design_id=design_id)
    else:
        # Redireciona para a lista de variações do produto.
        product_type_slug = tier.product_variation.product_type.slug
        return redirect('products:product_variation_list', slug=product_type_slug)

@require_POST
def remove_from_cart_view(request, tier_id):
    """
    Remove um item da sacola de orçamento.
    """
    cart = request.session.get('cart', {})
    tier_id_str = str(tier_id)

    if tier_id_str in cart:
        # Remove o item do dicionário da sacola.
        del cart[tier_id_str]
        messages.success(request, "Item removido da sua sacola.")
        # Salva as alterações na sessão.
        request.session['cart'] = cart
    
    return redirect('orders:cart_detail')

def cart_detail_view(request):
    cart = request.session.get('cart', {})
    
    # --- LÓGICA DE SEPARAÇÃO DOS ITENS ---
    design_items = []
    custom_art_items = []
    hire_design_items = []

    for item_id, item in cart.items():
        # Itens com taxa de design vão para a lista de "Contratar Design"
        if item.get('design_fee'):
            hire_design_items.append(item)
        # Itens com ID de design (mas sem taxa) vão para "Modelos Prontos"
        elif item.get('design_id'):
            design_items.append(item)
        # Os restantes são do fluxo "Enviar Minha Arte"
        else:
            custom_art_items.append(item)

    # Lógica de cálculo movida para a view para ser mais robusta.
    subtotal = sum(decimal.Decimal(item['price']) for item in cart.values())
    total_design_fee = sum(decimal.Decimal(item.get('design_fee', 0)) for item in cart.values())
    total = subtotal + total_design_fee
    
    context = {
        'design_items': design_items,
        'custom_art_items': custom_art_items,
        'hire_design_items': hire_design_items,
        'subtotal': subtotal,
        'total_design_fee': total_design_fee,
        'total': total,
    }
    return render(request, 'orders/cart_detail.html', context)

@require_POST
def submit_cart_view(request):
    """
    Recebe os dados do formulário da sacola, envia um email com o resumo do pedido
    e limpa a sacola.
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Sua sacola está vazia.")
        return redirect('orders:cart_detail')

    # Coleta os dados de contato do formulário
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    company = request.POST.get('company', '') # Campo opcional

    # Monta a mensagem do email com o resumo dos itens
    message_body = f"""
    Novo Pedido de Orçamento (do site)

    DADOS DO CLIENTE:
    - Nome: {name}
    - Email: {email}
    - Telefone: {phone}
    - Empresa: {company or 'Não informado'}

    -----------------------------------

    ITENS DO ORÇAMENTO:
    """

    subtotal = decimal.Decimal(0)
    total_design_fee = decimal.Decimal(0)

    for item in cart.values():
        price = decimal.Decimal(item['price'])
        design_fee = decimal.Decimal(item.get('design_fee', 0))
        subtotal += price
        total_design_fee += design_fee
        
        message_body += f"\n- Produto: {item['variation_name']}"
        if item.get('design_name'):
            message_body += f"\n  Design: {item['design_name']}"
        message_body += f"\n  Quantidade: {item['quantity']}"
        message_body += f"\n  Preço do Item: R$ {price:.2f}"
        if design_fee > 0:
            message_body += f"\n  Taxa de Arte: R$ {design_fee:.2f}"
        message_body += "\n"

    total = subtotal + total_design_fee
    message_body += f"""
    -----------------------------------
    RESUMO FINANCEIRO:
    - Subtotal dos Produtos: R$ {subtotal:.2f}
    - Taxa de Arte Total: R$ {total_design_fee:.2f}
    - TOTAL DO ORÇAMENTO: R$ {total:.2f}
    """

    try:
        send_mail(
            f'Novo Orçamento do Site - {name}',
            message_body,
            settings.DEFAULT_FROM_EMAIL,
            ['contato@premiumgrafica.com.br'],
            fail_silently=False,
        )
        # Limpa a sacola após o envio bem-sucedido
        request.session['cart'] = {}
        messages.success(request, 'Seu pedido de orçamento foi enviado com sucesso! Agradecemos o seu contato.')
    except Exception as e:
        messages.error(request, 'Ocorreu um erro ao enviar seu pedido. Por favor, tente novamente.')
        print(f"Erro ao enviar email: {e}")

    return redirect('designs:gallery') # Redireciona para a página inicial