# main.py
import sys
from PyQt6.QtWidgets import QApplication
from app_ui import MainWindow

# Ponto de entrada da aplicação
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())