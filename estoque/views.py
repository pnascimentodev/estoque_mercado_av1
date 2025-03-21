from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
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
            form.save()
            return redirect('cadastrar_produto')
    else:
        form = ProdutoForm()
    return render(request, 'cadastrar_produto.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.tipo_usuario != 'G':
        return redirect('login')
    produtos = Produto.objects.all()
    return render(request, 'dashboard.html', {'produtos': produtos})

@login_required
@user_passes_test(is_gerente, login_url='login')
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        # Pegar apenas a quantidade do POST
        quantidade = request.POST.get('quantidade')
        if quantidade is not None:
            try:
                quantidade = int(quantidade)
                if quantidade >= 0:
                    produto.quantidade = quantidade
                    produto.save()
                    return redirect('dashboard')
                else:
                    return render(request, 'editar_produto.html', {
                        'produto': produto,
                        'error': 'A quantidade não pode ser negativa'
                    })
            except ValueError:
                return render(request, 'editar_produto.html', {
                    'produto': produto,
                    'error': 'A quantidade deve ser um número válido'
                })
    
    return render(request, 'editar_produto.html', {'produto': produto})

@login_required
@user_passes_test(is_gerente, login_url='login')
def exportar_estoque(request):
    produtos = Produto.objects.all().order_by('nome')
    
    # Criar o DataFrame com os dados dos produtos
    data = {
        'Código': [produto.codigo for produto in produtos],
        'Nome do Produto': [produto.nome for produto in produtos],
        'Nota Fiscal': [produto.nota_fiscal for produto in produtos],
        'Quantidade em Estoque': [produto.quantidade for produto in produtos]
    }
    df = pd.DataFrame(data)
    
    # Configurar a resposta HTTP com o arquivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=estoque.xlsx'
    
    # Salvar o DataFrame como Excel
    df.to_excel(response, index=False, sheet_name='Estoque')
    
    return response