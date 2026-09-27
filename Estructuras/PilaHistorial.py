from typing import List
from Entidades.Enum import EstadoSolicitud

class PilaHistorial:
    def __init__(self):
        self._items: List[EstadoSolicitud]=[]

    def Apilar(self, estado: EstadoSolicitud):
        self._items.append(estado)

    def Desapilar(self)->EstadoSolicitud:
        if self.esta_vacia():
            raise ValueError("No se hay estados anteriores en el historial para deshacer.")
        return self._items.pop()

    def Ver_tope(self) -> EstadoSolicitud:
        if self.esta_vacia():
            raise ValueError("El historial está vacío.")
        return self._items[-1]

    def ObtenerHistorialCompleto(self)-> List[EstadoSolicitud]:
        return list(self._items)
    