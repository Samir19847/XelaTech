from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QMessageBox)
from Servicios.GeneradorDatos import GeneradorDatos
from UI.Utilidades import crear_tabla, llenar_tabla, leer_entero

class PestañaDatos(QWidget):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self._construir()
        self.refrescar()

    def _construir(self):
        self.spn_cantidad = QSpinBox()
        self.spn_cantidad.setRange(1, 100)
        self.spn_cantidad.setValue(8)
        self.txt_semilla = QLineEdit()
        self.txt_semilla.setPlaceholderText("opcional: con la misma semilla salen los mismos datos")
        self.btn_generar = QPushButton("Generar datos de prueba (Random)")
        self.btn_generar.clicked.connect(self.generar)
        fila = QHBoxLayout()
        for w in (QLabel("Cantidad de solicitudes:"), self.spn_cantidad, QLabel("Semilla:"),
                  self.txt_semilla, self.btn_generar):
            fila.addWidget(w)
        self.lbl_resultado = QLabel("")
        self.lbl_resultado.setWordWrap(True)
        self.tabla = crear_tabla(["Calificación", "Cantidad de entregas"])
        self.lbl_promedio = QLabel("")
        principal = QVBoxLayout(self)
        principal.addLayout(fila)
        principal.addWidget(self.lbl_resultado)
        principal.addWidget(QLabel("Estadísticas de calificaciones (arreglo de 5 posiciones):"))
        principal.addWidget(self.tabla)
        principal.addWidget(self.lbl_promedio)

    def generar(self):
        try:
            texto = self.txt_semilla.text().strip()
            semilla = leer_entero(texto, "La semilla") if texto else None
            resumen = GeneradorDatos(self.gestor, semilla).generar(self.spn_cantidad.value())
        except ValueError as error:
            QMessageBox.warning(self, "No se pudieron generar los datos", str(error))
            return
        por_estado = ", ".join(f"{estado}: {n}" for estado, n in resumen["por_estado"].items())
        texto = f"Solicitudes creadas: {resumen['solicitudes_creadas']}. Por estado: {por_estado}."
        if resumen["omitidas"]:
            texto += f" Omitidas: {len(resumen['omitidas'])}."
        self.lbl_resultado.setText(texto)
        self.refrescar()

    def refrescar(self):
        datos = self.gestor.estadisticas_calificaciones()
        arreglo = datos["arreglo"]
        llenar_tabla(self.tabla, [[f"{i + 1} estrella(s)", arreglo[i]] for i in range(len(arreglo))])
        self.lbl_promedio.setText(f"Promedio general de calificaciones: {datos['promedio']:.2f}")
