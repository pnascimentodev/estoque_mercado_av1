from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Produto, Usuario
from .forms import ProdutoForm, UsuarioForm
import pandas as pd
from django.http import HttpResponse

def is_gerente(user):
    return user.is_authenticated and user.tipo_usuario == 'G'

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug para verificar os dados recebidos
        print(f"Tentativa de login - Username: {username}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"Login bem sucedido - Tipo de usuário: {user.tipo_usuario}")
            if user.tipo_usuario == 'F':
                return redirect('cadastrar_produto')
            elif user.tipo_usuario == 'G':
                return redirect('dashboard')
        else:
            print("Falha no login - Usuário não autenticado")
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(is_gerente, login_url='login')
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('dashboard')
    else:
        form = UsuarioForm()
    return render(request, 'registrar_usuario.html', {'form': form})

@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            # Salva o novo registro do produto
            novo_produto = form.save()
            
            # Atualiza a quantidade total no dashboard
            produtos_mesmo_codigo = Produto.objects.filter(codigo=novo_produto.codigo)
            quantidade_total = sum(p.quantidade for p in produtos_mesmo_codigo)
            
            messages.success(
                request, 
                f'Produto registrado com sucesso! Quantidade total em estoque: {quantidade_total}'
            )
            return redirect('cadastrar_produto')
    else:
        form = ProdutoForm()
    return render(request, 'cadastrar_produto.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.tipo_usuario != 'G':
        return redirect('login')
    
    # Agrupa produtos pelo código e soma as quantidades
    produtos_agrupados = {}
    for produto in Produto.objects.all():
        if produto.codigo not in produtos_agrupados:
            produtos_agrupados[produto.codigo] = {
                'nome': produto.nome,
                'quantidade': produto.quantidade,
                'pk': produto.pk
            }
        else:
            produtos_agrupados[produto.codigo]['quantidade'] += produto.quantidade
    
    # Converte o dicionário em lista para o template
    produtos = [
        {
            'nome': info['nome'],
            'quantidade': info['quantidade'],
            'pk': info['pk']
        }
        for info in produtos_agrupados.values()
    ]
    
    return render(request, 'dashboard.html', {'produtos': produtos})

@login_required
@user_passes_test(is_gerente, login_url='login')
def editar_produto(request, pk):
    produto_referencia = get_object_or_404(Produto, pk=pk)
    
    # Obtém todos os registros do mesmo produto e calcula o total
    produtos_mesmo_codigo = Produto.objects.filter(codigo=produto_referencia.codigo)
    quantidade_total = sum(p.quantidade for p in produtos_mesmo_codigo)
    
    if request.method == 'POST':
        quantidade = request.POST.get('quantidade')
        if quantidade is not None:
            try:
                nova_quantidade = int(quantidade)
                if nova_quantidade >= 0:
                    # Calcula a diferença entre a nova quantidade e o total atual
                    diferenca = nova_quantidade - quantidade_total
                    
                    # Atualiza o registro mais recente com a diferença
                    ultimo_registro = produtos_mesmo_codigo.latest('id')
                    ultimo_registro.quantidade += diferenca
                    ultimo_registro.save()
                    
                    messages.success(request, f'Quantidade atualizada com sucesso para {nova_quantidade}')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'A quantidade não pode ser negativa')
            except ValueError:
                messages.error(request, 'A quantidade deve ser um número válido')
    
    # Passa o produto de referência e a quantidade total para o template
    return render(request, 'editar_produto.html', {
        'produto': produto_referencia,
        'quantidade_total': quantidade_total
    })

@login_required
@user_passes_test(is_gerente, login_url='login')
def exportar_estoque(request):
    # Agrupa produtos pelo código
    produtos_agrupados = {}
    for produto in Produto.objects.all():
        if produto.codigo not in produtos_agrupados:
            produtos_agrupados[produto.codigo] = {
                'codigo': produto.codigo,
                'nome': produto.nome,
                'notas_fiscais': [produto.nota_fiscal],
                'quantidade': produto.quantidade
            }
        else:
            produtos_agrupados[produto.codigo]['notas_fiscais'].append(produto.nota_fiscal)
            produtos_agrupados[produto.codigo]['quantidade'] += produto.quantidade
    
    # Criar o DataFrame com os dados agrupados
    data = {
        'Código': [info['codigo'] for info in produtos_agrupados.values()],
        'Nome do Produto': [info['nome'] for info in produtos_agrupados.values()],
        'Notas Fiscais': [', '.join(info['notas_fiscais']) for info in produtos_agrupados.values()],
        'Quantidade em Estoque': [info['quantidade'] for info in produtos_agrupados.values()]
    }
    df = pd.DataFrame(data)
    df = df.sort_values('Nome do Produto')
    
    # Configurar a resposta HTTP com o arquivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=estoque.xlsx'
    
    # Salvar o DataFrame como Excel
    df.to_excel(response, index=False, sheet_name='Estoque')
    
    return response