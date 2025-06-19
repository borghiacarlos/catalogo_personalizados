from django.db import models
from cloudinary.models import CloudinaryField # Importe o CloudinaryField

# Modelagem para os Tipos de Produtos e suas Variações

class ProductType(models.Model):
    """
    Representa o tipo de impresso. Ex: 'Cartão de Visita', 'Pasta', 'Envelope'.
    Será usado para organizar as variações e no fluxo "Quero Enviar Minha Arte".
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do Tipo de Produto")
    slug = models.SlugField(max_length=100, unique=True, help_text="Versão do nome otimizada para URLs.")

    design_creation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Taxa de Criação de Arte",
        help_text="Valor cobrado para criar a arte para este tipo de produto. Deixe 0 se não houver taxa."
    )

    # image = models.ImageField(
    #     upload_to='product_types/',
    #     blank=True, # A imagem é opcional
    #     null=True,
    #     verbose_name="Imagem representativa do produto",
    #     help_text="Imagem que aparecerá na galeria de produtos."
    # )

    image = CloudinaryField('image', blank=True, null=True, folder='product_types')

    class Meta:
        verbose_name = "Tipo de Produto"
        verbose_name_plural = "Tipos de Produtos"

    def __str__(self):
        return self.name

class ProductVariation(models.Model):
    """
    Representa uma versão específica e pré-configurada de um produto.
    Ex: 'Cartão Premium com Verniz', 'Cartão Econômico'.
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="variations", verbose_name="Tipo de Produto")
    name = models.CharField(max_length=100, verbose_name="Nome da Variação")
    # icon_image = models.ImageField(upload_to='products/icons/', blank=True, null=True, verbose_name="Ícone Visual")
    icon_image = CloudinaryField('icon_image', blank=True, null=True, folder='products/icons')
    detailed_description = models.TextField(
        blank=True,
        verbose_name="Descrição Detalhada",
        help_text="Explique em detalhes sobre o produto, papel, acabamentos, etc."
    )
    video_url = models.URLField(
        blank=True,
        verbose_name="URL do Vídeo (YouTube, Vimeo)",
        help_text="Cole aqui o link 'embed' do vídeo."
    )

    class Meta:
        verbose_name = "Variação de Produto"
        verbose_name_plural = "Variações de Produtos"
        unique_together = ('product_type', 'name')

    def __str__(self):
        return f"{self.product_type.name} - {self.name}"

class ProductImage(models.Model):
    """
    Uma imagem da galeria para uma ProductVariation.
    """
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name="images", verbose_name="Variação de Produto")
    # image = models.ImageField(upload_to='products/gallery/', verbose_name="Imagem")
    image = CloudinaryField('image', folder='products/gallery')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Texto Alternativo (SEO)")

    class Meta:
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens do Produto"

    def __str__(self):
        return f"Imagem para {self.product_variation.name}"

# NOVO MODEL PARA AS ESPECIFICAÇÕES
class Specification(models.Model):
    """
    Uma característica específica de uma ProductVariation.
    Ex: Para 'Cartão Premium', uma especificação pode ser 'Papel: Couchê 300g'.
    """
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name="specifications", verbose_name="Variação de Produto")
    name = models.CharField(max_length=100, verbose_name="Nome da Característica") # Ex: "Papel"
    value = models.CharField(max_length=255, verbose_name="Valor da Característica") # Ex: "Couchê 300g"

    icon = models.CharField(
        max_length=50,
        blank=True, # O ícone é opcional
        verbose_name="Classe do Ícone (Bootstrap Icons)",
        help_text="Ex: 'bi-rulers' ou 'bi-palette'. Veja os nomes em bootstrap-icons."
    )
    
    class Meta:
        verbose_name = "Especificação"
        verbose_name_plural = "Especificações"
        # Garante que não haja duas características com o mesmo nome para a mesma variação.
        unique_together = ('product_variation', 'name')

    def __str__(self):
        return f"{self.name}: {self.value}"


class PriceTier(models.Model):
    """
    Representa uma faixa de preço para uma quantidade específica de uma variação.
    Ex: Para a variação 'Cartão Premium', 1000 unidades custam R$ 150,00.
    """
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name="price_tiers", verbose_name="Variação de Produto")
    quantity = models.PositiveIntegerField(verbose_name="Quantidade")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")

    class Meta:
        verbose_name = "Faixa de Preço"
        verbose_name_plural = "Faixas de Preço"
        unique_together = ('product_variation', 'quantity')
        ordering = ['quantity']

    def __str__(self):
        return f"{self.product_variation.name} - {self.quantity} un. - R$ {self.price}"
