# Recursos Extras - Sistema de Padaria

Este documento descreve os recursos extras implementados no Sistema de Padaria versão 2.0.

## 📋 Índice

1. [Impressão de Comandas](#impressão-de-comandas)
2. [Painel para Garçons](#painel-para-garçons)
3. [Modo Offline](#modo-offline)
4. [QR Code para Menu Público](#qr-code-para-menu-público)
5. [Configuração e Uso](#configuração-e-uso)

---

## 🖨️ Impressão de Comandas

### Funcionalidades

- **Impressão automática**: Comandas são impressas automaticamente na cozinha
- **Múltiplas impressoras**: Suporte a diferentes impressoras
- **Formato personalizado**: Layout otimizado para impressoras térmicas
- **Status de impressão**: Controle de comandas já impressas

### Como Funciona

1. **Detecção automática**: Quando um item é adicionado à comanda
2. **Formatação**: Geração de layout específico para cozinha
3. **Impressão**: Envio para impressora configurada
4. **Controle**: Marcação de comanda como "impressa"

### Configuração

```python
# No desktop, configure a impressora:
from desktop.services.printer_service import PrinterService

printer = PrinterService()
impressoras = printer.listar_impressoras()
printer.definir_impressora_padrao("Impressora_Cozinha")
```

### Exemplo de Comanda Impressa

```
========================================
           PADARIA
========================================
Comanda: #123
Mesa: 5
Data: 2024-01-15 14:30:00
Status: aberta
----------------------------------------
ITENS:
----------------------------------------
Pão Francês
  2x R$ 0.50 = R$ 1.00

Café Expresso
  1x R$ 3.50 = R$ 3.50
  Obs: Sem açúcar

----------------------------------------
TOTAL: R$ 4.50
========================================

Obrigado pela preferência!
Impresso em: 15/01/2024 14:30:15
```

---

## 👨‍💼 Painel para Garçons

### Funcionalidades

- **Visão em tempo real**: Comandas atualizadas automaticamente
- **Filtros inteligentes**: Por status, mesa, tempo
- **Ações rápidas**: Imprimir, entregar, finalizar
- **Estatísticas**: Resumo de comandas por status
- **Notificações**: Alertas para novas comandas

### Interface

```
┌─────────────────────────────────────────────────────────┐
│                    Painel do Garçom                     │
├─────────────────────────────────────────────────────────┤
│ Filtrar por: [Todas ▼] [Atualizar]                      │
├─────────────────────────────────────────────────────────┤
│ Mesa │ Status │ Total │ Itens │ Tempo │ Obs │ Ações │ Det │
├──────┼────────┼───────┼───────┼───────┼─────┼───────┼─────┤
│  5   │ Aberta │ R$4.50│   2   │ 5 min │     │[I][E] │ [D] │
│  8   │ Aguard │ R$12.0│   3   │ 15min │     │   [F] │ [D] │
└──────┴────────┴───────┴───────┴───────┴─────┴───────┴─────┘
│ Total: 2 │ Abertas: 1 │ Para Impressão: 1 │ Aguardando: 1 │
└─────────────────────────────────────────────────────────┘
```

### Ações Disponíveis

- **[I] Imprimir**: Marca comanda como impressa
- **[E] Entregar**: Registra entrega do pedido
- **[F] Finalizar**: Conclui pagamento
- **[D] Detalhes**: Mostra informações completas

### Configuração

```python
# Acesse o painel no desktop:
# Aba "Garçons" no sistema principal
```

---

## 📱 Modo Offline

### Funcionalidades

- **Funcionamento offline**: Tablet funciona sem internet
- **Cache local**: Produtos e comandas salvos localmente
- **Sincronização automática**: Dados enviados quando online
- **Operações pendentes**: Fila de ações para sincronizar
- **Detecção de conectividade**: Verificação automática

### Como Funciona

1. **Cache inicial**: Baixa produtos quando online
2. **Operações offline**: Salva ações localmente
3. **Detecção online**: Verifica conectividade periodicamente
4. **Sincronização**: Envia operações pendentes
5. **Confirmação**: Marca operações como sincronizadas

### Estrutura de Dados

```dart
// Cache local
{
  "produtos_cache": [...],
  "comanda_cache": {...},
  "pending_operations": [
    {
      "id": "1234567890",
      "tipo": "create",
      "tabela": "itens_comanda",
      "dados": {...},
      "timestamp": "2024-01-15T14:30:00Z"
    }
  ]
}
```

### Operações Offline

- ✅ Adicionar itens à comanda
- ✅ Fechar comanda
- ✅ Chamar garçom
- ✅ Visualizar produtos
- ✅ Ver histórico local

### Sincronização

```dart
// Verificar conectividade
bool isOnline = await OfflineService().isOnline();

// Sincronizar operações pendentes
bool success = await OfflineService().syncPendingOperations();
```

---

## 📱 QR Code para Menu Público

### Funcionalidades

- **QR Code único**: Cada mesa tem seu próprio código
- **Menu público**: Acessível sem comanda aberta
- **Interface responsiva**: Funciona em qualquer dispositivo
- **Categorização**: Produtos organizados por categoria
- **Informações detalhadas**: Preços, descrições, imagens

### Como Funciona

1. **Geração**: QR Code criado automaticamente para cada mesa
2. **Acesso**: Cliente escaneia com smartphone
3. **Menu**: Visualiza produtos disponíveis
4. **Interação**: Pode chamar garçom ou abrir comanda

### URL do QR Code

```
http://localhost:8000/mesas/1/qr-code
```

### Menu Público

```
http://localhost:8000/menu/1
```

### Interface do Menu

```
┌─────────────────────────────────────┐
│           Bem-vindo à Padaria!      │
│              Mesa 5                 │
│  Escolha seus produtos e abra uma   │
│      comanda para fazer seu pedido  │
├─────────────────────────────────────┤
│ [Todas] [Pães] [Cafés] [Bebidas]    │
├─────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐     │
│ │ Pão Francês │ │ Pão Queijo  │     │
│ │   R$ 0,50   │ │   R$ 2,50   │     │
│ └─────────────┘ └─────────────┘     │
│ ┌─────────────┐ ┌─────────────┐     │
│ │  Croissant  │ │Café Expresso│     │
│ │   R$ 4,00   │ │   R$ 3,50   │     │
│ └─────────────┘ └─────────────┘     │
├─────────────────────────────────────┤
│        [Abrir Comanda]              │
└─────────────────────────────────────┘
```

### Implementação

```python
# Backend - Geração do QR Code
@app.get("/mesas/{mesa_id}/qr-code")
def gerar_qr_code_mesa(mesa_id: int):
    menu_url = f"{BASE_URL}/menu/{mesa_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(menu_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    # Retorna imagem em base64
```

---

## ⚙️ Configuração e Uso

### Pré-requisitos

1. **Python 3.8+**: Para backend e desktop
2. **Flutter**: Para aplicativo tablet
3. **Impressora**: Para impressão de comandas
4. **Rede local**: Para comunicação entre dispositivos

### Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd ProjetoPadaria

# 2. Execute o script de inicialização
python start_system.py
```

### Configuração de Impressora

```python
# No desktop, acesse:
# Configurações > Impressora

# Ou via código:
from desktop.services.printer_service import PrinterService

printer = PrinterService()
impressoras = printer.listar_impressoras()
print("Impressoras disponíveis:", impressoras)
```

### Configuração de Rede

```bash
# 1. Descubra seu IP local
ipconfig  # Windows
ifconfig  # Linux/Mac

# 2. Configure no tablet
# Edite: tablet/lib/services/api_service.dart
# Altere: baseUrl = 'http://SEU_IP:8000'
```

### Uso dos Recursos

#### Impressão
1. Abra uma comanda no desktop
2. Adicione itens
3. Comanda é impressa automaticamente
4. Verifique status no painel de garçons

#### Painel de Garçons
1. Acesse aba "Garçons" no desktop
2. Visualize comandas em tempo real
3. Use filtros para organizar
4. Execute ações conforme necessário

#### Modo Offline
1. Configure tablet com dados iniciais
2. Use normalmente (funciona offline)
3. Sincronização automática quando online
4. Verifique operações pendentes

#### QR Code
1. Acesse: http://localhost:8000/mesas/1/qr-code
2. Imprima ou exiba na mesa
3. Clientes escaneiam com smartphone
4. Visualizam menu público

### Troubleshooting

#### Impressão não funciona
- Verifique se a impressora está conectada
- Teste com impressora padrão do sistema
- Use modo "console" para debug

#### Painel não atualiza
- Verifique conexão com backend
- Reinicie aplicação desktop
- Verifique logs de erro

#### Tablet offline não sincroniza
- Verifique conectividade de rede
- Force sincronização manual
- Limpe cache se necessário

#### QR Code não gera
- Verifique se a mesa existe
- Teste endpoint diretamente
- Verifique logs do backend

### Logs e Debug

```bash
# Backend logs
tail -f backend.log

# Desktop logs
# Verifique console da aplicação

# Tablet logs
flutter logs
```

### Backup e Restore

```bash
# Backup do banco
cp padaria.db backup/padaria_$(date +%Y%m%d).db

# Restore
cp backup/padaria_20240115.db padaria.db
```

---

## 🚀 Próximas Melhorias

### Planejadas
- [ ] Notificações push para garçons
- [ ] Integração com sistemas de pagamento
- [ ] Relatórios avançados
- [ ] Backup automático na nuvem
- [ ] Interface web para administração

### Sugestões
- [ ] Integração com delivery
- [ ] Sistema de fidelidade
- [ ] Controle de estoque
- [ ] Integração com fornecedores
- [ ] App para clientes

---

## 📞 Suporte

Para dúvidas ou problemas:

1. **Documentação**: README.md, DEMO.md
2. **Issues**: Abra uma issue no repositório
3. **Logs**: Verifique logs de erro
4. **Testes**: Execute testes unitários

---

**Sistema de Padaria v2.0** - Recursos Extras Implementados ✅ 