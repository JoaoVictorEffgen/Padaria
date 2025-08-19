# 🍽️ Sistema de Reservas de Mesas - Padaria Delícias

## 📋 **Visão Geral**

O sistema de reservas permite que clientes cadastrados reservem mesas através do site web, com gerenciamento completo no painel desktop. O sistema inclui:

- **Cadastro de clientes** (nome, telefone, endereço)
- **Reservas de mesas** com data, horário e observações
- **Interface web** para clientes fazerem reservas
- **Painel desktop** para funcionários gerenciarem reservas
- **Status de mesas** (livre, ocupada, reservada)

## 🏗️ **Arquitetura do Sistema**

### **Backend (FastAPI)**
- **Modelos**: `Cliente`, `Reserva`
- **Endpoints**: `/clientes/`, `/reservas/`
- **Validações**: Verificação de disponibilidade, conflitos de horário

### **Frontend Web**
- **Seção Mesas**: Visualização de mesas disponíveis
- **Modal de Reserva**: Formulário para novos clientes
- **Modal Cliente Existente**: Para clientes já cadastrados

### **Desktop (PyQt5)**
- **Aba Mesas & Reservas**: Gerenciamento completo
- **Tabela de Reservas**: Lista todas as reservas ativas
- **Detalhes da Reserva**: Informações completas do cliente
- **Ações**: Cancelar reserva, confirmar chegada

## 🔄 **Fluxo de Funcionamento**

### **1. Cliente Acessa o Site**
```
Cliente → Site Web → Seção Mesas → Visualiza Mesas Disponíveis
```

### **2. Cliente Faz Reserva**
```
Cliente → Clica "Reservar" → Modal de Cadastro → Preenche Dados → Confirma
```

### **3. Sistema Verifica Cliente**
```
Telefone Existe? → SIM → Modal Cliente Existente → Escolhe Data/Horário
Telefone Existe? → NÃO → Cria Novo Cliente → Cria Reserva
```

### **4. Mesa é Marcada como Reservada**
```
Status: livre → reservada
Sistema: Cria reserva + Atualiza status da mesa
```

### **5. Funcionário Gerencia no Desktop**
```
Desktop → Aba Reservas → Visualiza Todas as Reservas → Ações Disponíveis
```

## 📱 **Interface Web - Funcionalidades**

### **Seção de Mesas**
- **Grid de mesas** com status visual (livre, ocupada, reservada)
- **Botão "Reservar"** para mesas livres
- **Botão "Ver Reserva"** para mesas reservadas

### **Modal de Nova Reserva**
- **Nome completo** (obrigatório)
- **Telefone** (obrigatório, único)
- **Endereço** (obrigatório)
- **Data da reserva** (obrigatório, mínimo hoje)
- **Horário** (obrigatório, opções pré-definidas)
- **Observações** (opcional)

### **Modal de Cliente Existente**
- **Informações do cliente** (somente leitura)
- **Data da reserva** (obrigatório)
- **Horário** (obrigatório)
- **Observações** (opcional)

## 💻 **Painel Desktop - Funcionalidades**

### **Aba Mesas**
- **Cadastro de novas mesas**
- **Tabela de mesas** com status atualizado
- **Coluna "Reserva"** mostrando informações da reserva

### **Aba Reservas**
- **Lista todas as reservas ativas**
- **Colunas**: ID, Mesa, Cliente, Telefone, Data, Horário, Ações
- **Botão "Ver"** para cada reserva

### **Painel de Detalhes**
- **Informações completas do cliente**
- **Data e horário da reserva**
- **Observações**
- **Botões de ação**

### **Ações Disponíveis**
- **Cancelar Reserva**: Remove a reserva e libera a mesa
- **Confirmar Chegada**: Finaliza a reserva e abre comanda

## 🗄️ **Estrutura do Banco de Dados**

### **Tabela `clientes`**
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR NOT NULL,
    telefone VARCHAR UNIQUE NOT NULL,
    endereco TEXT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Tabela `reservas`**
```sql
CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    data_reserva DATE NOT NULL,
    horario_reserva VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'ativa',
    observacoes TEXT,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mesa_id) REFERENCES mesas (id),
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);
```

### **Tabela `mesas` (Atualizada)**
```sql
-- Colunas existentes + novas
status VARCHAR DEFAULT 'livre',  -- livre, ocupada, reservada
qr_code VARCHAR                  -- URL do QR Code
```

## 🔌 **Endpoints da API**

### **Clientes**
- `POST /clientes/` - Criar novo cliente
- `GET /clientes/` - Listar todos os clientes
- `GET /clientes/{id}` - Obter cliente por ID
- `GET /clientes/telefone/{telefone}` - Obter cliente por telefone

