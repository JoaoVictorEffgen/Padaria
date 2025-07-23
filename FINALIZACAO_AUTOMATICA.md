# Finalização Automática de Comandas

## 🎯 Funcionalidade Implementada

Quando uma comanda é **finalizada no desktop** (caixa), o **mobile/tablet detecta automaticamente** e mostra uma tela de confirmação para o cliente.

## 🔄 Como Funciona

### 1. **Monitoramento Automático**
- O mobile verifica o status da comanda a cada **5 segundos**
- Quando uma comanda está aberta, aparece "Monitorando..." no cabeçalho
- O sistema detecta mudanças de status em tempo real

### 2. **Detecção de Finalização**
- Quando o desktop finaliza uma comanda (status = "fechada")
- O mobile detecta automaticamente a mudança
- Limpa a comanda atual e mostra tela de confirmação

### 3. **Interface do Cliente**
- Tela verde com ícone de check
- Mensagem: "Comanda Finalizada!"
- Botão para abrir nova comanda

## 📱 Fluxo Completo

```
1. Cliente abre comanda no mobile
   ↓
2. Mobile mostra "Monitorando..." 
   ↓
3. Cliente faz pedidos
   ↓
4. Cliente fecha comanda no mobile
   ↓
5. Desktop recebe comanda para pagamento
   ↓
6. Caixa finaliza pagamento no desktop
   ↓
7. Mobile detecta automaticamente (5-10 segundos)
   ↓
8. Mobile mostra "Comanda Finalizada!"
   ↓
9. Cliente pode abrir nova comanda
```

## 🛠️ Implementação Técnica

### Mobile (Flutter)

#### ComandaProvider
```dart
// Timer para verificação periódica
Timer? _statusCheckTimer;

// Iniciar verificação a cada 5 segundos
void _iniciarVerificacaoStatus() {
  _statusCheckTimer = Timer.periodic(
    const Duration(seconds: 5), 
    (timer) => _verificarStatusComanda()
  );
}

// Verificar se comanda foi finalizada
Future<void> _verificarStatusComanda() async {
  final comandaId = _comandaAtual?.id;
  if (comandaId == null) return;

  // Busca status resumido da comanda
  final status = await ApiService.getStatusComanda(comandaId);

  if (status == null) return;

  if (status['status_comanda'] == "fechada") {
    _comandaAtual = null;
    _mensagemStatus = "Comanda finalizada no caixa";
    notifyListeners();
    return;
  }

  // Mensagem geral
  switch (status['status_geral_itens']) {
    case "pronto":
      _mensagemStatus = "Seu pedido está pronto!";
      break;
    case "preparando":
      _mensagemStatus = "Seu pedido está sendo preparado";
      break;
    case "pendente":
      _mensagemStatus = "Pedido recebido, aguardando preparo";
      break;
    case "parcial":
      _mensagemStatus = "Parte do seu pedido já está pronta!";
      break;
    default:
      _mensagemStatus = "Aguardando atualização do pedido";
  }

  // (Opcional) Você pode guardar status dos itens para mostrar na interface
  // status['itens'] é uma lista de {produto, status}

  notifyListeners();
}
```

#### Interface
```dart
// Indicador visual de monitoramento
Row(
  children: [
    Container(
      width: 8, height: 8,
      decoration: BoxDecoration(
        color: Colors.green,
        shape: BoxShape.circle,
      ),
    ),
    Text('Monitorando...'),
  ],
)

// Tela de finalização
if (provider.error == "Comanda finalizada no caixa") {
  return Center(
    child: Column(
      children: [
        Icon(Icons.check_circle, color: Colors.green, size: 64),
        Text('Comanda Finalizada!'),
        Text('Sua comanda foi finalizada no caixa.'),
        ElevatedButton(
          onPressed: () => _abrirComanda(provider),
          child: Text('Abrir Nova Comanda'),
        ),
      ],
    ),
  );
}
```

### Desktop (PyQt5)

#### Finalização de Comanda
```python
def finalizar_comanda(self):
    """Finaliza o pagamento da comanda"""
    try:
        self.api_client.finalizar_comanda(self.comanda_atual["id"])
        QMessageBox.information(self, "Sucesso", "Pagamento finalizado com sucesso")
        self.atualizar_comandas()
        self.comanda_atual = None
        self.limpar_detalhes_comanda()
    except Exception as e:
        QMessageBox.warning(self, "Erro", f"Erro ao finalizar comanda: {e}")
```

### Backend (FastAPI)

#### Endpoint de Finalização
```python
@app.put("/comandas/{comanda_id}/finalizar")
def finalizar_comanda(comanda_id: int, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(
        models.Comanda.id == comanda_id
    ).first()
    
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    
    comanda.status = "fechada"
    db.commit()
    return {"message": "Comanda finalizada com sucesso"}
```

