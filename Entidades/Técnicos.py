from Entidades.Persona import Persona

class Tecnico(Persona):
    LIMITE_TRABAJOS_ACTIVOS: int = 3
    def __init__(self, código: str, nombreCompleto: str, especialidad: str, disponible: bool = True, trabajosActivos: int = 0, serviciosFinalizados: int = 0, calificacionPromedio: float = 0.0):
        super().__init__(código, nombreCompleto)
        self.especialidad = especialidad
        self.disponible = disponible
        self.trabajosActivos = trabajosActivos
        self.serviciosFinalizados = serviciosFinalizados
        self.calificacionPromedio = calificacionPromedio

    @property
    def especialidad(self) -> str:
        return self._especialidad
    @especialidad.setter
    def especialidad(self, especialidad: str):
        if not especialidad.strip():
            raise ValueError("La especialidad no puede estar vacía.")
        self._especialidad = especialidad

    @property
    def disponible(self) -> bool:
        return self._disponible
    @disponible.setter
    def disponible(self, disponible: bool):
        if not isinstance(disponible, bool):
            raise ValueError("El estado de disponibilidad debe ser de tipo booleano (True/False).")
        self._disponible = disponible

    @property
    def trabajosActivos(self) -> int:
        return self._trabajosActivos
    @trabajosActivos.setter
    def trabajosActivos(self, cantidad: int):
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad de trabajos activos debe ser un número entero mayor o igual a 0.")
        if cantidad > Tecnico.LIMITE_TRABAJOS_ACTIVOS:
            raise ValueError(
                f"El técnico no puede superar el límite de {Tecnico.LIMITE_TRABAJOS_ACTIVOS} trabajos activos."
            )
        self._trabajosActivos = cantidad

    @property
    def serviciosFinalizados(self) -> int:
        return self._serviciosFinalizados
    @serviciosFinalizados.setter
    def serviciosFinalizados(self, cantidad: int):
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad de servicios finalizados debe ser un número entero mayor o igual a 0.")
        self._serviciosFinalizados = cantidad

    @property
    def calificacionPromedio(self) -> float:
        return self._calificacionPromedio
    @calificacionPromedio.setter
    def calificacionPromedio(self, calificacion: float):
        if not isinstance(calificacion, (int, float)):
            raise ValueError("La calificación promedio debe ser un valor numérico.")
        if not (0.0 <= calificacion <= 5.0):
            raise ValueError("La calificación promedio debe estar entre 0.0 y 5.0.")
        self._calificacionPromedio = float(calificacion)

    def puede_recibir_solicitud(self) -> bool:
        return self.disponible and (self.trabajosActivos < Tecnico.LIMITE_TRABAJOS_ACTIVOS)
    
    def asignar_trabajo(self):
        if not self.puede_recibir_solicitud():
            raise ValueError(f"No se puede asignar la solicitud. El técnico está indisponible o alcanzó el límite de {Tecnico.LIMITE_TRABAJOS_ACTIVOS} trabajos activos.")
        self.trabajosActivos += 1
        if self.trabajosActivos == Tecnico.LIMITE_TRABAJOS_ACTIVOS:
            self.disponible = False

    def finalizar_trabajo(self, nueva_calificacion: float = None):
        if self.trabajosActivos <= 0:
            raise ValueError("El técnico no tiene trabajos activos para finalizar.")
        self.trabajosActivos -= 1
        self.serviciosFinalizados += 1
        self.disponible = True
        if nueva_calificacion is not None:
            total = (self.calificacionPromedio * (self.serviciosFinalizados - 1)) + nueva_calificacion
            self.calificacionPromedio = total / self.serviciosFinalizados