### **Reservas**
- `POST /reservas/` - Criar nova reserva
- `GET /reservas/` - Listar reservas ativas
- `GET /reservas/mesa/{mesa_id}` - Obter reservas de uma mesa
- `PUT /reservas/{id}/cancelar` - Cancelar reserva

## 🎯 **Regras de Negócio**

### **Validações de Reserva**
1. **Mesa disponível**: Status deve ser "livre"
2. **Cliente válido**: Deve existir no sistema
3. **Data futura**: Reserva deve ser para data futura
4. **Sem conflitos**: Mesa não pode ter reserva no mesmo horário
5. **Telefone único**: Cada cliente tem um telefone único

### **Status das Mesas**
- **`livre`**: Mesa disponível para reserva
- **`ocupada`**: Mesa com comanda ativa
- **`reservada`**: Mesa reservada para horário específico

### **Status das Reservas**
- **`ativa`**: Reserva válida e ativa
- **`cancelada`**: Reserva cancelada
- **`finalizada`**: Cliente chegou e reserva foi finalizada

## 🚀 **Como Usar**

### **Para Clientes (Web)**
1. Acesse o site da padaria
2. Vá para a seção "Mesas"
3. Clique em "Reservar" na mesa desejada
4. Preencha seus dados ou use telefone existente
5. Escolha data e horário
6. Confirme a reserva

### **Para Funcionários (Desktop)**
1. Abra o sistema desktop
2. Vá para a aba "Mesas & Reservas"
3. Na aba "Reservas", visualize todas as reservas
4. Clique em "Ver" para ver detalhes
5. Use "Cancelar Reserva" ou "Confirmar Chegada"

## 🔧 **Configuração e Instalação**

### **1. Criar Tabelas**
```bash
python create_reservas_tables.py
```

### **2. Reiniciar Backend**
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### **3. Acessar Sistema**
- **Web**: http://localhost:8000
- **Desktop**: `python run_desktop.py`
- **API Docs**: http://localhost:8000/docs

## 📊 **Dados de Exemplo**

O sistema inclui clientes e reservas de exemplo:
- **João Silva** - Mesa 1 reservada para amanhã às 19:00
- **Maria Santos** - Cliente cadastrado
- **Pedro Costa** - Cliente cadastrado

## 🎨 **Estilos e Interface**

### **CSS Personalizado**
- **Modais responsivos** com animações
- **Status coloridos** para mesas (verde, vermelho, amarelo)
- **Formulários estilizados** com validação visual
- **Botões de ação** com ícones FontAwesome

### **Responsividade**
- **Mobile-first** design
- **Grid adaptativo** para diferentes tamanhos de tela
- **Modais otimizados** para dispositivos móveis

## 🔒 **Segurança e Validação**

### **Validações do Frontend**
- Campos obrigatórios marcados
- Data mínima (hoje)
- Horários pré-definidos
- Formato de telefone

### **Validações do Backend**
- Verificação de existência de mesa
- Verificação de existência de cliente
- Conflitos de horário
- Status de mesa disponível

## 📈 **Próximas Funcionalidades**

### **Funcionalidades Planejadas**
- **Notificações por email** para confirmação de reserva
- **Lembretes automáticos** antes da reserva
- **Histórico de reservas** por cliente
- **Relatórios de ocupação** por período
- **Integração com WhatsApp** para confirmações

### **Melhorias Técnicas**
- **Cache de clientes** para melhor performance
- **Validação em tempo real** de disponibilidade
- **Sistema de fila** para mesas muito solicitadas
- **Backup automático** das reservas

## 🐛 **Solução de Problemas**

### **Problemas Comuns**
1. **Mesa não aparece como reservada**
   - Verificar se a reserva foi criada no banco
   - Verificar status da mesa na tabela `mesas`

2. **Erro ao criar reserva**
   - Verificar se o cliente foi criado
   - Verificar se a mesa existe e está livre
   - Verificar conflitos de horário

3. **Reserva não aparece no desktop**
   - Verificar se o endpoint `/reservas/` está funcionando
   - Verificar se a tabela foi criada corretamente

### **Logs e Debug**
- **Backend**: Logs no terminal do uvicorn
- **Frontend**: Console do navegador (F12)
- **Desktop**: Mensagens de erro nas caixas de diálogo

## 📞 **Suporte**

Para dúvidas ou problemas:
- **Documentação da API**: http://localhost:8000/docs
- **Logs do sistema**: Verificar terminal onde o backend está rodando
- **Testes**: Usar os endpoints da API para verificar funcionamento

---

**Sistema de Reservas v1.0** - Implementado com ❤️ para a Padaria Delícias 