from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Registre os modelos do seu app normalmente
from .models import Produto

# Classe personalizada para o Admin
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'imagem')
    search_fields = ['nome']

# Adicionando o link para a página inicial na barra do admin
admin.site.site_header = 'Administração - Aluguel de Notebooks'
admin.site.index_title = 'Painel de Controle'
admin.site.site_title = 'Aluguel de Notebooks'

# Função para adicionar link para a página inicial
def redirect_to_home(request):
    return format_html('<a href="{0}">Ir para a página inicial</a>', reverse('listar_produtos'))

# Exibindo o link na barra de navegação
admin.site.add_action(redirect_to_home)

# Registrando os modelos no admin
admin.site.register(Produto, ProdutoAdmin)
