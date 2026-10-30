import sys
from Servicios.GestorXelaTech import GestorXelaTech
from PyQt6.QtWidgets import QApplication
from UI.VentanaPrincipal import VentanaPrincipal

def main():
    app = QApplication(sys.argv)
    gestor = GestorXelaTech()
    ventana = VentanaPrincipal(gestor)
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()