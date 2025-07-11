import sys
import os

# Adicionar o diretório pai ao path para encontrar o módulo desktop
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from desktop.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Configurar estilo da aplicação
    app.setStyle('Fusion')
    
    # Criar e mostrar janela principal
    window = MainWindow()
    window.show()
    
    # Executar aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 