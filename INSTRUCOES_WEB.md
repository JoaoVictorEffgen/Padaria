# 🚀 Instruções Rápidas - Site Web da Padaria

## ⚡ Início Rápido

### 1. Iniciar o Site
```bash
python run_web.py
```

### 2. Acessar no Navegador
- **Site**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. Testar Funcionamento
```bash
python test_web.py
```

## 📱 Como Usar o Site

### Para Clientes:
1. **Acesse o site** em http://localhost:8000
2. **Navegue pelo cardápio** usando os filtros de categoria
3. **Adicione produtos** ao carrinho clicando em "Adicionar"
4. **Ajuste quantidades** usando os botões + e -
5. **Finalize o pedido** clicando no carrinho e depois "Finalizar Pedido"
6. **O WhatsApp abrirá** com a mensagem do pedido formatada

### Para Administradores:
1. **Use o sistema desktop** para cadastrar produtos:
   ```bash
   python run_desktop.py
   ```
2. **Vá para a aba "Produtos"**
3. **Cadastre novos produtos** com nome, preço e categoria
4. **Os produtos aparecerão automaticamente** no site

## ⚙️ Configurações Importantes

### WhatsApp
Edite `backend/app/config_whatsapp.py`:
```python
"phone_number": "5511999999999"  # Seu número real
```

### Pedido Mínimo e Taxa de Entrega
Edite `backend/app/static/js/app.js`:
```javascript
DELIVERY_FEE: 5.00,      // Taxa de entrega
MINIMUM_ORDER: 15.00     // Pedido mínimo
```

## 🎨 Personalização

### Cores do Site
Edite `backend/app/static/css/style.css`:
```css
--primary-color: #e67e22;    /* Cor principal */
--secondary-color: #f39c12;  /* Cor secundária */
--accent-color: #25d366;     /* Cor do WhatsApp */
```

### Imagens
Substitua as imagens em `backend/app/static/images/`:
- `hero-bread.jpg` - Imagem principal
- `about-bakery.jpg` - Imagem da seção sobre

## 📞 Funcionalidades WhatsApp

### Pedidos Automáticos
- Mensagem pré-formatada com todos os itens
- Cálculo automático de totais
- Inclusão de taxa de entrega
- Solicitação de dados do cliente

### Mensagens Padrão
- Boas-vindas automáticas
- Informações de horário
- Cardápio completo
- Status de pedidos

## 🔧 Solução de Problemas

### Site não carrega
1. Verifique se o servidor está rodando: `python run_web.py`
2. Teste a conexão: `python test_web.py`
3. Verifique a porta 8000 não está em uso

### Produtos não aparecem
1. Use o sistema desktop para cadastrar produtos
2. Verifique se os produtos estão marcados como "disponível"
3. Recarregue a página do site

### WhatsApp não funciona
1. Verifique o número no arquivo de configuração
2. Teste o link manualmente: `https://wa.me/5511999999999`
3. Certifique-se de que o número está no formato correto

### Erro de CSS/JavaScript
1. Verifique se os arquivos estão em `backend/app/static/`
2. Limpe o cache do navegador
3. Verifique o console do navegador (F12)

## 📊 Monitoramento

### Logs do Servidor
O servidor mostra logs em tempo real:
- Requisições recebidas
- Erros de API
- Status de conexão

### Teste Automático
Execute `python test_web.py` para verificar:
- Página principal
- API de produtos
- Arquivos estáticos
- JavaScript

## 🚀 Deploy para Produção

### 1. Configurar Servidor
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### 2. Configurar Nginx
```nginx
server {
    listen 80;
    server_name sua-padaria.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### 3. Configurar HTTPS
- Use Let's Encrypt para certificado SSL
- Configure redirecionamento HTTP → HTTPS

## 📞 Suporte

### Comandos Úteis
```bash
# Iniciar servidor
python run_web.py

# Testar funcionamento
python test_web.py

# Sistema desktop (para cadastrar produtos)
python run_desktop.py

# Ver logs em tempo real
tail -f logs/app.log
```

### Verificações Rápidas
- ✅ Servidor rodando na porta 8000
- ✅ Banco de dados conectado
- ✅ Produtos cadastrados
- ✅ WhatsApp configurado
- ✅ Arquivos estáticos carregando

## 🎯 Próximos Passos

1. **Personalize as cores** e imagens
2. **Configure o WhatsApp** com seu número
3. **Cadastre produtos** usando o sistema desktop
4. **Teste o fluxo completo** de pedido
5. **Configure para produção** se necessário

---

**🎉 Seu site da padaria está pronto para uso!** 