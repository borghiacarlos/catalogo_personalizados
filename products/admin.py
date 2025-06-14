from django.contrib import admin
from .models import ProductType, ProductVariation, PriceTier, Specification, ProductImage

# Para uma melhor experiência no admin, vamos customizar como os models são exibidos.

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    """
    Configura a exibição do ProductType no painel de administração.
    """
    fields = ('name', 'slug', 'image', 'design_creation_fee')
    list_display = ('name', 'slug', 'design_creation_fee')
    prepopulated_fields = {'slug': ('name',)}

# NOVO INLINE PARA A GALERIA DE IMAGENS
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # Mostra um campo para adicionar uma nova imagem.
    verbose_name = "Imagem da Galeria"
    verbose_name_plural = "Galeria de Imagens do Produto"

# NOVO INLINE PARA AS ESPECIFICAÇÕES
class SpecificationInline(admin.TabularInline):
    """
    Permite adicionar e editar as Especificações
    diretamente na página da Variação de Produto.
    """
    model = Specification
    extra = 1


class PriceTierInline(admin.TabularInline):
    """
    Permite adicionar e editar as Faixas de Preço (PriceTiers)
    diretamente na página da Variação de Produto (ProductVariation).
    """
    model = PriceTier
    extra = 1


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    """
    Configura a exibição da ProductVariation no painel de administração.
    """
    list_display = ('name', 'product_type')
    list_filter = ('product_type',)
    search_fields = ('name', 'product_type__name')

    # Adicione a descrição detalhada e o vídeo aos campos editáveis.
    # Usamos fieldsets para organizar melhor a página do admin.
    fieldsets = (
        (None, {
            'fields': ('product_type', 'name', 'icon_image')
        }),
        ('Conteúdo Detalhado (para o modal "Saiba Mais")', {
            'classes': ('collapse',), # Começa recolhido para não poluir
            'fields': ('detailed_description', 'video_url'),
        }),
    )
    # Adicionamos o novo inline à lista.
    inlines = [ProductImageInline, SpecificationInline, PriceTierInline]

