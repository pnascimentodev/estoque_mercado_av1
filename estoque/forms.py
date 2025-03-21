from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Produto, Usuario

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['codigo', 'nome', 'nota_fiscal', 'quantidade']
        labels = {
            'codigo': 'Código do Produto',
            'nome': 'Nome do Produto',
            'nota_fiscal': 'Número da Nota Fiscal',
            'quantidade': 'Quantidade'
        }

class UsuarioForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(
        choices=[('F', 'Funcionário'), ('G', 'Gerente')],
        label='Tipo de Usuário',
        widget=forms.RadioSelect
    )

    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'tipo_usuario']
        labels = {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirmar senha',
            'tipo_usuario': 'Tipo de Usuário'
        }
