from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QComboBox,
                             QPushButton, QMessageBox)
from Entidades.Enum import EstadoSolicitud
from UI.Utilidades import crear_tabla, llenar_tabla, con_seleccion, leer_decimal, leer_entero


class PestanaAtencion(QWidget):
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        self._construir()
        self.refrescar()

    def _construir(self):
        self.tbl_urgente = crear_tabla(["Código", "Cliente", "Equipo"])
        self.tbl_normal = crear_tabla(["Código", "Cliente", "Equipo"])
        self.cmb_dia = QComboBox()
        self.cmb_dia.addItem("Hoy", None)
        for indice, nombre in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]):
            self.cmb_dia.addItem(nombre, indice)
        self.btn_atender = QPushButton("Atender siguiente de la cola (urgentes primero)")
        self.btn_atender.clicked.connect(self.atender)
        col_urgente = QVBoxLayout()
        col_urgente.addWidget(QLabel("Cola URGENTE (FIFO)"))
        col_urgente.addWidget(self.tbl_urgente)
        col_normal = QVBoxLayout()
        col_normal.addWidget(QLabel("Cola NORMAL (FIFO)"))
        col_normal.addWidget(self.tbl_normal)
        colas = QHBoxLayout()
        colas.addLayout(col_urgente)
        colas.addLayout(col_normal)
        fila_atender = QHBoxLayout()
        fila_atender.addWidget(QLabel("Día de la semana para la matriz:"))
        fila_atender.addWidget(self.cmb_dia)
        fila_atender.addWidget(self.btn_atender)
        grupo_colas = QGroupBox("1. Colas de espera")
        caja = QVBoxLayout()
        caja.addLayout(colas)
        caja.addLayout(fila_atender)
        grupo_colas.setLayout(caja)
        self.tabla = crear_tabla(["Código", "Cliente", "Equipo", "Prioridad", "Estado", "Técnico", "Diagnóstico", "Total"])
        self.cmb_estado = QComboBox()
        for estado in (EstadoSolicitud.EN_DIAGNOSTICO, EstadoSolicitud.EN_REPARACION, EstadoSolicitud.LISTA_PARA_ENTREGAR):
            self.cmb_estado.addItem(estado.value, estado)
        self.btn_estado = QPushButton("Cambiar estado")
        self.btn_estado.clicked.connect(self.cambiar_estado)
        self.txt_diagnostico = QLineEdit()
        self.txt_mano_obra = QLineEdit()
        self.btn_diagnostico = QPushButton("Guardar diagnóstico")
        self.btn_diagnostico.clicked.connect(self.guardar_diagnostico)
        self.cmb_repuesto = QComboBox()
        self.txt_cantidad = QLineEdit("1")
        self.btn_repuesto = QPushButton("Usar repuesto")
        self.btn_repuesto.clicked.connect(self.usar_repuesto)
        self.cmb_calificacion = QComboBox()
        for n in range(1, 6):
            self.cmb_calificacion.addItem(f"{n} estrella(s)", n)
        self.cmb_calificacion.setCurrentIndex(4)
        self.btn_entregar = QPushButton("Entregar al cliente")
        self.btn_entregar.clicked.connect(self.entregar)
        self.btn_deshacer = QPushButton("Deshacer último cambio")
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_historial = QPushButton("Ver historial")
        self.btn_historial.clicked.connect(self.ver_historial)
        self.btn_cancelar = QPushButton("Cancelar solicitud")
        self.btn_cancelar.clicked.connect(self.cancelar)
        fila1 = QHBoxLayout()
        for w in (QLabel("Avanzar a:"), self.cmb_estado, self.btn_estado):
            fila1.addWidget(w)
        fila2 = QHBoxLayout()
        for w in (QLabel("Diagnóstico:"), self.txt_diagnostico, QLabel("Mano de obra (Q):"),
                  self.txt_mano_obra, self.btn_diagnostico):
            fila2.addWidget(w)
        fila3 = QHBoxLayout()
        for w in (QLabel("Repuesto:"), self.cmb_repuesto, QLabel("Cantidad:"), self.txt_cantidad, self.btn_repuesto):
            fila3.addWidget(w)
        fila4 = QHBoxLayout()
        for w in (QLabel("Calificación al técnico:"), self.cmb_calificacion, self.btn_entregar):
            fila4.addWidget(w)
        fila5 = QHBoxLayout()
        for w in (self.btn_deshacer, self.btn_historial, self.btn_cancelar):
            fila5.addWidget(w)
        grupo_acciones = QGroupBox("2. Solicitudes: selecciona una fila y usa las acciones")
        caja2 = QVBoxLayout()
        caja2.addWidget(self.tabla)
        for fila in (fila1, fila2, fila3, fila4, fila5):
            caja2.addLayout(fila)
        grupo_acciones.setLayout(caja2)

        principal = QVBoxLayout(self)
        principal.addWidget(grupo_colas)
        principal.addWidget(grupo_acciones)

    def atender(self):
        try:
            solicitud, tecnico = self.gestor.atender_siguiente(self.cmb_dia.currentData())
        except ValueError as error:
            QMessageBox.warning(self, "No se pudo atender", str(error))
            return
        self.refrescar()
        QMessageBox.information(self, "Solicitud asignada",
                                f"La solicitud {solicitud.codigoSolicitud} quedó asignada a {tecnico.nombreCompleto}.")
    def cambiar_estado(self):
        hecho, _ = con_seleccion(self, self.tabla,
                                 lambda codigo: self.gestor.cambiar_estado(codigo, self.cmb_estado.currentData()))
        if hecho:
            self.refrescar()
    def guardar_diagnostico(self):
        hecho, _ = con_seleccion(self, self.tabla, lambda codigo: self.gestor.registrar_diagnostico(
            codigo, self.txt_diagnostico.text(), leer_decimal(self.txt_mano_obra.text(), "El costo de mano de obra")))
        if hecho:
            self.txt_diagnostico.clear()
            self.txt_mano_obra.clear()
            self.refrescar()
    def usar_repuesto(self):
        hecho, alerta = con_seleccion(self, self.tabla, lambda codigo: self.gestor.usar_repuesto(
            codigo, self.cmb_repuesto.currentData(), leer_entero(self.txt_cantidad.text(), "La cantidad")))
        if hecho:
            self.refrescar()
            if alerta:
                QMessageBox.warning(self, "Alerta de stock", alerta)

    def entregar(self):
        hecho, _ = con_seleccion(self, self.tabla,
                                 lambda codigo: self.gestor.entregar_solicitud(codigo, self.cmb_calificacion.currentData()))
        if hecho:
            self.refrescar()
    def deshacer(self):
        hecho, _ = con_seleccion(self, self.tabla, self.gestor.deshacer_ultimo_cambio)
        if hecho:
            self.refrescar()
    def cancelar(self):
        hecho, _ = con_seleccion(self, self.tabla, self.gestor.cancelar_solicitud)
        if hecho:
            self.refrescar()

    def ver_historial(self):
        hecho, historial = con_seleccion(self, self.tabla, self.gestor.historial_de)
        if hecho:
            texto = " → ".join(e.value for e in historial) if historial else "Sin cambios anteriores."
            QMessageBox.information(self, "Historial (pila de estados)", texto)
    @staticmethod
    def _fila_cola(s):
        return [s.codigoSolicitud, s.cliente.nombreCompleto, f"{s.equipo.marca} {s.equipo.modelo}"]

    def refrescar(self):
        llenar_tabla(self.tbl_urgente, [self._fila_cola(s) for s in self.gestor.listar_cola_urgente()])
        llenar_tabla(self.tbl_normal, [self._fila_cola(s) for s in self.gestor.listar_cola_normal()])
        filas = []
        for s in self.gestor.listar_solicitudes():
            tecnico = s.tecnico.nombreCompleto if s.tecnico is not None else "-"
            filas.append([s.codigoSolicitud, s.cliente.nombreCompleto, f"{s.equipo.marca} {s.equipo.modelo}",
                          s.prioridad.value, s.estado.value, tecnico, s.diagnostico or "-", f"Q{s.total:,.2f}"])
        llenar_tabla(self.tabla, filas)
        elegido = self.cmb_repuesto.currentData()
        self.cmb_repuesto.clear()
        for r in self.gestor.listar_repuestos():
            self.cmb_repuesto.addItem(f"{r.codigo} - {r.nombre} (existencia: {r.existencia})", r.codigo)
        indice = self.cmb_repuesto.findData(elegido)
        if indice >= 0:
            self.cmb_repuesto.setCurrentIndex(indice)
