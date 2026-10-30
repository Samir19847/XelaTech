from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView)


class PestañaTecnicos(QWidget):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self._construir()
        self.refrescar()

    def _construir(self):
        self.txt_codigo = QLineEdit()
        self.txt_nombre = QLineEdit()
        self.cmb_especialidad = QComboBox()
        for especialidad in self.gestor.especialidades_validas():
            self.cmb_especialidad.addItem(especialidad)
        formulario = QFormLayout()
        formulario.addRow("Código:", self.txt_codigo)
        formulario.addRow("Nombre completo:", self.txt_nombre)
        formulario.addRow("Especialidad:", self.cmb_especialidad)
        self.btn_registrar = QPushButton("Registrar técnico")
        self.btn_registrar.clicked.connect(self.registrar)
        self.btn_disponibilidad = QPushButton("Cambiar disponibilidad del técnico seleccionado")
        self.btn_disponibilidad.clicked.connect(self.cambiar_disponibilidad)
        self.tabla = QTableWidget(0, 7)
        self.tabla.setHorizontalHeaderLabels(["Código", "Nombre", "Especialidad", "Disponible",
                                              "Trabajos activos", "Finalizados", "Calificación"])
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        principal = QVBoxLayout(self)
        principal.addLayout(formulario)
        principal.addWidget(self.btn_registrar)
        principal.addWidget(self.btn_disponibilidad)
        principal.addWidget(self.tabla)
    def registrar(self):
        try:
            self.gestor.registrar_tecnico(self.txt_codigo.text(), self.txt_nombre.text(),
                                          self.cmb_especialidad.currentText())
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo registrar", str(error))
            return
        self.txt_codigo.clear()
        self.txt_nombre.clear()
        self.refrescar()

    def cambiar_disponibilidad(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Selecciona un técnico", "Primero haz clic en una fila de la tabla.")
            return
        codigo = self.tabla.item(fila, 0).text()
        tecnico = self.gestor.obtener_tecnico(codigo)
        try:
            self.gestor.establecer_disponibilidad(codigo, not tecnico.disponible)
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo cambiar", str(error))
            return
        self.refrescar()
        self.tabla.selectRow(fila)

    def refrescar(self):
        tecnicos = self.gestor.listar_tecnicos()
        self.tabla.setRowCount(len(tecnicos))
        for fila, t in enumerate(tecnicos):
            valores = [t.código, t.nombreCompleto, t.especialidad, "Sí" if t.disponible else "No",
                       t.trabajosActivos, t.serviciosFinalizados, f"{t.calificacionPromedio:.2f}"]
            for columna, valor in enumerate(valores):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))