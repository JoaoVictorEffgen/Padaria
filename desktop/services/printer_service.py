import win32print
import win32api
import tempfile
import os
from datetime import datetime
from typing import Dict, List

class PrinterService:
    def __init__(self):
        self.default_printer = win32print.GetDefaultPrinter()
    
    def listar_impressoras(self) -> List[str]:
        """Lista todas as impressoras disponíveis"""
        printers = []
        for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            printers.append(printer[2])
        return printers
    
    def definir_impressora_padrao(self, printer_name: str):
        """Define uma impressora como padrão"""
        try:
            win32print.SetDefaultPrinter(printer_name)
            self.default_printer = printer_name
            return True
        except Exception as e:
            print(f"Erro ao definir impressora padrão: {e}")
            return False
    
    def gerar_comando_impressao(self, comanda: Dict) -> str:
        """Gera o conteúdo da comanda para impressão"""
        content = []
        
        # Cabeçalho
        content.append("=" * 40)
        content.append("           PADARIA")
        content.append("=" * 40)
        content.append(f"Comanda: #{comanda['id']}")
        content.append(f"Mesa: {comanda['mesa_numero']}")
        content.append(f"Data: {comanda['data_abertura']}")
        content.append(f"Status: {comanda['status']}")
        content.append("-" * 40)
        
        # Itens
        content.append("ITENS:")
        content.append("-" * 40)
        
        for item in comanda['itens']:
            produto = item['produto']
            subtotal = item['quantidade'] * item['preco_unitario']
            
            content.append(f"{produto['nome']}")
            content.append(f"  {item['quantidade']}x R$ {item['preco_unitario']:.2f} = R$ {subtotal:.2f}")
            
            if item.get('observacoes'):
                content.append(f"  Obs: {item['observacoes']}")
            
            if item.get('status'):
                content.append(f"  Status: {item['status']}")
            
            content.append("")
        
        # Total
        content.append("-" * 40)
        content.append(f"TOTAL: R$ {comanda['total']:.2f}")
        content.append("=" * 40)
        
        # Observações da comanda
        if comanda.get('observacoes'):
            content.append("")
            content.append("OBSERVAÇÕES:")
            content.append(comanda['observacoes'])
            content.append("=" * 40)
        
        # Rodapé
        content.append("")
        content.append("Obrigado pela preferência!")
        content.append(f"Impresso em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        return "\n".join(content)
    
    def imprimir_comanda(self, comanda: Dict, printer_name: str = None) -> bool:
        """Imprime uma comanda"""
        try:
            # Usar impressora especificada ou padrão
            if printer_name:
                self.definir_impressora_padrao(printer_name)
            
            # Gerar conteúdo
            content = self.gerar_comando_impressao(comanda)
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(content)
                temp_file = f.name
            
            # Imprimir arquivo
            win32api.ShellExecute(0, "print", temp_file, None, ".", 0)
            
            # Aguardar um pouco e deletar arquivo temporário
            import time
            time.sleep(2)
            os.unlink(temp_file)
            
            return True
            
        except Exception as e:
            print(f"Erro ao imprimir comanda: {e}")
            return False
    
    def imprimir_comandas_pendentes(self, comandas: List[Dict], printer_name: str = None) -> bool:
        """Imprime múltiplas comandas pendentes"""
        try:
            for comanda in comandas:
                if comanda['status'] in ['aberta', 'impressa']:
                    success = self.imprimir_comanda(comanda, printer_name)
                    if not success:
                        print(f"Erro ao imprimir comanda {comanda['id']}")
                        return False
            return True
        except Exception as e:
            print(f"Erro ao imprimir comandas pendentes: {e}")
            return False
    
    def gerar_relatorio_impressao(self, comandas: List[Dict]) -> str:
        """Gera relatório de comandas para impressão"""
        content = []
        
        # Cabeçalho
        content.append("=" * 50)
        content.append("           RELATÓRIO DE COMANDA")
        content.append("=" * 50)
        content.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        content.append(f"Total de comandas: {len(comandas)}")
        content.append("-" * 50)
        
        # Comandas
        for comanda in comandas:
            content.append(f"Comanda #{comanda['id']} - Mesa {comanda['mesa_numero']}")
            content.append(f"Status: {comanda['status']}")
            content.append(f"Total: R$ {comanda['total']:.2f}")
            content.append(f"Itens: {comanda['quantidade_itens']}")
            content.append("-" * 30)
        
        # Resumo
        total_geral = sum(c['total'] for c in comandas)
        content.append(f"TOTAL GERAL: R$ {total_geral:.2f}")
        content.append("=" * 50)
        
        return "\n".join(content)
    
    def imprimir_relatorio(self, comandas: List[Dict], printer_name: str = None) -> bool:
        """Imprime relatório de comandas"""
        try:
            content = self.gerar_relatorio_impressao(comandas)
            
            # Usar impressora especificada ou padrão
            if printer_name:
                self.definir_impressora_padrao(printer_name)
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(content)
                temp_file = f.name
            
            # Imprimir arquivo
            win32api.ShellExecute(0, "print", temp_file, None, ".", 0)
            
            # Aguardar um pouco e deletar arquivo temporário
            import time
            time.sleep(2)
            os.unlink(temp_file)
            
            return True
            
        except Exception as e:
            print(f"Erro ao imprimir relatório: {e}")
            return False

# Classe alternativa para sistemas não-Windows
class SimplePrinterService:
    def __init__(self):
        self.default_printer = "console"
    
    def listar_impressoras(self) -> List[str]:
        """Lista impressoras disponíveis (simulado)"""
        return ["console", "arquivo"]
    
    def imprimir_comanda(self, comanda: Dict, printer_name: str = None) -> bool:
        """Imprime comanda no console ou arquivo"""
        try:
            content = self.gerar_comando_impressao(comanda)
            
            if printer_name == "arquivo":
                # Salvar em arquivo
                filename = f"comanda_{comanda['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Comanda salva em: {filename}")
            else:
                # Imprimir no console
                print("\n" + "="*50)
                print("COMANDA PARA IMPRESSÃO:")
                print("="*50)
                print(content)
                print("="*50)
            
            return True
            
        except Exception as e:
            print(f"Erro ao imprimir comanda: {e}")
            return False
    
    def gerar_comando_impressao(self, comanda: Dict) -> str:
        """Gera o conteúdo da comanda para impressão"""
        content = []
        
        # Cabeçalho
        content.append("=" * 40)
        content.append("           PADARIA")
        content.append("=" * 40)
        content.append(f"Comanda: #{comanda['id']}")
        content.append(f"Mesa: {comanda['mesa_numero']}")
        content.append(f"Data: {comanda['data_abertura']}")
        content.append(f"Status: {comanda['status']}")
        content.append("-" * 40)
        
        # Itens
        content.append("ITENS:")
        content.append("-" * 40)
        
        for item in comanda['itens']:
            produto = item['produto']
            subtotal = item['quantidade'] * item['preco_unitario']
            
            content.append(f"{produto['nome']}")
            content.append(f"  {item['quantidade']}x R$ {item['preco_unitario']:.2f} = R$ {subtotal:.2f}")
            
            if item.get('observacoes'):
                content.append(f"  Obs: {item['observacoes']}")
            
            if item.get('status'):
                content.append(f"  Status: {item['status']}")
            
            content.append("")
        
        # Total
        content.append("-" * 40)
        content.append(f"TOTAL: R$ {comanda['total']:.2f}")
        content.append("=" * 40)
        
        # Observações da comanda
        if comanda.get('observacoes'):
            content.append("")
            content.append("OBSERVAÇÕES:")
            content.append(comanda['observacoes'])
            content.append("=" * 40)
        
        # Rodapé
        content.append("")
        content.append("Obrigado pela preferência!")
        content.append(f"Impresso em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        return "\n".join(content) 