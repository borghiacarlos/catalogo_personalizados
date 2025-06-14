from django.contrib import admin
from .models import Category, Color, Design

# Customizando a exibição dos models do app 'designs'.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o model Category.
    """
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o model Color.
    """
    list_display = ('name', 'hex_code')


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o model Design.
    """
    list_display = ('name',)
    list_filter = ('categories', 'colors')
    search_fields = ('name',)
    # Melhora a interface de seleção para campos 'muitos-para-muitos',
    # trocando a caixa de seleção múltipla por uma interface com duas caixas.
    filter_horizontal = ('categories', 'colors', 'available_variations')