## 🧪 Como Testar

### 1. **Preparação**
```bash
# Iniciar todos os sistemas
python start_system.py
```

### 2. **Teste Manual**
1. Abra o app mobile/tablet
2. Abra uma comanda
3. Observe "Monitorando..." no cabeçalho
4. No desktop, selecione a comanda e clique "Finalizar"
5. Observe que o mobile detecta automaticamente

### 3. **Teste Automatizado**
```bash
# Executar script de teste
python test_finalizar_comanda.py
```

## ⚙️ Configurações

### Intervalo de Verificação
```dart
// Em ComandaProvider
Timer.periodic(const Duration(seconds: 5), ...)
```

### URL da API
```dart
// Em ApiService
static const String baseUrl = 'http://192.168.0.7:8000';
```

## 🔧 Personalização

### Mudar Intervalo de Verificação
```dart
// Em ComandaProvider.dart, linha ~30
Timer.periodic(const Duration(seconds: 10), ...) // 10 segundos
```

### Mudar Mensagem de Finalização
```dart
// Em ComandaProvider.dart, linha ~50
_error = "Sua conta foi fechada no caixa";
```

### Mudar Cores da Interface
```dart
// Em home_screen.dart
color: Colors.blue, // Cor do indicador
color: Colors.green, // Cor da tela de finalização
```

## 🚨 Troubleshooting

### Mobile não detecta finalização
1. Verificar se o backend está rodando
2. Verificar se o IP está correto no ApiService
3. Verificar logs do mobile para erros de conexão

### Verificação muito lenta
1. Reduzir intervalo no Timer.periodic
2. Verificar latência da rede
3. Verificar se há muitas requisições simultâneas

### Erro de conexão
1. Verificar se mobile e desktop estão na mesma rede
2. Verificar firewall/antivírus
3. Testar conectividade com ping

## 📊 Vantagens

### Para o Cliente
- ✅ **Experiência fluida**: Não precisa perguntar se pode sair
- ✅ **Feedback visual**: Sabe que o pagamento foi processado
- ✅ **Facilidade**: Pode abrir nova comanda imediatamente

### Para o Negócio
- ✅ **Eficiência**: Cliente sai mais rápido
- ✅ **Satisfação**: Experiência profissional
- ✅ **Controle**: Sistema integrado e confiável

### Para o Desenvolvimento
- ✅ **Tempo real**: Comunicação automática
- ✅ **Robustez**: Tratamento de erros
- ✅ **Escalabilidade**: Fácil de estender

## 🔮 Próximas Melhorias

1. **Notificações push** quando comanda for finalizada
2. **Som de confirmação** na finalização
3. **Histórico de comandas** no mobile
4. **Modo offline** com sincronização posterior
5. **Múltiplas mesas** por dispositivo 

---

## 1. Backend: Adicionar status "reservada" e endpoints

- Adicionar o status "reservada" no modelo Mesa.
- Criar endpoints para reservar e desreservar uma mesa.

## 2. Frontend Web: Interface de reserva

- Adicionar uma seção/listagem de mesas na interface web.
- Permitir ao usuário clicar em "Reservar" (ou "Cancelar Reserva") para cada mesa.
- Exibir o status da mesa (livre, ocupada, reservada).

---

### Começando pelo backend:

#### a) Adicionar status "reservada" no modelo Mesa

No arquivo `models.py`, altere o comentário do campo status para incluir "reservada":
```python
status = Column(String, default="livre")  # livre, ocupada, reservada
```

#### b) Criar endpoints para reservar/desreservar mesa

No arquivo `main.py` do backend, adicione:

```python
from fastapi import Path

@app.put("/mesas/{mesa_id}/reservar")
def reservar_mesa(mesa_id: int = Path(...), db: Session = Depends(get_db)):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    if mesa.status == "ocupada":
        raise HTTPException(status_code=400, detail="Mesa já está ocupada")
    mesa.status = "reservada"
    db.commit()
    return {"message": "Mesa reservada com sucesso"}

@app.put("/mesas/{mesa_id}/liberar")
def liberar_mesa(mesa_id: int = Path(...), db: Session = Depends(get_db)):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    mesa.status = "livre"
    db.commit()
    return {"message": "Mesa liberada com sucesso"}
```

---

### Depois, no frontend:

- Adicionar uma seção de mesas (ex: abaixo do cardápio).
- Listar todas as mesas e seus status.
- Botão para reservar/liberar mesa, conforme o status.

Se quiser, posso já aplicar as mudanças no backend para você! Confirma que posso seguir com a implementação dos endpoints de reserva/liberação? 

---

