# 🌐 Site Web da Padaria Delícias

## 📋 Visão Geral

O site web da Padaria Delícias é uma plataforma moderna e responsiva que permite aos clientes:

- **Visualizar o cardápio** completo da padaria
- **Fazer pedidos online** com carrinho de compras
- **Integração direta com WhatsApp** para finalização de pedidos
- **Sistema de entrega** com cálculo automático de taxas
- **Interface responsiva** para desktop, tablet e mobile

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Iniciar o Servidor Web
```bash
python run_web.py
```

### 3. Acessar o Site
- **Site principal**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## 🎨 Funcionalidades

### 📱 Interface Responsiva
- Design moderno e intuitivo
- Adaptação automática para diferentes tamanhos de tela
- Navegação suave e animações fluidas

### 🛒 Carrinho de Compras
- Adicionar/remover produtos
- Controle de quantidades
- Cálculo automático de totais
- Persistência local (localStorage)

### 📞 Integração WhatsApp
- Botão direto para WhatsApp
- Mensagem pré-formatada com pedido
- Cálculo automático de taxas de entrega
- Validação de pedido mínimo

### 🍞 Sistema de Produtos
- Filtros por categoria
- Busca dinâmica
- Imagens e descrições
- Preços atualizados

## ⚙️ Configurações

### WhatsApp
Edite o arquivo `backend/app/config_whatsapp.py`:

```python
WHATSAPP_CONFIG = {
    "phone_number": "5511999999999",  # Seu número do WhatsApp
    "delivery_info": {
        "minimum_order": 15.00,       # Pedido mínimo
        "delivery_fee": 5.00,         # Taxa de entrega
        "delivery_time": "30-45 minutos"
    }
}
```

### Frontend
Edite o arquivo `backend/app/static/js/app.js`:

```javascript
const CONFIG = {
    WHATSAPP_NUMBER: '5511999999999',  // Seu número
    DELIVERY_FEE: 5.00,                // Taxa de entrega
    MINIMUM_ORDER: 15.00               // Pedido mínimo
};
```

## 📁 Estrutura de Arquivos

```
backend/app/static/
├── index.html          # Página principal
├── css/
│   └── style.css       # Estilos CSS
├── js/
│   └── app.js          # JavaScript da aplicação
└── images/             # Imagens do site
    ├── hero-bread.jpg
    ├── about-bakery.jpg
    └── favicon.ico
```

## 🎯 Funcionalidades Principais

### 1. Página Inicial (Hero Section)
- Apresentação da padaria
- Botões de ação (Ver Cardápio / WhatsApp)
- Design atrativo com gradientes

### 2. Seção de Produtos
- Grid responsivo de produtos
- Filtros por categoria
- Controles de quantidade
- Adição ao carrinho

### 3. Carrinho Lateral
- Lista de produtos selecionados
- Controles de quantidade
- Cálculo de totais
- Botão de finalização

### 4. Seção Sobre
- Informações da padaria
- Horário de funcionamento
- Diferenciais do negócio

### 5. Seção Contato
- Informações de contato
- Formulário de mensagem
- Links para redes sociais

## 🔧 Personalização

### Cores e Estilo
Edite `backend/app/static/css/style.css`:

```css
:root {
    --primary-color: #e67e22;
    --secondary-color: #f39c12;
    --accent-color: #25d366;
}
```

### Produtos
Os produtos são carregados automaticamente da API. Para adicionar produtos:

1. Use o sistema desktop: `python run_desktop.py`
2. Vá para a aba "Produtos"
3. Cadastre novos produtos
4. Eles aparecerão automaticamente no site

### Imagens
Substitua as imagens em `backend/app/static/images/`:
- `hero-bread.jpg` - Imagem principal
- `about-bakery.jpg` - Imagem da seção sobre
- `favicon.ico` - Ícone do site

## 📱 Responsividade

O site é totalmente responsivo e funciona em:

- **Desktop** (1200px+)
- **Tablet** (768px - 1199px)
- **Mobile** (até 767px)

### Breakpoints
```css
@media (max-width: 768px) {
    /* Estilos para tablet */
}

@media (max-width: 480px) {
    /* Estilos para mobile */
}
```

## 🔒 Segurança

- Validação de formulários no frontend
- Sanitização de dados
- HTTPS recomendado para produção
- Validação de pedido mínimo

## 🚀 Deploy

### Para Produção
1. Configure um servidor web (nginx/apache)
2. Use um servidor WSGI (gunicorn)
3. Configure HTTPS
4. Atualize as URLs da API

### Exemplo com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique os logs do servidor
- Teste a API em `/docs`
- Verifique a conexão com o banco de dados

## 🎉 Próximas Funcionalidades

- [ ] Sistema de login para clientes
- [ ] Histórico de pedidos
- [ ] Avaliações e comentários
- [ ] Sistema de cupons de desconto
- [ ] Integração com pagamentos online
- [ ] Chat em tempo real
- [ ] Notificações push
- [ ] App mobile nativo 