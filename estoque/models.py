from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('F', 'Funcionário'),
        ('G', 'Gerente'),
    ]
    tipo_usuario = models.CharField(
        max_length=1, 
        choices=TIPO_USUARIO_CHOICES,
        default='F',  # Valor padrão como Funcionário
    )
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    # Sobrescrevendo campos do AbstractUser para evitar conflitos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',
        related_query_name='usuario'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario'
    )
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.username

class Produto(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=100)
    nota_fiscal = models.CharField(max_length=50)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.nome