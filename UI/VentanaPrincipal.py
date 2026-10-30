from PyQt6.QtWidgets import QMainWindow, QTabWidget
from UI.PestañaCliente import PestañaClientes


class VentanaPrincipal(QMainWindow):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self.setWindowTitle("XelaTech Soporte")
        self.resize(1000, 650)
        pestañas = QTabWidget()
        pestañas.addTab(PestañaClientes(gestor), "Clientes")
        self.setCentralWidget(pestañas)