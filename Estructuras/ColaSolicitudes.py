from collections import deque
from typing import Optional, List
from Entidades.Solicitudes import Solicitud
from Entidades.Enum import NivelPrioridad

class ColaSolicitudes:
    def __init__(self):
        self._colaUrgente: deque[Solicitud] = deque()
        self._colaNormal: deque[Solicitud] = deque()

    def _cola_de(self, solicitud: Solicitud) -> deque:
        return self._colaUrgente if solicitud.prioridad == NivelPrioridad.URGENTE else self._colaNormal

    def Encolar(self, solicitud: Solicitud):
        if solicitud in self._colaUrgente or solicitud in self._colaNormal:
            raise ValueError(f"La solicitud '{solicitud.codigoSolicitud}' ya está en la cola.")
        self._cola_de(solicitud).append(solicitud)

    def EncolarAlFrente(self, solicitud: Solicitud):
        if solicitud in self._colaUrgente or solicitud in self._colaNormal:
            raise ValueError(f"La solicitud '{solicitud.codigoSolicitud}' ya está en la cola.")
        self._cola_de(solicitud).appendleft(solicitud)

    def Siguiente(self) -> Optional[Solicitud]:
        if self._colaUrgente:
            return self._colaUrgente[0]
        if self._colaNormal:
            return self._colaNormal[0]
        return None

    def Desencolar(self) -> Optional[Solicitud]:
        if self._colaUrgente:
            return self._colaUrgente.popleft()
        if self._colaNormal:
            return self._colaNormal.popleft()
        return None

    def Quitar(self, solicitud: Solicitud) -> bool:
        for cola in (self._colaUrgente, self._colaNormal):
            if solicitud in cola:
                cola.remove(solicitud)
                return True
        return False

    def SolicitudesExistentes(self) -> bool:
        return len(self._colaUrgente) > 0 or len(self._colaNormal) > 0

    def Cantidad(self) -> int:
        return len(self._colaUrgente) + len(self._colaNormal)

    def ObtenerSolicitudesUrgentes(self) -> List[Solicitud]:
        return list(self._colaUrgente)

    def ObtenerSolicitudesNormales(self) -> List[Solicitud]:
        return list(self._colaNormal)