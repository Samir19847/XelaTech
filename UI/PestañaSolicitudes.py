from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox)
from Entidades.Enum import NivelPrioridad
from UI.Utilidades import crear_tabla, llenar_tabla, con_seleccion

class PestañaSolicitudes(QWidget):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self._construir()
        self.refrescar()

    def _construir(self):
        self.txt_codigo = QLineEdit()
        self.cmb_cliente = QComboBox()
        self.cmb_equipo = QComboBox()
        self.cmb_cliente.currentIndexChanged.connect(self._llenar_equipos)
        self.txt_descripcion = QLineEdit()
        self.cmb_prioridad = QComboBox()
        for prioridad in NivelPrioridad:
            self.cmb_prioridad.addItem(prioridad.value, prioridad)
        formulario = QFormLayout()
        formulario.addRow("Código de la solicitud:", self.txt_codigo)
        formulario.addRow("Cliente:", self.cmb_cliente)
        formulario.addRow("Equipo del cliente:", self.cmb_equipo)
        formulario.addRow("Descripción del problema:", self.txt_descripcion)
        formulario.addRow("Prioridad:", self.cmb_prioridad)
        self.btn_crear = QPushButton("Crear solicitud (queda en estado Recibida)")
        self.btn_crear.clicked.connect(self.crear)
        self.btn_encolar = QPushButton("Poner en cola la solicitud seleccionada")
        self.btn_encolar.clicked.connect(self.encolar)
        self.btn_cancelar = QPushButton("Cancelar la solicitud seleccionada")
        self.btn_cancelar.clicked.connect(self.cancelar)
        self.tabla = crear_tabla(["Código", "Cliente", "Equipo", "Prioridad", "Estado", "Técnico", "Total"])
        principal = QVBoxLayout(self)
        principal.addLayout(formulario)
        principal.addWidget(self.btn_crear)
        principal.addWidget(self.btn_encolar)
        principal.addWidget(self.btn_cancelar)
        principal.addWidget(self.tabla)

    def _llenar_equipos(self):
        self.cmb_equipo.clear()
        codigo_cliente = self.cmb_cliente.currentData()
        for e in self.gestor.listar_equipos():
            if e.propietario.código == codigo_cliente:
                self.cmb_equipo.addItem(f"{e.codigoInterno} - {e.marca} {e.modelo}", e.codigoInterno)

    def crear(self):
        try:
            self.gestor.crear_solicitud(
                self.txt_codigo.text(), self.cmb_cliente.currentData(), self.cmb_equipo.currentData(),
                self.txt_descripcion.text(), self.cmb_prioridad.currentData()
            )
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo crear", str(error))
            return
        self.txt_codigo.clear()
        self.txt_descripcion.clear()
        self.refrescar()

    def encolar(self):
        hecho, _ = con_seleccion(self, self.tabla, self.gestor.encolar_solicitud)
        if hecho:
            self.refrescar()
    def cancelar(self):
        hecho, _ = con_seleccion(self, self.tabla, self.gestor.cancelar_solicitud)
        if hecho:
            self.refrescar()

    def refrescar(self):
        elegido = self.cmb_cliente.currentData()
        self.cmb_cliente.blockSignals(True)
        self.cmb_cliente.clear()
        for c in self.gestor.listar_clientes():
            self.cmb_cliente.addItem(f"{c.código} - {c.nombreCompleto}", c.código)
        indice = self.cmb_cliente.findData(elegido)
        if indice >= 0:
            self.cmb_cliente.setCurrentIndex(indice)
        self.cmb_cliente.blockSignals(False)
        self._llenar_equipos()
        # tabla
        filas = []
        for s in self.gestor.listar_solicitudes():
            tecnico = s.tecnico.nombreCompleto if s.tecnico is not None else "-"
            filas.append([s.codigoSolicitud, s.cliente.nombreCompleto, f"{s.equipo.marca} {s.equipo.modelo}",
                          s.prioridad.value, s.estado.value, tecnico, f"Q{s.total:,.2f}"])
        llenar_tabla(self.tabla, filas)
