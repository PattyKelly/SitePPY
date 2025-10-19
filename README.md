# SitePPY - Sistema de Acesso Personal

Sistema web de autenticação e acesso personal desenvolvido com Flask.

## Funcionalidades

- 🔒 Sistema de autenticação seguro
- 👤 Acesso personalizado para usuários
- 📊 Dashboard personalizado
- 🎨 Interface moderna e responsiva
- ⚡ Rápido e fácil de usar

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/PattyKelly/SitePPY.git
cd SitePPY
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Inicie o servidor:
```bash
python app.py
```

2. Acesse no navegador:
```
http://localhost:5000
```

3. Use as credenciais de demonstração:
   - **Admin**: usuário: `admin`, senha: `admin123`
   - **Usuário**: usuário: `user`, senha: `user123`

## Estrutura do Projeto

```
SitePPY/
├── app.py              # Aplicação principal Flask
├── requirements.txt    # Dependências Python
├── templates/          # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── dashboard.html
└── static/            # Arquivos estáticos
    └── css/
        └── style.css  # Estilos CSS
```

## Tecnologias Utilizadas

- **Flask**: Framework web Python
- **Flask-Login**: Gerenciamento de sessões de usuário
- **Werkzeug**: Utilitários WSGI e hash de senhas
- **HTML/CSS**: Interface do usuário

## Segurança

- Senhas são armazenadas com hash seguro usando Werkzeug
- Sistema de sessões com Flask-Login
- Proteção de rotas com decorador @login_required
- Chave secreta para sessões (altere em produção!)

## Aviso de Segurança

⚠️ Este é um projeto de demonstração. Para uso em produção:
1. Altere a `SECRET_KEY` no arquivo `app.py`
2. Use um banco de dados real (PostgreSQL, MySQL, etc.)
3. Implemente validações adicionais
4. Use HTTPS
5. Adicione rate limiting
6. Implemente recuperação de senha

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.