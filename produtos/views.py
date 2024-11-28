# produtos/views.py
import os
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import AlugarProdutoForm, ProdutoForm
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from django.http import HttpResponseForbidden
from .models import Produto, Aluguel
from django.contrib.admin.views.decorators import staff_member_required


# Função para verificar se o usuário é administrador (superusuário)
def admin_check(user):
    return user.is_superuser  # Verifica se o usuário é um superusuário (admin)

@login_required(login_url='/cadastro/')  # Redireciona para login se não autenticado
def listar_alugueis(request):
    # Filtra os aluguéis do usuário autenticado
    alugueis = Aluguel.objects.filter(usuario=request.user)
    return render(request, 'produtos/listar_alugueis.html', {'alugueis': alugueis})
@staff_member_required(login_url='')  # Permite acesso apenas a administradores
def adm_alugueis(request):
    alugueis = Aluguel.objects.all()  # Busca todos os registros de aluguel
    return render(request, 'produtos/adm_alugueis.html', {'alugueis': alugueis})

@staff_member_required(login_url='')
def deletar_aluguel(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id=aluguel_id)
    aluguel.delete()
    return redirect('produtos:adm_alugueis')

# Lista de produtos (disponível para todos os usuários)
def listar_produtos(request):
    produtos = Produto.objects.all()  # Todos os produtos
    return render(request, 'produtos/listar.html', {'produtos': produtos})

def detalhes_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'produtos/detalhes_produto.html', {'produto': produto})

# Adicionar produto (somente administradores podem adicionar produtos)
@login_required  # Garante que o usuário esteja logado
@user_passes_test(admin_check)  # Garante que o usuário seja um administrador
def adicionar_produto(request):
    nome = request.GET.get('nome', '')
    descricao = request.GET.get('descricao', '')
    imagem = request.GET.get('imagem', '')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            if imagem:
                try:
                    # Fazer o download da imagem
                    response = requests.get(imagem)
                    image_name = urlparse(imagem).path.split('/')[-1]
                    form.instance.imagem.save(image_name, ContentFile(response.content), save=False)
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao baixar a imagem: {e}")
            form.save()
            return redirect('produtos:listar_produtos')  # Redireciona para a lista de produtos
    else:
        form = ProdutoForm(initial={
            'nome': nome,
            'descricao': descricao,
            'imagem': imagem,
        })
    return render(request, 'produtos/adicionar.html', {'form': form})
def preencher_form(request):
    api_url = "https://noteb.com/api/webservice.php"
    api_key = "112233aabbcc"  # Substitua pela sua API Key

    # Recuperar o parâmetro de pesquisa
    model_id = request.GET.get('model_id', '')  # Padrão vazio se não houver valor

    if not model_id:
        return JsonResponse({'error': 'Model ID não fornecido'}, status=400)

    try:
        response = requests.post(api_url, data={
            'apikey': api_key,
            'method': "get_model_info",
            'param[model_id]': model_id,
        })

        if response.status_code != 200:
            return JsonResponse({'error': 'Erro na requisição à API'}, status=500)

        data = response.json()

        if data.get("code") != 26 or not data.get("result"):
            return JsonResponse({'error': 'Nenhum dado encontrado na API'}, status=404)

        # Verificar e acessar os dados corretamente
        result = data.get("result", {}).get("0")
        if not result:
            return JsonResponse({'error': '"result" não está no formato esperado'}, status=500)

        # Acessar `model_info` como uma lista
        model_info_list = result.get("model_info", [])
        if not model_info_list or not isinstance(model_info_list, list):
            return JsonResponse({'error': 'model_info não está no formato esperado'}, status=500)

        # Usar o primeiro elemento da lista
        model_info = model_info_list[0]

        # Extração dos dados
        nome = model_info.get("name", "Desconhecido")
        imagem = result.get("model_resources", {}).get("thumbnail", "")
        descricao = formatar_descricao(result)

        # Redirecionar para a página de adicionar produto
        return redirect(f'/produtos/adicionar/?nome={nome}&descricao={descricao}&imagem={imagem}')

    except requests.RequestException as e:
        return JsonResponse({'error': f'Erro ao acessar a API: {e}'}, status=500)
    except KeyError as e:
        return JsonResponse({'error': f'Erro no formato dos dados retornados: {e}'}, status=500)

