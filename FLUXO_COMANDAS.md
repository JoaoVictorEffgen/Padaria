# 🔄 Fluxo de Comandas - Sistema de Padaria

## 📱 **Mobile/Tablet (Cliente)**

### **Fluxo de Abertura**
1. Cliente seleciona mesa
2. Clica em "Abrir Comanda"
3. Sistema cria comanda com status `"aberta"`
4. Cliente pode adicionar produtos
5. Cliente pode chamar garçom

### **Fluxo de Fechamento**
1. **Cliente NÃO fecha a comanda diretamente**
2. Cliente clica em "Solicitar Fechamento"
3. Sistema muda status para `"aguardando_pagamento"`
4. **Comanda é enviada para o caixa (desktop)**
5. Mobile mostra "Aguardando Pagamento"
6. Botão fica desabilitado com texto "Aguardando Pagamento"

### **Detecção Automática de Finalização**
- Sistema verifica status a cada 5 segundos
- Quando desktop finaliza comanda (status = `"fechada"`)
- Mobile detecta automaticamente
- Mostra tela "Comanda Finalizada!"
- Cliente pode abrir nova comanda

---

## 💻 **Desktop (Caixa/Funcionário)**

### **Gestão de Comandas**
1. Visualiza todas as comandas
2. Identifica comandas com status `"aguardando_pagamento"`
3. Processa pagamento
4. Finaliza comanda (status = `"fechada"`)

### **Finalização**
1. Funcionário clica em "Finalizar" na comanda
2. Sistema muda status para `"fechada"`
3. **Mobile detecta automaticamente em 5 segundos**
4. Cliente vê confirmação de finalização

---

## 🔗 **Sincronização Automática**

### **Timer de Verificação**
- **Frequência**: A cada 5 segundos
- **Endpoint**: `GET /comandas/{id}`
- **Detecção**: Mudança de status para `"fechada"`

### **Estados da Comanda**
- `"aberta"` → Cliente adicionando produtos
- `"aguardando_pagamento"` → Enviada para caixa
- `"fechada"` → Finalizada no desktop

---

## 🚫 **Restrições de Segurança**

### **Mobile**
- ❌ **NÃO pode fechar comanda diretamente**
- ❌ **NÃO pode alterar status para "fechada"**
- ✅ Pode solicitar fechamento
- ✅ Pode chamar garçom
- ✅ Pode adicionar produtos

### **Desktop**
- ✅ **ÚNICO que pode finalizar comandas**
- ✅ Pode alterar status para "fechada"
- ✅ Pode processar pagamentos
- ✅ Pode gerenciar mesas

---

## 📋 **Endpoints da API**

### **Solicitar Fechamento**
```
PUT /comandas/{id}/solicitar-fechamento
Status: 200 OK
Response: {"message": "Comanda enviada para o caixa - aguardando finalização"}
```

### **Finalizar Comanda**
```
PUT /comandas/{id}/finalizar
Status: 200 OK
Response: {"message": "Comanda finalizada com sucesso"}
```

### **Verificar Status**
```
GET /comandas/{id}
Status: 200 OK
Response: Comanda com status atualizado
```

---

## 🎯 **Benefícios do Novo Fluxo**

1. **Segurança**: Apenas funcionários podem finalizar comandas
2. **Controle**: Fluxo padronizado de pagamento
3. **Sincronização**: Mobile e desktop sempre sincronizados
4. **Experiência**: Cliente vê status em tempo real
5. **Auditoria**: Rastreamento completo do processo

---

## 🔧 **Implementação Técnica**

### **Mobile (Flutter)**
- `ComandaProvider.solicitarFechamento()`
- Timer periódico para verificação
- UI adaptativa baseada no status
- Botões condicionais

### **Backend (FastAPI)**
- Endpoint `solicitar-fechamento`
- Validação de permissões
- Mudança de status controlada
- Logs de auditoria

### **Desktop (PyQt5)**
- Interface para finalização
- Controle de status
- Gestão de pagamentos
- Sincronização com backend 