from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView)
from Entidades.Enum import TipoCliente


class PestañaClientes(QWidget):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self._construir()
        self.actualizar_tabla()

    def _construir(self):
        self.txt_codigo = QLineEdit()
        self.txt_nombre = QLineEdit()
        self.txt_telefono = QLineEdit()
        self.txt_correo = QLineEdit()
        self.cmb_tipo = QComboBox()
        for tipo in TipoCliente:
            self.cmb_tipo.addItem(tipo.value, tipo)
        formulario = QFormLayout()
        formulario.addRow("Código:", self.txt_codigo)
        formulario.addRow("Nombre completo:", self.txt_nombre)
        formulario.addRow("Teléfono:", self.txt_telefono)
        formulario.addRow("Correo:", self.txt_correo)
        formulario.addRow("Tipo de cliente:", self.cmb_tipo)
        self.btn_registrar = QPushButton("Registrar cliente")
        self.btn_registrar.clicked.connect(self.registrar)
        self.tabla = QTableWidget(0, 6)
        self.tabla.setHorizontalHeaderLabels(["Código", "Nombre", "Teléfono", "Correo", "Tipo", "Solicitudes"])
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        principal = QVBoxLayout(self)
        principal.addLayout(formulario)
        principal.addWidget(self.btn_registrar)
        principal.addWidget(self.tabla)

    def registrar(self):
        try:
            self.gestor.registrar_cliente(
                self.txt_codigo.text(), self.txt_nombre.text(), self.txt_telefono.text(),
                self.txt_correo.text(), self.cmb_tipo.currentData()
            )
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo registrar", str(error))
            return
        self.limpiar_formulario()
        self.actualizar_tabla()

    def limpiar_formulario(self):
        for campo in (self.txt_codigo, self.txt_nombre, self.txt_telefono, self.txt_correo):
            campo.clear()
        self.cmb_tipo.setCurrentIndex(0)

    def actualizar_tabla(self):
        clientes = self.gestor.listar_clientes()
        self.tabla.setRowCount(len(clientes))
        for fila, c in enumerate(clientes):
            valores = [c.código, c.nombreCompleto, c.telefono, c.correoElectronico,
                       c.tipoCliente.value, c.cantidadSolicitudes]
            for columna, valor in enumerate(valores):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))