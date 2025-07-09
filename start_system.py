#!/usr/bin/env python3
"""
Script de inicialização completa do Sistema de Padaria
Inclui todos os recursos extras implementados
"""

import os
import sys
import subprocess
import time
import socket
import platform
from pathlib import Path

def print_header():
    """Imprime cabeçalho do sistema"""
    print("=" * 60)
    print("           SISTEMA DE PADARIA - VERSÃO 2.0")
    print("=" * 60)
    print("Recursos implementados:")
    print("[OK] Sistema Desktop (PyQt5)")
    print("[OK] Backend API (FastAPI)")
    print("[OK] Aplicativo Tablet (Flutter)")
    print("[OK] Impressão de Comandas")
    print("[OK] Painel para Garçons")
    print("[OK] Modo Offline com Sincronização")
    print("[OK] QR Code para Menu Público")
    print("=" * 60)

def check_python_installation():
    """Verifica se Python está instalado e acessível"""
    print("[INFO] Verificando instalação do Python...")
    
    # Tentar diferentes comandos Python
    python_commands = ['python', 'python3', 'py']
    python_path = None
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                python_path = cmd
                print(f"[OK] Python encontrado: {result.stdout.strip()}")
                break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    if not python_path:
        print("[ERRO] Python não encontrado no sistema!")
        print("\n[INFO] Para instalar o Python:")
        print("1. Acesse: https://www.python.org/downloads/")
        print("2. Baixe a versão mais recente (3.8 ou superior)")
        print("3. Durante a instalação, MARQUE 'Add Python to PATH'")
        print("4. Reinicie o terminal após a instalação")
        print("\n[INFO] Ou use o Microsoft Store:")
        print("   - Abra Microsoft Store")
        print("   - Procure por 'Python'")
        print("   - Instale a versão mais recente")
        return None
    
    return python_path

def check_python_version(python_cmd):
    """Verifica versão do Python"""
    try:
        result = subprocess.run([python_cmd, '--version'], 
                              capture_output=True, text=True)
        version_output = result.stdout.strip()
        
        # Extrair número da versão
        import re
        version_match = re.search(r'Python (\d+\.\d+)', version_output)
        if version_match:
            version = version_match.group(1)
            major, minor = map(int, version.split('.'))
            
            if major >= 3 and minor >= 8:
                print(f"[OK] Python {version} - Versão compatível")
                return True
            else:
                print(f"[ERRO] Python {version} - Versão muito antiga")
                print("   Necessário Python 3.8 ou superior")
                return False
        else:
            print(f"[AVISO] Não foi possível determinar a versão: {version_output}")
            return True  # Assumir que é compatível
            
    except Exception as e:
        print(f"[ERRO] Erro ao verificar versão: {e}")
        return False

