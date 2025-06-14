from django.db import models
# Importamos o model ProductVariation do app 'products' para criar a relação.
from products.models import ProductVariation

# Modelagem para os Designs e seus filtros

class Category(models.Model):
    """
    Categorias para filtrar os designs. Ex: 'Advocacia', 'Odontologia', 'Pet Shop'.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    slug = models.SlugField(max_length=100, unique=True, help_text="Versão do nome otimizada para URLs.")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return self.name

class Color(models.Model):
    """
    Cores para filtrar os designs.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Nome da Cor")
    hex_code = models.CharField(max_length=7, unique=True, help_text="Código Hexadecimal da cor. Ex: #FF5733", verbose_name="Código Hex")

    class Meta:
        verbose_name = "Cor"
        verbose_name_plural = "Cores"
        ordering = ['name']

    def __str__(self):
        return self.name

class Design(models.Model):
    """
    O modelo de arte principal do catálogo.
    """
    name = models.CharField(max_length=100, verbose_name="Nome do Design")
    image = models.ImageField(upload_to='designs/', verbose_name="Imagem Principal")
    categories = models.ManyToManyField(Category, related_name="designs", verbose_name="Categorias")
    colors = models.ManyToManyField(Color, related_name="designs", blank=True, verbose_name="Cores")

    # Esta é a relação principal: Um design pode oferecer várias variações de produto.
    # Ex: Um design de cartão pode ser oferecido nas variações 'Econômico' e 'Premium'.
    available_variations = models.ManyToManyField(
        ProductVariation,
        related_name="designs",
        help_text="Selecione as variações de produto que podem ser usadas com este design.",
        verbose_name="Variações de Produto Disponíveis"
    )

    class Meta:
        verbose_name = "Design"
        verbose_name_plural = "Designs"

    def __str__(self):
        return self.name
