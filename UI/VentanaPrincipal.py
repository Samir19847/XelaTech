from PyQt6.QtWidgets import QMainWindow, QTabWidget
from UI.PestañaCliente import PestañaClientes
from UI.PestañaTecnico import PestañaTecnicos
from UI.PestañaRepuestos import PestañaRepuestos
from UI.PestañaEquipos import PestañaEquipos


class VentanaPrincipal(QMainWindow):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self.setWindowTitle("XelaTech Soporte")
        self.resize(1100, 700)

        self.pestanas = QTabWidget()
        self.pestanas.addTab(PestañaClientes(gestor), "Clientes")
        self.pestanas.addTab(PestañaTecnicos(gestor), "Técnicos")
        self.pestanas.addTab(PestañaRepuestos(gestor), "Repuestos")
        self.pestanas.addTab(PestañaEquipos(gestor), "Equipos")
        self.pestanas.currentChanged.connect(self._al_cambiar_pestana)
        self.setCentralWidget(self.pestanas)

    def _al_cambiar_pestana(self, indice):
        # Cada pestaña sabe redibujarse con los datos actuales del gestor
        self.pestanas.widget(indice).refrescar()