## 2. Flutter: Provider e Widget para Status da Comanda

### a) No seu `ComandaProvider` (ou similar):

Adicione um campo para a mensagem de status:
```dart
String? _mensagemStatus;
String? get mensagemStatus => _mensagemStatus;
```

Adapte o método de verificação de status para buscar o novo endpoint:
```dart
Future<void> _verificarStatusComanda() async {
  final comandaId = _comandaAtual?.id;
  if (comandaId == null) return;

  // Busca status resumido da comanda
  final status = await ApiService.getStatusComanda(comandaId);

  if (status == null) return;

  if (status['status_comanda'] == "fechada") {
    _comandaAtual = null;
    _mensagemStatus = "Comanda finalizada no caixa";
    notifyListeners();
    return;
  }

  // Mensagem geral
  switch (status['status_geral_itens']) {
    case "pronto":
      _mensagemStatus = "Seu pedido está pronto!";
      break;
    case "preparando":
      _mensagemStatus = "Seu pedido está sendo preparado";
      break;
    case "pendente":
      _mensagemStatus = "Pedido recebido, aguardando preparo";
      break;
    case "parcial":
      _mensagemStatus = "Parte do seu pedido já está pronta!";
      break;
    default:
      _mensagemStatus = "Aguardando atualização do pedido";
  }

  // (Opcional) Você pode guardar status dos itens para mostrar na interface
  // status['itens'] é uma lista de {produto, status}

  notifyListeners();
}
```

No seu `ApiService`:
```dart
static Future<Map<String, dynamic>?> getStatusComanda(int comandaId) async {
  final response = await http.get(Uri.parse('$baseUrl/comandas/$comandaId/status'));
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  }
  return null;
}
```

### b) Exemplo de Widget para mostrar o status:

```dart
Consumer<ComandaProvider>(
  builder: (context, provider, _) {
    if (provider.mensagemStatus != null) {
      return Card(
        color: Colors.amber[50],
        margin: EdgeInsets.all(16),
        child: ListTile(
          leading: Icon(Icons.info, color: Colors.orange),
          title: Text(provider.mensagemStatus!),
        ),
      );
    }
    return SizedBox.shrink();
  },
)
```

Se quiser mostrar o status de cada item:
```dart
if (provider.statusItens != null) ...[
  for (final item in provider.statusItens!)
    ListTile(
      title: Text(item['produto']),
      trailing: Text(item['status']),
    ),
]
```

---

Se precisar do código completo para Flutter, me diga qual estrutura você usa (Provider, Bloc, etc.) e se quer a tela de status detalhada ou só um resumo!  
Se quiser, posso te ajudar a testar o endpoint do backend também. 

---

## 1. Teste do Endpoint `/comandas/{comanda_id}/status`

Aqui está um exemplo de teste em Python para você rodar e ver a resposta do backend:

```python
import requests

BASE_URL = "http://localhost:8000"  # ajuste se necessário
COMANDA_ID = 1  # coloque aqui o ID de uma comanda existente

def testar_status_comanda():
    url = f"{BASE_URL}/comandas/{COMANDA_ID}/status"
    resp = requests.get(url)
    print("Status HTTP:", resp.status_code)
    print("Resposta JSON:")
    print(resp.json())

if __name__ == "__main__":
    testar_status_comanda()
```

- Troque o `COMANDA_ID` para um ID válido de comanda aberta no seu sistema.
- Rode o script com `python nome_do_arquivo.py`.
- Você deve ver um JSON parecido com:
  ```json
  {
    "comanda_id": 1,
    "mesa_numero": 5,
    "status_comanda": "aberta",
    "status_geral_itens": "preparando",
    "itens": [
      {"produto": "Café", "status": "pronto"},
      {"produto": "Pão", "status": "preparando"}
    ]
  }
  ```

Se o resultado for esse, o backend está pronto para o mobile consumir!

---

## 2. Exemplo de Tela Resumida no Flutter

No Flutter, basta mostrar a mensagem principal (como já sugerido):

```dart
Consumer<ComandaProvider>(
  builder: (context, provider, _) {
    if (provider.mensagemStatus != null) {
      return Card(
        color: Colors.amber[50],
        margin: EdgeInsets.all(16),
        child: ListTile(
          leading: Icon(Icons.info, color: Colors.orange),
          title: Text(provider.mensagemStatus!),
        ),
      );
    }
    return SizedBox.shrink();
  },
)
```

Se quiser, pode colocar esse widget no topo da tela da comanda/pedido.

---

Se rodar o teste do backend e der tudo certo, seu app mobile já pode consumir esse status!  
Se quiser, posso te ajudar a criar um teste automatizado para rodar sempre que quiser validar o backend.  
Me avise se precisar de mais algum ajuste! 