def formatar_descricao(model_data):
    """Formatar os detalhes do JSON em um texto legível."""
    detalhes = []

    # CPU
    cpu = model_data.get("cpu", {})
    detalhes.append(f"CPU: {cpu.get('prod', '')} {cpu.get('model', '')}, {cpu.get('cores', '')} núcleos, "
                    f"Base: {cpu.get('base_speed', '')} MHz, Boost: {cpu.get('boost_speed', '')} MHz, Cache: {cpu.get('cache', '')} MB")

    # Display
    display = model_data.get("display", {})
    detalhes.append(f"Display: {display.get('size', '')}\" {display.get('type', '')}, Resolução: "
                    f"{display.get('horizontal_resolution', '')}x{display.get('vertical_resolution', '')}, Touch: {display.get('touch', '')}")

    # Memory
    memory = model_data.get("memory", {})
    detalhes.append(f"Memória: {memory.get('size', '')} GB {memory.get('type', '')} {memory.get('speed', '')} MHz")

    # Primary Storage
    storage = model_data.get("primary_storage", {})
    detalhes.append(f"Armazenamento: {storage.get('model', '')}, Capacidade: {storage.get('cap', '')} GB")

    # GPU
    gpu = model_data.get("gpu", {})
    detalhes.append(f"GPU: {gpu.get('prod', '')} {gpu.get('model', '')}, Base: {gpu.get('base_speed', '')} MHz, "
                    f"Boost: {gpu.get('boost_speed', '')} MHz, Tipo de Memória: {gpu.get('memory_type', '')}")

    # Outros detalhes podem ser adicionados aqui...

    return "\n".join(detalhes)
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos:listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar.html', {'form': form, 'produto': produto})

# Remover produto (somente administradores podem remover)
@login_required  # Garante que o usuário esteja logado
@user_passes_test(admin_check)  # Garante que o usuário seja um administrador
def remover_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if produto.imagem:
        # Caminho completo do arquivo de imagem
        imagem_path = os.path.join(settings.MEDIA_ROOT, produto.imagem.name)
        
        # Exclui o arquivo de imagem se existir
        if os.path.isfile(imagem_path):
            os.remove(imagem_path)
    produto.delete()
    return redirect('produtos:listar_produtos')

# Cadastro de usuário
def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Cria o usuário
            login(request, user)  # Faz o login automático do usuário recém-criado
            return redirect('listar_produtos')  # Redireciona para a página principal (produtos)
    else:
        form = UserCreationForm()  # Formulário vazio

    return render(request, 'produtos/cadastro.html', {'form': form})

def listar_produtos(request):
    produtos = Produto.objects.all()  # Todos os produtos
    print(produtos)  # Isso imprimirá os produtos no terminal
    return render(request, 'produtos/listar.html', {'produtos': produtos})

def listar_modelos(request):
    api_url = "https://noteb.com/api/webservice.php"
    api_key = "112233aabbcc"  # Substitua pela sua API Key

    # Recuperar o parâmetro de pesquisa
    model_name = request.GET.get('model_name', '')  # Padrão vazio se não houver valor

    # Enviar requisição para a API
    response = requests.post(api_url, data={
        'apikey': api_key,
        'method': "list_models",
        'param[model_name]': model_name,  # Enviar o parâmetro de pesquisa
    })

    if response.status_code == 200:
        try:
            data = response.json()
            # Extrair apenas a lista de modelos do campo "result"
            modelos = []
            for key, value in data.get("result", {}).items():
                if "model_info" in value:
                    for info in value["model_info"]:
                        modelos.append({
                            "id": info["id"],
                            "name": info["name"],
                            "thumbnail": value["model_resources"].get("thumbnail"),
                            "launch_date": value["model_resources"].get("launch_date"),
                            "official_link": value["model_resources"].get("official_link"),
                        })
        except ValueError:
            modelos = []  # Caso haja erro no parsing do JSON

        # Enviar os modelos e o termo de pesquisa para o template
        return render(request, 'produtos/listar_modelos.html', {'modelos': modelos, 'search_term': model_name})
    else:
        return render(request, 'produtos/listar_modelos.html', {'error': "Erro ao obter os modelos da API.", 'search_term': model_name})
    
@login_required(login_url='/cadastro/')  # Redireciona para a página de cadastro
def alugar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if not produto.disponivel:
        return HttpResponseForbidden("Este produto não está disponível para aluguel.")

    if request.method == "POST":
        form = AlugarProdutoForm(request.POST)
        if form.is_valid():
            meses = form.cleaned_data['meses']

            # Salva os dados do aluguel no banco
            Aluguel.objects.create(
                usuario=request.user,  # Usuário autenticado
                notebook=produto,  # Produto sendo alugado
                meses=meses,  # Quantidade de meses do aluguel
            )

            # Atualiza o estoque do produto
            produto.estoque -= 1
            produto.disponivel = produto.estoque > 0
            produto.save()

            return redirect('listar_produtos')  # Redireciona após o aluguel
    else:
        form = AlugarProdutoForm()

    return render(request, 'produtos/alugar.html', {'produto': produto, 'form': form})
def listar_produtos(request):
    if request.user.is_authenticated and request.user.is_superuser:
        produtos = Produto.objects.all()  # Exibe todos os produtos, incluindo os indisponíveis
    else:
        produtos = Produto.objects.filter(disponivel=True)  # Exibe apenas produtos disponíveis

    return render(request, 'produtos/listar.html', {
        'produtos': produtos
    })