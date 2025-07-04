# Sistema de Padaria - Desktop e Tablet

Sistema completo para gerenciamento de padaria com interface desktop para caixa/gerência e app tablet para mesas.

## Estrutura do Projeto

```
ProjetoPadaria/
├── backend/                 # API REST (FastAPI)
│   ├── app/
│   │   ├── models.py       # Modelos do banco
│   │   ├── database.py     # Configuração do banco
│   │   ├── schemas.py      # Schemas Pydantic
│   │   └── main.py         # API principal
│   └── requirements.txt
├── desktop/                 # Sistema Desktop (PyQt5)
│   ├── main.py
│   ├── ui/
│   │   ├── main_window.py
│   │   └── comanda_widget.py
│   └── services/
│       └── api_client.py
├── tablet/                  # App Tablet (Flutter)
│   ├── lib/
│   │   ├── main.dart
│   │   ├── models/
│   │   ├── services/
│   │   └── widgets/
│   └── pubspec.yaml
└── database/               # Banco SQLite
    └── padaria.db
```

## Funcionalidades

### Sistema Desktop
- Cadastro de produtos (nome, preço, categoria)
- Visualização de comandas em tempo real
- Associação de comanda à mesa
- Cálculo automático de valores
- Fechamento de comandas
- Histórico e relatórios

### App Tablet
- Interface por categorias de produtos
- Adição de produtos à comanda
- Visualização do valor parcial
- Botão "Chamar Garçom"
- Fechamento de comanda

## Instalação e Execução

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Desktop
```bash
cd desktop
python main.py
```

### Tablet
```bash
cd tablet
flutter pub get
flutter run
```

## Banco de Dados

Tabelas principais:
- `mesas` (id, numero, status)
- `produtos` (id, nome, preco, categoria)
- `comandas` (id, mesa_id, status, total, data)
- `itens_comanda` (id, comanda_id, produto_id, quantidade) 