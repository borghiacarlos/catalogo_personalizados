from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

#def index_view(request):
#    Usamos o renderizador padrão do Django agora
#    Apontaremos para um novo template: 'core/pages/index.html'
#    context = {
#        'message': 'Olá do Django para um template com Bootstrap!'
#    }
#    return render(request, 'core/pages/index.html', context)

def quote_request_view(request):
    """
    Exibe o formulário de orçamento personalizado e trata o envio por email.
    """
    if request.method == 'POST':
        # --- Lógica de Envio de Email ---
        # Pegamos os dados do formulário
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        material_type = request.POST.get('material_type')
        material_format = request.POST.get('material_format')
        paper_type = request.POST.get('paper_type')
        printing_color = request.POST.get('printing_color')
        printing_sides = request.POST.get('printing_sides')
        finishing = request.POST.get('finishing')
        embellishment = request.POST.get('embellishment')
        quantity = request.POST.get('quantity')
        details = request.POST.get('details')

        # Montamos a mensagem do email
        subject = f'Novo Pedido de Orçamento Personalizado - {name}'
        message_body = f"""
        Um novo pedido de orçamento foi recebido através do site.

        DADOS DE CONTATO:
        - Nome: {name}
        - Email: {email}
        - Telefone/WhatsApp: {phone}

        DETALHES DO ORÇAMENTO:
        - Tipo de Material: {material_type}
        - Formato: {material_format}
        - Papel: {paper_type}
        - Impressão: {printing_color}
        - Lados (Frente/Verso): {printing_sides or 'Não especificado'}
        - Acabamentos: {finishing}
        - Enobrecimento: {embellishment}
        - Quantidade: {quantity}
        
        DETALHES ADICIONAIS:
        {details}
        """
        
        try:
            # Enviamos o email
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL, # Remetente
                ['contato@premiumgrafica.com.br'], # Destinatário
                fail_silently=False,
            )
            messages.success(request, 'Seu pedido de orçamento foi enviado com sucesso! Entraremos em contato em breve.')
        except Exception as e:
            messages.error(request, 'Ocorreu um erro ao enviar seu pedido. Por favor, tente novamente ou contate-nos pelo WhatsApp.')
            print(e) # Para debug no console

        return redirect('quote_request')

    return render(request, 'core/pages/quote_request.html')