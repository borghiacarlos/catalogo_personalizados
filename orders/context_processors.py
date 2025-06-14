# orders/context_processors.py

def cart_context(request):
    """
    Disponibiliza o conteúdo da sacola e a contagem de itens para todos os templates.
    """
    cart = request.session.get('cart', {})
    cart_item_count = len(cart)
    
    return {
        'cart': cart,
        'cart_item_count': cart_item_count,
    }
