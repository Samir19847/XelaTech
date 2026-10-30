from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QLabel,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView)
from Entidades.Enum import TipoEquipo
from UI.Utilidades import leer_entero
DATO_EXTRA = {
    TipoEquipo.COMPUTADORA_PORTATIL: ("¿Incluye cargador? (sí/no):", "incluyeCargador"),
    TipoEquipo.COMPUTADORA_ESCRITORIO: ("Tipo de gabinete:", "tipoGabinete"),
    TipoEquipo.IMPRESORA: ("Tipo de inyección:", "tipoInyeccion"),
    TipoEquipo.CONSOLA: ("Cantidad de mandos:", "cantidadMandos"),
}


class PestañaEquipos(QWidget):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self._construir()
        self.refrescar()

    def _construir(self):
        self.cmb_tipo = QComboBox()
        for tipo in TipoEquipo:
            self.cmb_tipo.addItem(tipo.value, tipo)
        self.cmb_tipo.currentIndexChanged.connect(self._cambiar_etiqueta_extra)
        self.cmb_cliente = QComboBox()
        self.txt_codigo = QLineEdit()
        self.txt_serie = QLineEdit()
        self.txt_marca = QLineEdit()
        self.txt_modelo = QLineEdit()
        self.txt_estado = QLineEdit()
        self.txt_accesorios = QLineEdit()
        self.lbl_extra = QLabel()
        self.txt_extra = QLineEdit()
        formulario = QFormLayout()
        formulario.addRow("Tipo de equipo:", self.cmb_tipo)
        formulario.addRow("Cliente propietario:", self.cmb_cliente)
        formulario.addRow("Código interno:", self.txt_codigo)
        formulario.addRow("Número de serie:", self.txt_serie)
        formulario.addRow("Marca:", self.txt_marca)
        formulario.addRow("Modelo:", self.txt_modelo)
        formulario.addRow("Estado físico:", self.txt_estado)
        formulario.addRow("Accesorios entregados:", self.txt_accesorios)
        formulario.addRow(self.lbl_extra, self.txt_extra)
        self.btn_registrar = QPushButton("Registrar equipo")
        self.btn_registrar.clicked.connect(self.registrar)
        self.tabla = QTableWidget(0, 7)
        self.tabla.setHorizontalHeaderLabels(["Código", "Serie", "Tipo", "Marca", "Modelo", "Propietario", "Estado físico"])
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        principal = QVBoxLayout(self)
        principal.addLayout(formulario)
        principal.addWidget(self.btn_registrar)
        principal.addWidget(self.tabla)
        self._cambiar_etiqueta_extra()

    def _cambiar_etiqueta_extra(self):
        etiqueta, _ = DATO_EXTRA[self.cmb_tipo.currentData()]
        self.lbl_extra.setText(etiqueta)
        self.txt_extra.clear()

    def _leer_extra(self) -> dict:
        tipo = self.cmb_tipo.currentData()
        _, parametro = DATO_EXTRA[tipo]
        texto = self.txt_extra.text().strip()
        if texto == "":
            return {}
        if tipo == TipoEquipo.COMPUTADORA_PORTATIL:
            if texto.lower() not in ("sí", "si", "no"):
                raise ValueError("Escribe 'sí' o 'no' en ¿Incluye cargador?.")
            return {parametro: texto.lower() in ("sí", "si")}
        if tipo == TipoEquipo.CONSOLA:
            return {parametro: leer_entero(texto, "La cantidad de mandos")}
        return {parametro: texto}

    def registrar(self):
        try:
            extras = self._leer_extra()
            self.gestor.registrar_equipo(
                self.cmb_tipo.currentData(), self.txt_codigo.text(), self.txt_serie.text(),
                self.txt_marca.text(), self.txt_modelo.text(), self.cmb_cliente.currentData(),
                self.txt_estado.text(), self.txt_accesorios.text(), **extras
            )
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo registrar", str(error))
            return
        for campo in (self.txt_codigo, self.txt_serie, self.txt_marca, self.txt_modelo,
                      self.txt_estado, self.txt_accesorios, self.txt_extra):
            campo.clear()
        self.refrescar()

    def refrescar(self):
        elegido = self.cmb_cliente.currentData()
        self.cmb_cliente.clear()
        for c in self.gestor.listar_clientes():
            self.cmb_cliente.addItem(f"{c.código} - {c.nombreCompleto}", c.código)
        indice = self.cmb_cliente.findData(elegido)
        if indice >= 0:
            self.cmb_cliente.setCurrentIndex(indice)
        equipos = self.gestor.listar_equipos()
        self.tabla.setRowCount(len(equipos))
        for fila, e in enumerate(equipos):
            valores = [e.codigoInterno, e.numeroSerie, e.tipoEquipo.value, e.marca, e.modelo,
                       e.propietario.nombreCompleto, e.estadoFisico]
            for columna, valor in enumerate(valores):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))