def install_dependencies(python_cmd):
    """Instala dependências Python"""
    print("\n[INFO] Instalando dependências Python...")
    try:
        # Verificar se requirements.txt existe
        if not Path("requirements.txt").exists():
            print("[ERRO] Arquivo requirements.txt não encontrado")
            return False
        
        # Instalar dependências
        result = subprocess.run([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] Dependências Python instaladas com sucesso")
            return True
        else:
            print(f"[ERRO] Erro ao instalar dependências:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERRO] Erro ao instalar dependências: {e}")
        return False

def setup_database(python_cmd):
    """Configura banco de dados"""
    print("\n[INFO] Configurando banco de dados...")
    try:
        # Verificar se o backend existe
        if not Path("backend").exists():
            print("[ERRO] Diretório 'backend' não encontrado")
            return False
        
        # Executar setup do banco
        result = subprocess.run([python_cmd, "-c", """
import sys
import os
sys.path.append('backend')
from app.database import engine, SessionLocal
from app import models
from app.models import Mesa, Produto, Garcom

# Criar tabelas
models.Base.metadata.create_all(bind=engine)
print("[OK] Tabelas criadas com sucesso")

# Inserir dados iniciais
db = SessionLocal()

# Verificar se já existem dados
if db.query(Mesa).count() == 0:
    # Criar mesas
    for i in range(1, 11):
        mesa = Mesa(numero=i, status="livre")
        db.add(mesa)
    print("[OK] 10 mesas criadas")

if db.query(Produto).count() == 0:
    # Criar produtos
    produtos = [
        Produto(nome="Pão Francês", preco=0.50, categoria="Pães", descricao="Pão francês tradicional"),
        Produto(nome="Pão de Queijo", preco=2.50, categoria="Pães", descricao="Pão de queijo caseiro"),
        Produto(nome="Croissant", preco=4.00, categoria="Pães", descricao="Croissant de manteiga"),
        Produto(nome="Café Expresso", preco=3.50, categoria="Cafés", descricao="Café expresso tradicional"),
        Produto(nome="Cappuccino", preco=5.00, categoria="Cafés", descricao="Cappuccino com espuma de leite"),
        Produto(nome="Coca-Cola", preco=4.50, categoria="Bebidas", descricao="Refrigerante Coca-Cola 350ml"),
        Produto(nome="Suco de Laranja", preco=6.00, categoria="Bebidas", descricao="Suco de laranja natural"),
        Produto(nome="Brigadeiro", preco=3.00, categoria="Doces", descricao="Brigadeiro caseiro"),
        Produto(nome="Pastel de Carne", preco=5.50, categoria="Salgados", descricao="Pastel de carne moída"),
        Produto(nome="Coxinha", preco=4.50, categoria="Salgados", descricao="Coxinha de frango"),
    ]
    for produto in produtos:
        db.add(produto)
    print("[OK] 10 produtos criados")

if db.query(Garcom).count() == 0:
    # Criar garçons
    garcons = [
        Garcom(nome="João Silva", codigo="G001"),
        Garcom(nome="Maria Santos", codigo="G002"),
        Garcom(nome="Pedro Costa", codigo="G003"),
    ]
    for garcom in garcons:
        db.add(garcom)
    print("[OK] 3 garçons criados")

db.commit()
db.close()
print("[OK] Banco de dados configurado com sucesso")
        """], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"[ERRO] Erro ao configurar banco:")
            print(result.stderr)
            return False
        
    except Exception as e:
        print(f"[ERRO] Erro ao configurar banco: {e}")
        return False

def start_backend(python_cmd):
    """Inicia o backend"""
    print("\n[INFO] Iniciando Backend API...")
    try:
        # Verificar se a porta está livre
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print("[AVISO] Porta 8000 já está em uso. Backend pode já estar rodando.")
            return True
        
        # Iniciar backend em background
        if platform.system() == "Windows":
            subprocess.Popen([python_cmd, "-m", "uvicorn", "backend.app.main:app", 
                            "--host", "0.0.0.0", "--port", "8000", "--reload"],
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([python_cmd, "-m", "uvicorn", "backend.app.main:app", 
                            "--host", "0.0.0.0", "--port", "8000", "--reload"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Aguardar backend inicializar
        print("[INFO] Aguardando backend inicializar...")
        time.sleep(5)
        
        # Testar conexão
        try:
            import requests
            response = requests.get("http://localhost:8000/docs", timeout=5)
            if response.status_code == 200:
                print("[OK] Backend iniciado com sucesso")
                print("[INFO] Documentação API: http://localhost:8000/docs")
                return True
        except:
            pass
        
        print("[AVISO] Backend pode ter iniciado, mas não foi possível verificar")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro ao iniciar backend: {e}")
        return False

def start_desktop(python_cmd):
    """Inicia aplicação desktop"""
    print("\n[INFO] Iniciando aplicação Desktop...")
    try:
        if not Path("desktop/main.py").exists():
            print("[ERRO] Arquivo desktop/main.py não encontrado")
            return False
        
        if platform.system() == "Windows":
            subprocess.Popen([python_cmd, "desktop/main.py"],
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([python_cmd, "desktop/main.py"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("[OK] Aplicação Desktop iniciada")
        print("[INFO] Recursos disponíveis:")
        print("   • Gestão de Comandas")
        print("   • Cadastro de Produtos")
        print("   • Gestão de Mesas")
        print("   • Painel de Garçons")
        print("   • Impressão de Comandas")
        print("   • Relatórios")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro ao iniciar desktop: {e}")
        return False

def check_flutter():
    """Verifica se Flutter está instalado"""
    try:
        result = subprocess.run(["flutter", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Flutter encontrado")
            return True
    except FileNotFoundError:
        pass
    
    print("[AVISO] Flutter não encontrado")
    print("[INFO] Para usar o aplicativo tablet, instale o Flutter:")
    print("   https://flutter.dev/docs/get-started/install")
    return False

def setup_tablet():
    """Configura aplicativo tablet"""
    if not check_flutter():
        return False
    
    print("\n[INFO] Configurando aplicativo Tablet...")
    try:
        # Verificar se o projeto Flutter existe
        if not Path("tablet").exists():
            print("[ERRO] Diretório 'tablet' não encontrado")
            return False
        
        # Instalar dependências Flutter
        os.chdir("tablet")
        subprocess.run(["flutter", "pub", "get"], check=True, capture_output=True)
        os.chdir("..")
        
        print("[OK] Dependências Flutter instaladas")
        print("[INFO] Para executar o tablet:")
        print("   cd tablet")
        print("   flutter run")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro ao configurar tablet: {e}")
        return False

def show_network_info():
    """Mostra informações de rede"""
    print("\n[INFO] Informações de Rede:")
    try:
        # Obter IP local
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"   Hostname: {hostname}")
        print(f"   IP Local: {local_ip}")
        print(f"   Backend API: http://{local_ip}:8000")
        print(f"   Documentação: http://{local_ip}:8000/docs")
        print(f"   Menu Público: http://{local_ip}:8000/menu/1")
        
        print("\n[INFO] Para conectar tablets:")
        print(f"   • Configure o IP {local_ip} no aplicativo")
        print(f"   • Use a mesma rede Wi-Fi")
        print(f"   • Teste a conexão: http://{local_ip}:8000/produtos/")
        
    except Exception as e:
        print(f"[ERRO] Erro ao obter informações de rede: {e}")

def show_qr_code_info():
    """Mostra informações sobre QR Code"""
    print("\n[INFO] QR Code para Menu Público:")
    print("   • Cada mesa tem seu próprio QR Code")
    print("   • Acesse: http://localhost:8000/mesas/1/qr-code")
    print("   • Clientes podem escanear e ver o menu")
    print("   • Funciona mesmo sem comanda aberta")

def show_offline_info():
    """Mostra informações sobre modo offline"""
    print("\n[INFO] Modo Offline:")
    print("   • Tablet funciona sem internet")
    print("   • Dados são salvos localmente")
    print("   • Sincronização automática quando online")
    print("   • Operações pendentes são enviadas")

def main():
    """Função principal"""
    print_header()
    
    # Verificar Python
    python_cmd = check_python_installation()
    if not python_cmd:
        print("\n[ERRO] Python não encontrado. Instale o Python primeiro.")
        return
    
    # Verificar versão
    if not check_python_version(python_cmd):
        print("\n[ERRO] Versão do Python incompatível.")
        return
    
    # Instalar dependências
    if not install_dependencies(python_cmd):
        print("[ERRO] Falha na instalação de dependências")
        return
    
    # Configurar banco
    if not setup_database(python_cmd):
        print("[ERRO] Falha na configuração do banco")
        return
    
    # Iniciar backend
    if not start_backend(python_cmd):
        print("[ERRO] Falha ao iniciar backend")
        return
    
    # Iniciar desktop
    if not start_desktop(python_cmd):
        print("[ERRO] Falha ao iniciar desktop")
        return
    
    # Configurar tablet (opcional)
    setup_tablet()
    
    # Mostrar informações
    show_network_info()
    show_qr_code_info()
    show_offline_info()
    
    print("\n" + "=" * 60)
    print("[OK] Sistema iniciado com sucesso!")
    print("=" * 60)
    print("\n[INFO] Próximos passos:")
    print("1. Abra o aplicativo Desktop")
    print("2. Configure impressoras (se necessário)")
    print("3. Teste a criação de comandas")
    print("4. Configure tablets na mesma rede")
    print("5. Teste o QR Code das mesas")
    print("\n[INFO] Comandos úteis:")
    print("   • Parar backend: Ctrl+C no terminal do backend")
    print("   • Ver logs: tail -f backend.log")
    print("   • Backup DB: cp padaria.db backup/")
    print("\n[INFO] Suporte:")
    print("   • Documentação: README.md")
    print("   • Demo: DEMO.md")
    print("   • Resumo: RESUMO_EXECUTIVO.md")

if __name__ == "__main__":
    main() 