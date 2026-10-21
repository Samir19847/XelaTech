from datetime import datetime
from typing import List, Optional
from Entidades.Cliente import Cliente
from Entidades.Equipo import Equipo
from Entidades.Técnicos import Tecnico
from Entidades.Repuestos import Repuestos
from Entidades.DetalleRepuesto import DetalleRepuesto
from Estructuras.PilaHistorial import PilaHistorial
from Entidades.Enum import NivelPrioridad, EstadoSolicitud

class Solicitud:
    TRANSICIONES_VALIDAS = {
        EstadoSolicitud.RECIBIDA: {
            EstadoSolicitud.EN_ESPERA,
            EstadoSolicitud.ASIGNADA,
            EstadoSolicitud.CANCELADA,
        },
        EstadoSolicitud.EN_ESPERA: {
            EstadoSolicitud.ASIGNADA,
            EstadoSolicitud.CANCELADA,
        },
        EstadoSolicitud.ASIGNADA: {
            EstadoSolicitud.EN_DIAGNOSTICO,
            EstadoSolicitud.CANCELADA,
        },
        EstadoSolicitud.EN_DIAGNOSTICO: {
            EstadoSolicitud.EN_REPARACION,
            EstadoSolicitud.LISTA_PARA_ENTREGAR,
            EstadoSolicitud.CANCELADA,
        },
        EstadoSolicitud.EN_REPARACION: {
            EstadoSolicitud.LISTA_PARA_ENTREGAR,
        },
        EstadoSolicitud.LISTA_PARA_ENTREGAR: {
            EstadoSolicitud.ENTREGADA,
        },
        EstadoSolicitud.ENTREGADA: set(),
        EstadoSolicitud.CANCELADA: set(),
    }
    ESTADOS_FINALES = {EstadoSolicitud.ENTREGADA, EstadoSolicitud.CANCELADA}
    def __init__(
        self,
        codigoSolicitud: str,
        cliente: Cliente,
        equipo: Equipo,
        descripcionProblema: str,
        prioridad: NivelPrioridad = NivelPrioridad.NORMAL,
        tecnico: Optional[Tecnico] = None,
        costoManoObra: float = 0.0,
    ):
        self._historial = PilaHistorial()
        self._estado = EstadoSolicitud.RECIBIDA
        self.codigoSolicitud = codigoSolicitud
        self.cliente = cliente
        self.equipo = equipo
        self.descripcionProblema = descripcionProblema
        self.fechaHoraRecepcion = datetime.now()
        self.prioridad = prioridad
        self.tecnico = tecnico
        self.diagnostico = ""
        self.repuestosUtilizados: List[DetalleRepuesto] = []
        self.costoManoObra = costoManoObra
        self.cliente.incrementar_solicitudes()

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
        self._exigir_modificable()
        if not isinstance(valor, str):
            raise ValueError("El diagnóstico debe ser una cadena de texto.")
        self._diagnostico = valor.strip()

    @property
    def costoManoObra(self) -> float:
        return self._costoManoObra
    @costoManoObra.setter
    def costoManoObra(self, valor: float):
        self._exigir_modificable()
        if not isinstance(valor, (int, float)) or isinstance(valor, bool) or valor < 0:
            raise ValueError("El costo de mano de obra debe ser un valor numérico mayor o igual a 0.")
        self._costoManoObra = float(valor)

    @property
    def costoRepuestos(self) -> float:
        return sum(detalle.subtotal for detalle in self.repuestosUtilizados)
    @property
    def total(self) -> float:
        costo_revision = self.equipo.calcular_costo_revision()
        return self.costoManoObra + self.costoRepuestos + costo_revision

    def _exigir_modificable(self):
        if self._estado in Solicitud.ESTADOS_FINALES:
            raise ValueError(f"La solicitud está '{self._estado.value}' y ya no admite cambios.")

    def CambiarEstado(self, nuevo_estado: EstadoSolicitud):
        if not isinstance(nuevo_estado, EstadoSolicitud):
            raise ValueError("El nuevo estado debe ser una instancia de EstadoSolicitud.")
        if nuevo_estado == self._estado:
            raise ValueError(f"La solicitud ya está en estado '{nuevo_estado.value}'.")
        permitidas = self.TRANSICIONES_VALIDAS[self._estado]
        if nuevo_estado not in permitidas:
            raise ValueError(
                f"Transición inválida: '{self._estado.value}' → '{nuevo_estado.value}'."
            )
        if nuevo_estado == EstadoSolicitud.ASIGNADA and self._tecnico is None:
            raise ValueError("Una solicitud solo pasa a 'Asignada' mediante asignar_tecnico().")
        self._historial.Apilar(self._estado)
        self._estado = nuevo_estado

    def DeshacerEstado(self):
        self._exigir_modificable()
        if self._historial.esta_vacia():
            raise ValueError("No hay estados anteriores en el historial para deshacer.")
        estado_previo = self._historial.Desapilar()

        if self._estado == EstadoSolicitud.ASIGNADA and self._tecnico is not None:
            self._tecnico.liberar_trabajo()
            self._tecnico = None

        self._estado = estado_previo

    def asignar_tecnico(self, nuevo_tecnico: Tecnico):
        if not isinstance(nuevo_tecnico, Tecnico):
            raise ValueError("El técnico debe ser una instancia de la clase Tecnico.")
        if self._estado not in {EstadoSolicitud.RECIBIDA, EstadoSolicitud.EN_ESPERA}:
            raise ValueError(
                f"No se puede asignar técnico desde el estado '{self._estado.value}'."
            )
        if nuevo_tecnico.especialidad != self.equipo.especialidadRequerida:
            raise ValueError(
                f"Especialidad incompatible: el técnico es '{nuevo_tecnico.especialidad}' "
                f"y el equipo requiere '{self.equipo.especialidadRequerida}'."
            )
        if not nuevo_tecnico.puede_recibir_solicitud():
            raise ValueError(
                "El técnico no está disponible o alcanzó su límite de trabajos activos."
            )
        nuevo_tecnico.asignar_trabajo()
        self._tecnico = nuevo_tecnico
        self.CambiarEstado(EstadoSolicitud.ASIGNADA)

    def agregar_repuesto(self, repuesto: Repuestos, cantidad: int):
        self._exigir_modificable()
        if self._estado not in {EstadoSolicitud.EN_DIAGNOSTICO, EstadoSolicitud.EN_REPARACION}:
            raise ValueError(
                f"Solo se pueden usar repuestos en diagnóstico o reparación (Estado actual: '{self._estado.value}')."
            )
        detalle = DetalleRepuesto(repuesto, cantidad)
        repuesto.usar_repuesto(cantidad)
        self.repuestosUtilizados.append(detalle)

    def finalizar_solicitud(self):
        if self._estado not in {EstadoSolicitud.EN_DIAGNOSTICO, EstadoSolicitud.EN_REPARACION}:
            raise ValueError(
                f"No se puede finalizar una solicitud en estado '{self._estado.value}'."
            )
        self.CambiarEstado(EstadoSolicitud.LISTA_PARA_ENTREGAR)

    def registrar_entrega(self, calificacion_tecnico: int):
        if self._estado != EstadoSolicitud.LISTA_PARA_ENTREGAR:
            raise ValueError(
                f"Solo se puede entregar una solicitud 'Lista para entregar' (estado actual: '{self._estado.value}')."
            )
        if self._tecnico is None:
            raise ValueError("La solicitud no tiene técnico asignado.")
        self._tecnico.finalizar_trabajo(calificacion_tecnico)
        self.CambiarEstado(EstadoSolicitud.ENTREGADA)

    def cancelar_solicitud(self):
        self.CambiarEstado(EstadoSolicitud.CANCELADA)
        if self._tecnico is not None:
            self._tecnico.liberar_trabajo()
            self._tecnico = None