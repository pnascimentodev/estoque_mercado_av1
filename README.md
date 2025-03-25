# Sistema de Gerenciamento de Estoque - Supermercado

## Descrição do Projeto
Este projeto foi desenvolvido como parte da disciplina de Engenharia de Software, em grupo. O objetivo principal foi criar uma solução para o problema de gestão de estoque de um supermercado que estava enfrentando desfalques de produtos e necessitava de um sistema eficiente para controle de inventário.

## Funcionalidades
- Cadastro de produtos com código, nome, nota fiscal e quantidade
- Dashboard para visualização do estoque atual
- Sistema de busca de produtos
- Exportação do estoque para planilha Excel
- Controle de acesso com dois níveis de usuário:
  - Gerente: acesso total ao sistema
  - Funcionário: acesso limitado ao cadastro e visualização de produtos

## Requisitos
- Python 3.x
- Django
- Pandas
- Openpyxl

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/pnascimentodev/estoque_mercado_av1.git
cd novo_supermercado
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install django pandas openpyxl
```

4. Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crie um superusuário (administrador):
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

## Como Usar
1. Acesse o sistema através do navegador: `http://localhost:8000`
2. Faça login com suas credenciais
3. Para cadastrar produtos: clique em "Cadastrar Produto"
4. Para visualizar o estoque: acesse o "Dashboard"
5. Para exportar o estoque: clique em "Exportar Estoque" no Dashboard

## Tipos de Usuário
- **Gerente (G)**: 
  - Cadastrar/editar produtos
  - Visualizar dashboard
  - Exportar estoque
  - Registrar novos usuários
- **Funcionário (F)**:
  - Cadastrar produtos
  - Visualizar dashboard

## Tecnologias Utilizadas
- Django (Framework Web)
- SQLite (Banco de Dados)
- HTML/CSS (Frontend)
- Python (Backend)
- Pandas (Manipulação de Dados)

## Observações
Este projeto foi desenvolvido com foco na solução de um problema real de gestão de estoque, aplicando conceitos aprendidos na disciplina de Engenharia de Software, como desenvolvimento ágil, padrões de projeto e boas práticas de programação.

---
Desenvolvido para a disciplina de Engenharia de Software - Uninassau

Alunos:
- Priscila Nascimento
- Pedro Barbosa
- Rayane Mariano
- Henrique Mendes
- Aline Dayane
- Nicolas César
- Adison Alves Barbosa
- Sergio Gabriel
- Samuel Victor 
