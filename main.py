import sys
from PyQt5.QtWidgets import QApplication
from cnab_bradesco_gui import CNABBradescoGUI

def main():
    """
    Função principal que inicia a aplicação GUI
    """
    app = QApplication(sys.argv)
    window = CNABBradescoGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 