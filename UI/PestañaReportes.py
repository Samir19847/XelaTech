from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QComboBox,
                             QPushButton, QMessageBox)
from Entidades.Enum import EstadoSolicitud
from Servicios.Reportes import Reportes
from UI.Utilidades import crear_tabla, llenar_tabla

class PestanaReportes(QWidget):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self.reportes = Reportes(gestor)
        self._construir()

    def _construir(self):
        self.cmb_reporte = QComboBox()
        for numero, titulo in self.reportes.catalogo():
            self.cmb_reporte.addItem(f"{numero}. {titulo}", numero)
        self.cmb_orden = QComboBox()
        self.cmb_orden.addItem("Orden por defecto", None)
        self.cmb_orden.addItem("Ascendente", False)
        self.cmb_orden.addItem("Descendente", True)
        self.btn_generar = QPushButton("Generar reporte")
        self.btn_generar.clicked.connect(self.generar)
        fila = QHBoxLayout()
        for w in (self.cmb_reporte, QLabel("Orden (reportes 6, 7 y 8):"), self.cmb_orden, self.btn_generar):
            fila.addWidget(w)
        self.txt_nombre = QLineEdit()
        self.cmb_estado = QComboBox()
        self.cmb_estado.addItem("(cualquiera)", None)
        for estado in EstadoSolicitud:
            self.cmb_estado.addItem(estado.value, estado)
        self.txt_marca = QLineEdit()
        self.txt_codigo = QLineEdit()
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar)
        fila_busqueda = QHBoxLayout()
        for w in (QLabel("Cliente (nombre):"), self.txt_nombre, QLabel("Estado:"), self.cmb_estado,
                  QLabel("Marca:"), self.txt_marca, QLabel("Código de solicitud:"), self.txt_codigo, self.btn_buscar):
            fila_busqueda.addWidget(w)
        grupo_busqueda = QGroupBox("Reporte 11: búsquedas (llena los criterios que quieras)")
        grupo_busqueda.setLayout(fila_busqueda)
        self.lbl_titulo = QLabel("")
        self.tabla = crear_tabla(["Resultado"])
        self.lbl_notas = QLabel("")
        self.lbl_notas.setWordWrap(True)
        principal = QVBoxLayout(self)
        principal.addLayout(fila)
        principal.addWidget(grupo_busqueda)
        principal.addWidget(self.lbl_titulo)
        principal.addWidget(self.tabla)
        principal.addWidget(self.lbl_notas)

    def _mostrar(self, reporte):
        self.lbl_titulo.setText(f"Reporte {reporte['numero']}: {reporte['titulo']}")
        llenar_tabla(self.tabla, reporte["filas"], reporte["encabezados"])
        self.lbl_notas.setText("\n".join(reporte["notas"]))

    def generar(self):
        numero = self.cmb_reporte.currentData()
        descendente = self.cmb_orden.currentData()
        try:
            if numero in (6, 7, 8) and descendente is not None:
                metodo = {6: self.reportes.solicitudes_por_costo_total,
                          7: self.reportes.solicitudes_por_fecha,
                          8: self.reportes.repuestos_por_existencia}[numero]
                reporte = metodo(descendente=descendente)
            else:
                reporte = self.reportes.ejecutar(numero)
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo generar el reporte", str(error))
            return
        self._mostrar(reporte)

    def buscar(self):
        try:
            reporte = self.reportes.busquedas(
                nombre_cliente=self.txt_nombre.text().strip() or None,
                estado=self.cmb_estado.currentData(),
                marca=self.txt_marca.text().strip() or None,
                codigo=self.txt_codigo.text().strip() or None,
            )
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo buscar", str(error))
            return
        self._mostrar(reporte)

    def refrescar(self):
        pass
