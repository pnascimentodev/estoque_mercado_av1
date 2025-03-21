from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastrar-produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editar-produto/<int:pk>/', views.editar_produto, name='editar_produto'),
    path('exportar-estoque/', views.exportar_estoque, name='exportar_estoque'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
]