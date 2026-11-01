from PyQt6.QtWidgets import QMainWindow, QTabWidget
from UI.PestañaCliente import PestañaClientes
from UI.PestañaTecnico import PestañaTecnicos
from UI.PestañaRepuestos import PestañaRepuestos
from UI.PestañaEquipos import PestañaEquipos
from UI.PestañaSolicitudes import PestañaSolicitudes
from UI.PestañaAtencion import PestañaAtencion
from UI.PestañaReportes import PestañaReportes
from UI.PestañaDatos import PestañaDatos


class VentanaPrincipal(QMainWindow):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self.setWindowTitle("::: [ D E R E N ] ::: XelaTech Soporte ::: [ D E R E N ] :::")
        self.resize(1200, 780)
        self.pestanas = QTabWidget()
        self.pestanas.addTab(PestañaClientes(gestor), "Clientes")
        self.pestanas.addTab(PestañaTecnicos(gestor), "Técnicos")
        self.pestanas.addTab(PestañaRepuestos(gestor), "Repuestos")
        self.pestanas.addTab(PestañaEquipos(gestor), "Equipos")
        self.pestanas.addTab(PestañaSolicitudes(gestor), "Solicitudes")
        self.pestanas.addTab(PestañaAtencion(gestor), "Atención")
        self.pestanas.addTab(PestañaReportes(gestor), "Reportes y búsquedas")
        self.pestanas.addTab(PestañaDatos(gestor), "Datos de prueba")
        self.pestanas.currentChanged.connect(self._al_cambiar_pestana)
        self.setCentralWidget(self.pestanas)

    def _al_cambiar_pestana(self, indice):
        self.pestanas.widget(indice).refrescar()
