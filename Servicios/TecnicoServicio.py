from typing import List, Optional
from Entidades.Técnicos import Tecnico

class TecnicoService:
    def __init__(self, limite_carga_maxima: int = Tecnico.LIMITE_TRABAJOS_ACTIVOS):
        self.tecnicos: List[Tecnico] = []
        self.limite_carga_maxima = limite_carga_maxima

    def registrar_tecnico(self, id_tecnico: str, nombre: str, especialidad: str) -> Tecnico:
        if not id_tecnico or not nombre or not especialidad:
            raise ValueError("Error: Todos los campos del técnico son obligatorios.")
        for t in self.tecnicos:
            if t.id_tecnico == id_tecnico:
                raise ValueError(f"Error: Ya existe un técnico con el ID {id_tecnico}.")
        nuevo_tecnico = Tecnico(id_tecnico, nombre, especialidad)
        self.tecnicos.append(nuevo_tecnico)
        return nuevo_tecnico

    def buscar_por_id(self, id_tecnico: str) -> Optional[Tecnico]:
        for t in self.tecnicos:
            if t.id_tecnico == id_tecnico:
                return t
        return None

    def validar_disponibilidad_asignacion(self, id_tecnico: str) -> Tecnico:
        tecnico = self.buscar_por_id(id_tecnico)
        if not tecnico:
            raise ValueError(f"Error: El técnico con ID {id_tecnico} no existe.")
        if getattr(tecnico, 'carga_activa', 0) >= self.limite_carga_maxima:
            raise ValueError(f"Error: El técnico {tecnico.nombre} ya alcanzó su límite máximo de carga ({self.limite_carga_maxima} solicitudes).")
        return tecnico

    def obtener_todos(self) -> List[Tecnico]:
        return self.tecnicos.copy()