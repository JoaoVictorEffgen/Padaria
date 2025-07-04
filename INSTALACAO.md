# Guia de Instalação - Sistema de Padaria

Este guia irá ajudá-lo a instalar e configurar o Sistema de Padaria em seu computador.

## 📋 Pré-requisitos

### Sistema Operacional
- **Windows 10/11** (recomendado)
- **Linux** (Ubuntu 18.04+)
- **macOS** (10.14+)

### Requisitos Mínimos
- **RAM**: 4GB
- **Espaço em disco**: 2GB livres
- **Processador**: Dual-core 2.0GHz
- **Rede**: Conexão Wi-Fi/Ethernet

## 🐍 Instalação do Python

### Windows

#### Opção 1: Microsoft Store (Recomendado)
1. Abra a **Microsoft Store**
2. Procure por **"Python"**
3. Instale a versão mais recente (3.11+)
4. Aguarde a instalação completar

#### Opção 2: Download Direto
1. Acesse: https://www.python.org/downloads/
2. Clique em **"Download Python"**
3. **IMPORTANTE**: Marque ✅ "Add Python to PATH"
4. Clique em **"Install Now"**
5. Aguarde a instalação completar

#### Opção 3: Scripts Automáticos
Execute um dos scripts incluídos:
```bash
# Script Batch
INSTALAR_PYTHON.bat

# Script PowerShell
powershell -ExecutionPolicy Bypass -File INSTALAR_PYTHON.ps1
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### macOS
```bash
# Usando Homebrew
brew install python3

# Ou baixe do site oficial
# https://www.python.org/downloads/macos/
```

## ✅ Verificação da Instalação

Após instalar o Python, verifique se está funcionando:

```bash
python --version
# ou
python3 --version
```

Você deve ver algo como: `Python 3.11.0`

## 🚀 Instalação do Sistema

### Passo 1: Clone ou Baixe o Projeto
```bash
# Se você tem Git instalado:
git clone <url-do-repositorio>
cd ProjetoPadaria

# Ou baixe o ZIP e extraia
```

### Passo 2: Execute o Script de Inicialização
```bash
python start_system.py
```

O script irá:
- ✅ Verificar se Python está instalado
- 📦 Instalar dependências automaticamente
- 🗄️ Configurar banco de dados
- 🚀 Iniciar backend API
- 🖥️ Abrir aplicação desktop

## 🔧 Instalação Manual (Alternativa)

Se o script automático não funcionar, siga estes passos:

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados
```bash
python setup_database.py
```

### 3. Iniciar Backend
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Iniciar Desktop (em outro terminal)
```bash
python desktop/main.py
```

## 📱 Configuração do Tablet (Opcional)

### Pré-requisitos
- **Flutter SDK** instalado
- **Android Studio** ou **VS Code**

### Instalação do Flutter
1. Acesse: https://flutter.dev/docs/get-started/install
2. Siga as instruções para seu sistema operacional
3. Execute: `flutter doctor`

### Configuração do App
```bash
cd tablet
flutter pub get
flutter run
```

## 🌐 Configuração de Rede

### Para Conectar Tablets
1. Descubra o IP do seu computador:
   ```bash
   # Windows
   ipconfig
   
   # Linux/macOS
   ifconfig
   ```

2. Configure o IP no tablet:
   - Edite: `tablet/lib/services/api_service.dart`
   - Altere: `baseUrl = 'http://SEU_IP:8000'`

3. Certifique-se de que todos os dispositivos estão na mesma rede Wi-Fi

## 🖨️ Configuração de Impressora

### Windows
1. Conecte a impressora ao computador
2. Instale os drivers da impressora
3. Configure como impressora padrão
4. Teste a impressão

### Linux/macOS
1. Configure a impressora via CUPS
2. Teste a impressão
3. Configure no sistema se necessário

## 🚨 Solução de Problemas

### Python não encontrado
```bash
# Verifique se está no PATH
echo $PATH  # Linux/macOS
echo %PATH% # Windows

# Reinstale Python marcando "Add to PATH"
```

### Erro de dependências
```bash
# Atualize pip
python -m pip install --upgrade pip

# Instale dependências uma por vez
pip install fastapi uvicorn sqlalchemy pydantic PyQt5 requests
```

### Porta 8000 ocupada
```bash
# Encontre o processo
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/macOS

# Mate o processo ou use outra porta
```

### Erro de banco de dados
```bash
# Delete o arquivo do banco e recrie
rm padaria.db
python setup_database.py
```

### Tablet não conecta
1. Verifique se o IP está correto
2. Teste: `ping SEU_IP`
3. Verifique firewall
4. Teste no navegador: `http://SEU_IP:8000/produtos/`

## 📞 Suporte

### Logs e Debug
```bash
# Backend logs
tail -f backend.log

# Desktop logs
# Verifique console da aplicação

# Tablet logs
flutter logs
```

### Recursos Úteis
- **Documentação**: README.md
- **Demo**: DEMO.md
- **Recursos Extras**: RECURSOS_EXTRAS.md
- **Resumo**: RESUMO_EXECUTIVO.md

### Comandos Úteis
```bash
# Parar backend
Ctrl+C

# Backup do banco
cp padaria.db backup/padaria_$(date +%Y%m%d).db

# Verificar status
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

## ✅ Verificação Final

Após a instalação, verifique se tudo está funcionando:

1. **Backend**: http://localhost:8000/docs
2. **Desktop**: Aplicação deve abrir automaticamente
3. **Banco**: Dados iniciais devem estar carregados
4. **Rede**: IP deve estar acessível na rede local

## 🎉 Próximos Passos

1. **Configure impressoras** (se necessário)
2. **Teste criação de comandas**
3. **Configure tablets** na mesma rede
4. **Teste QR Code** das mesas
5. **Leia a documentação** para usar todos os recursos

---

**Sistema de Padaria v2.0** - Guia de Instalação ✅ 