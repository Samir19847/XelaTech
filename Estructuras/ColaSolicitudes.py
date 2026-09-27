from collections import deque
from typing import Optional, List
from Entidades.Solicitudes import Solicitud
from Entidades.Enum import NivelPrioridad

class ColaSolicitudes:
    def __init__(self):
        self._colaUrgente: deque[Solicitud]=deque()
        self._colaNormal: deque[Solicitud]=deque()

    def Encolar(self, solicitud:Solicitud):
        if solicitud.prioridad==NivelPrioridad.URGENTE:
            self._colaUrgente.append(solicitud)
        else:
            self._colaNormal.append(solicitud)

    def Desencolar(self) -> Optional[Solicitud]:
        if self._colaUrgente:
            return self._colaUrgente.popleft()
        else:
            return self._colaNormal.popleft()
        return None

    def SolicitudesExistentes(self)->bool:
        return len(self._colaUrgente) >0 or len(self._colaNormal) >0

    def ObtenerSolicitudesUrgentes(self)->List[Solicitud]:
        return list(self._colaUrgente)

    def ObtenerSolicitudesNormales(self)->List[Solicitud]:
        return list(self._colaNormal)
    