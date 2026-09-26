from datetime import datetime
from typing import List, Optional
from Entidades.Cliente import Cliente
from Entidades.Equipo import Equipo
from Entidades.Técnicos import Tecnico
from Entidades.Repuestos import Repuestos
from Entidades.Enum import NivelPrioridad, EstadoSolicitud

class Solicitud:
    def __init__(
        self,
        codigoSolicitud: str,
        cliente: Cliente,
        equipo: Equipo,
        descripcionProblema: str,
        prioridad: NivelPrioridad = NivelPrioridad.NORMAL,
        tecnico: Optional[Tecnico] = None,
        costoManoObra: float = 0.0
    ):
        self.codigoSolicitud = codigoSolicitud
        self.cliente = cliente
        self.equipo = equipo
        self.descripcionProblema = descripcionProblema
        self.fechaHoraRecepcion = datetime.now()
        self.prioridad = prioridad
        self.estado = EstadoSolicitud.RECIBIDA
        self.tecnico = tecnico
        self.diagnostico = ""
        self.repuestosUtilizados: List[Repuestos] = []
        self.costoManoObra = costoManoObra
        self.cliente.cantidadSolicitudes += 1


    @property
    def codigoSolicitud(self) -> str:
        return self._codigoSolicitud
    @codigoSolicitud.setter
    def codigoSolicitud(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código de solicitud no puede estar vacío.")
        self._codigoSolicitud = valor.strip()

    @property
    def cliente(self) -> Cliente:
        return self._cliente
    @cliente.setter
    def cliente(self, valor: Cliente):
        if not isinstance(valor, Cliente):
            raise ValueError("El cliente asignado debe ser una instancia válida de la clase Cliente.")
        self._cliente = valor

    @property
    def equipo(self) -> Equipo:
        return self._equipo
    @equipo.setter
    def equipo(self, valor: Equipo):
        if not isinstance(valor, Equipo):
            raise ValueError("El equipo debe ser una instancia válida de la clase Equipo.")
        self._equipo = valor

    @property
    def descripcionProblema(self) -> str:
        return self._descripcionProblema
    @descripcionProblema.setter
    def descripcionProblema(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La descripción del problema no puede estar vacía.")
        self._descripcionProblema = valor.strip()

    @property
    def prioridad(self) -> NivelPrioridad:
        return self._prioridad
    @prioridad.setter
    def prioridad(self, valor: NivelPrioridad):
        if not isinstance(valor, NivelPrioridad):
            raise ValueError("La prioridad debe ser una instancia del Enum NivelPrioridad.")
        self._prioridad = valor

    @property
    def estado(self) -> EstadoSolicitud:
        return self._estado
    @estado.setter
    def estado(self, valor: EstadoSolicitud):
        if not isinstance(valor, EstadoSolicitud):
            raise ValueError("El estado debe ser una instancia del Enum EstadoSolicitud.")
        self._estado = valor

    @property
    def tecnico(self) -> Optional[Tecnico]:
        return self._tecnico
    @tecnico.setter
    def tecnico(self, valor: Optional[Tecnico]):
        if valor is not None and not isinstance(valor, Tecnico):
            raise ValueError("El técnico asignado debe ser una instancia de la clase Tecnico o None.")
        self._tecnico = valor

    @property
    def diagnostico(self) -> str:
        return self._diagnostico
    @diagnostico.setter
    def diagnostico(self, valor: str):
        if not isinstance(valor, str):
            raise ValueError("El diagnóstico debe ser una cadena de texto.")
        self._diagnostico = valor.strip()

    @property
    def costoManoObra(self) -> float:
        return self._costoManoObra
    @costoManoObra.setter
    def costoManoObra(self, valor: float):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El costo de mano de obra debe ser un valor numérico mayor o igual a 0.")
        self._costoManoObra = float(valor)

    @property
    def costoRepuestos(self) -> float:
        return sum(repuesto.precioVenta * repuesto.cantidadUtilizada for repuesto in self.repuestosUtilizados)
    @property
    def total(self) -> float:
        costo_revision = self.equipo.calcular_costo_revision()
        return self.costoManoObra + self.costoRepuestos + costo_revision

    def asignar_tecnico(self, nuevo_tecnico: Tecnico):
        nuevo_tecnico.asignar_trabajo()
        self.tecnico = nuevo_tecnico
        self.estado = EstadoSolicitud.ASIGNADA

    def agregar_repuesto(self, repuesto: Repuestos, cantidad: int):
        repuesto.usar_repuesto(cantidad)
        self.repuestosUtilizados.append(repuesto)

    def finalizar_solicitud(self, calificacion_tecnico: Optional[float] = None):
        if self.estado == EstadoSolicitud.ENTREGADA or self.estado == EstadoSolicitud.CANCELADA:
            raise ValueError("No se puede finalizar una solicitud entregada o cancelada.")
        if self.tecnico is not None:
            self.tecnico.finalizar_trabajo(nueva_calificacion=calificacion_tecnico)

        self.estado = EstadoSolicitud.LISTA_PARA_ENTREGAR