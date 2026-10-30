from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView)
from Entidades.Enum import CategoriaRepuesto
from UI.Utilidades import leer_entero, leer_decimal


class PestañaRepuestos(QWidget):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self._construir()
        self.refrescar()
    def _construir(self):
        self.txt_codigo = QLineEdit()
        self.txt_nombre = QLineEdit()
        self.cmb_categoria = QComboBox()
        for categoria in CategoriaRepuesto:
            self.cmb_categoria.addItem(categoria.value, categoria)
        self.txt_existencia = QLineEdit()
        self.txt_minima = QLineEdit("1")
        self.txt_costo = QLineEdit()
        self.txt_precio = QLineEdit()
        formulario = QFormLayout()
        formulario.addRow("Código:", self.txt_codigo)
        formulario.addRow("Nombre:", self.txt_nombre)
        formulario.addRow("Categoría:", self.cmb_categoria)
        formulario.addRow("Existencia:", self.txt_existencia)
        formulario.addRow("Existencia mínima:", self.txt_minima)
        formulario.addRow("Costo unitario (Q):", self.txt_costo)
        formulario.addRow("Precio de venta (Q):", self.txt_precio)
        self.btn_registrar = QPushButton("Registrar repuesto")
        self.btn_registrar.clicked.connect(self.registrar)

        self.tabla = QTableWidget(0, 8)
        self.tabla.setHorizontalHeaderLabels(["Código", "Nombre", "Categoría", "Existencia", "Mínima",
                                              "Costo", "Precio", "Estado"])
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        principal = QVBoxLayout(self)
        principal.addLayout(formulario)
        principal.addWidget(self.btn_registrar)
        principal.addWidget(self.tabla)

    def registrar(self):
        try:
            self.gestor.registrar_repuesto(
                self.txt_codigo.text(), self.txt_nombre.text(), self.cmb_categoria.currentData(),
                leer_entero(self.txt_existencia.text(), "La existencia"),
                leer_decimal(self.txt_costo.text(), "El costo unitario"),
                leer_decimal(self.txt_precio.text(), "El precio de venta"),
                leer_entero(self.txt_minima.text(), "La existencia mínima"),
            )
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo registrar", str(error))
            return
        for campo in (self.txt_codigo, self.txt_nombre, self.txt_existencia, self.txt_costo, self.txt_precio):
            campo.clear()
        self.txt_minima.setText("1")
        self.refrescar()

    def refrescar(self):
        repuestos = self.gestor.listar_repuestos()
        self.tabla.setRowCount(len(repuestos))
        for fila, r in enumerate(repuestos):
            if r.existencia == 0:
                estado = "AGOTADO"
            elif r.bajoMinimo:
                estado = "Bajo el mínimo"
            else:
                estado = "Normal"
            valores = [r.codigo, r.nombre, r.categoria.value, r.existencia, r.existenciaMinima,
                       f"Q{r.costoUnitario:,.2f}", f"Q{r.precioVenta:,.2f}", estado]
            for columna, valor in enumerate(valores):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))