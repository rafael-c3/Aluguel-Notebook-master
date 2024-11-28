# produtos/urls.py
from django.urls import path
from . import views
app_name = 'produtos'

urlpatterns = [
    # Página para listar os produtos (disponível para todos)
    path('', views.listar_produtos, name='listar_produtos'),
    
    # URLs para adicionar, editar e remover produtos (disponíveis apenas para administradores)
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('remover/<int:produto_id>/', views.remover_produto, name='remover_produto'),
    path('listar_modelos/', views.listar_modelos, name='listar_modelos'),
    path('detalhes_produto/<int:produto_id>/', views.detalhes_produto, name='detalhes_produto'),
    path('preencher_form/', views.preencher_form, name='preencher_form'),
    path('login/', views.login, name='login'),
    path('alugar/<int:produto_id>/', views.alugar_produto, name='alugar_produto'),
    path('meus_alugueis/', views.listar_alugueis, name='listar_alugueis'),
    path('adm_alugueis/', views.adm_alugueis, name='adm_alugueis'),
    path('deletar_aluguel/<int:aluguel_id>/', views.deletar_aluguel, name='deletar_aluguel'),
]