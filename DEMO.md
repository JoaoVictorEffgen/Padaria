# Demonstração do Sistema Padaria

## 🎯 Visão Geral

Este sistema completo para padaria inclui:
- **Backend API** (FastAPI + SQLite)
- **Sistema Desktop** (PyQt5) para caixa/gerência
- **App Tablet** (Flutter) para mesas

## 🚀 Início Rápido

### 1. Inicialização Completa
```bash
python start_system.py
```

### 2. Inicialização Manual
```bash
# Terminal 1 - Backend
python run_backend.py

# Terminal 2 - Desktop
python run_desktop.py

# Terminal 3 - Tablet (se Flutter instalado)
cd tablet
flutter run
```

## 📋 Fluxo de Demonstração

### Cenário: Mesa 4 faz pedido

#### 1. Preparação (Sistema Desktop)
1. Abrir sistema desktop
2. Ir para aba "Mesas"
3. Clicar "Abrir Comanda" na Mesa 4
4. Verificar que mesa fica "ocupada"

#### 2. Pedido do Cliente (Tablet)
1. Abrir app no tablet
2. Clicar "Abrir Comanda"
3. Selecionar categoria "Pães"
4. Tocar em "Pão Francês" (adiciona à comanda)
5. Selecionar categoria "Cafés"
6. Tocar em "Café Expresso" (adiciona à comanda)
7. Ver total atualizado: R$ 4,00

#### 3. Acompanhamento (Sistema Desktop)
1. Na aba "Comandas", ver comanda da Mesa 4
2. Clicar na comanda para ver detalhes
3. Ver itens: Pão Francês (R$ 0,50) + Café Expresso (R$ 3,50)
4. Total: R$ 4,00

#### 4. Finalização
1. No tablet: Clicar "Fechar Comanda"
2. No desktop: Comanda muda para "Aguardando pagamento"
3. No desktop: Clicar "Finalizar Pagamento"
4. Mesa 4 fica livre novamente

## 🎮 Funcionalidades para Testar

### Sistema Desktop

#### Cadastro de Produtos
- Aba "Produtos"
- Preencher: Nome, Preço, Categoria, Descrição
- Clicar "Cadastrar Produto"

#### Gerenciamento de Mesas
- Aba "Mesas"
- Ver status: livre/ocupada
- Abrir comandas para mesas livres

#### Visualização de Comandas
- Aba "Comandas"
- Ver comandas ativas em tempo real
- Detalhes: mesa, status, total, itens

#### Relatórios
- Aba "Relatórios"
- Estatísticas: total comandas, faturamento
- Histórico de comandas

### App Tablet

#### Interface por Categorias
- Filtros: Todas, Pães, Bebidas, Cafés, Doces, Salgados
- Cards de produtos com preço e descrição

#### Gestão de Comanda
- Abrir comanda automaticamente
- Adicionar produtos com toque
- Ver total em tempo real
- Quantidade de cada produto no card

#### Comunicação
- Botão "Chamar Garçom"
- Botão "Fechar Comanda"

## 🔧 Configurações de Teste

### Dados Iniciais
O sistema vem com:
- 5 mesas (1-5)
- 10 produtos em 5 categorias
- Preços de R$ 0,50 a R$ 6,00

### Produtos de Exemplo
- **Pães**: Pão Francês, Pão de Queijo, Croissant
- **Cafés**: Expresso, Cappuccino
- **Bebidas**: Coca-Cola, Suco de Laranja
- **Doces**: Brigadeiro
- **Salgados**: Pastel de Carne, Coxinha

## 🌐 Configuração de Rede

### Para Teste Local
- Backend: http://localhost:8000
- Desktop: Conecta automaticamente
- Tablet: Editar `tablet/lib/services/api_service.dart`

### Para Teste em Rede
1. Descobrir IP da máquina:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. Atualizar IP no tablet:
   ```dart
   static const String baseUrl = 'http://SEU_IP:8000';
   ```

3. Verificar conectividade:
   - Mesma rede Wi-Fi
   - Firewall permite porta 8000

## 📊 Endpoints da API

### Teste via Navegador
- Documentação: http://localhost:8000/docs
- Produtos: http://localhost:8000/produtos/
- Comandas: http://localhost:8000/comandas/
- Mesas: http://localhost:8000/mesas/

### Teste via curl
```bash
# Listar produtos
curl http://localhost:8000/produtos/

# Criar comanda
curl -X POST http://localhost:8000/comandas/ \
  -H "Content-Type: application/json" \
  -d '{"mesa_id": 1}'

# Adicionar item
curl -X POST http://localhost:8000/comandas/1/itens/ \
  -H "Content-Type: application/json" \
  -d '{"produto_id": 1, "quantidade": 2, "preco_unitario": 0.50}'
```

## 🐛 Solução de Problemas

### Backend não inicia
- Verificar Python 3.8+
- Verificar porta 8000 livre
- Verificar dependências instaladas

### Desktop não conecta
- Verificar backend rodando
- Verificar URL da API
- Verificar firewall

### Tablet não conecta
- Verificar IP correto
- Verificar rede Wi-Fi
- Verificar backend aceita conexões externas

### Erro de banco
- Executar `python setup_database.py`
- Verificar permissões de escrita

## 🎯 Próximos Passos

### Melhorias Sugeridas
1. **Notificações em tempo real** (WebSockets)
2. **Sistema de usuários** (login/logout)
3. **Relatórios avançados** (gráficos, exportação)
4. **Integração com impressora** (comandas físicas)
5. **Backup automático** do banco
6. **Sistema de pagamentos** (PIX, cartão)

### Personalização
- Adicionar mais categorias de produtos
- Modificar design das interfaces
- Implementar sistema de promoções
- Adicionar controle de estoque

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs do backend
2. Consultar documentação da API
3. Verificar conectividade de rede
4. Testar endpoints individualmente 