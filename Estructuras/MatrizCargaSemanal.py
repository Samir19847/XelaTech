from typing import List, Tuple, Dict
from Entidades.Técnicos import Tecnico

class MatrizCargaSemanal:
    DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    def __init__(self, listaTecnicos: List[Tecnico]):
        self._tecnicos = listaTecnicos
        self._matriz: List[List[int]] = [
            [0 for _ in range(len(self.DIAS_SEMANA))]
            for _ in range(len(self._tecnicos))
        ]

    def registrar_asignacion(self, indice_tecnico: int, indice_dia: int, cantidad: int = 1):
        if 0 <= indice_tecnico < len(self._tecnicos) and 0 <= indice_dia < len(self.DIAS_SEMANA):
            self._matriz[indice_tecnico][indice_dia] += cantidad
        else:
            raise IndexError("Índice de técnico o día fuera del rango válido de la matriz.")

    def obtener_pico_de_carga(self) -> Dict:
        if not self._tecnicos:
            return {"Tecnico": "N/A", 
                    "Día": "N/A", 
                    "Máx_carga": 0}
        max_carga = -1
        idx_tec_max = 0
        idx_dia_max = 0
        for i in range(len(self._tecnicos)):
            for j in range(len(self.DIAS_SEMANA)):
                if self._matriz[i][j] > max_carga:
                    max_carga = self._matriz[i][j]
                    idx_tec_max = i
                    idx_dia_max = j
        return {
            "Técnico": self._tecnicos[idx_tec_max].nombreCompleto,
            "Día": self.DIAS_SEMANA[idx_dia_max],
            "Máx_carga": max_carga
        }

    def obtener_matriz_completa(self) -> Tuple[List[str], List[str], List[List[int]]]:
        nombres_tecnicos = [t.nombreCompleto for t in self._tecnicos]
        return nombres_tecnicos, self.DIAS_SEMANA, self._matriz