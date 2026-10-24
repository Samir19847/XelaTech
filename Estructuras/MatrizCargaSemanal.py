from typing import List, Tuple, Dict
from Entidades.Técnicos import Tecnico

class MatrizCargaSemanal:
    DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    def __init__(self, listaTecnicos: List[Tecnico]):
        self._tecnicos = list(listaTecnicos)
        self._matriz: List[List[int]] = [
            [0 for _ in range(len(self.DIAS_SEMANA))]
            for _ in range(len(self._tecnicos))
        ]

    def agregar_tecnico(self, tecnico: Tecnico) -> int:
        if not isinstance(tecnico, Tecnico):
            raise ValueError("El técnico debe ser una instancia de la clase Tecnico.")
        self._tecnicos.append(tecnico)
        self._matriz.append([0 for _ in range(len(self.DIAS_SEMANA))])
        return len(self._tecnicos) - 1

    def _validar_indices(self, indice_tecnico: int, indice_dia: int):
        if not (0 <= indice_tecnico < len(self._tecnicos) and 0 <= indice_dia < len(self.DIAS_SEMANA)):
            raise IndexError("Índice de técnico o día fuera del rango válido de la matriz.")

    def registrar_asignacion(self, indice_tecnico: int, indice_dia: int, cantidad: int = 1):
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un entero mayor o igual a 0.")
        self._validar_indices(indice_tecnico, indice_dia)
        self._matriz[indice_tecnico][indice_dia] += cantidad

    def quitar_asignacion(self, indice_tecnico: int, indice_dia: int, cantidad: int = 1):
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un entero mayor o igual a 0.")
        self._validar_indices(indice_tecnico, indice_dia)
        if self._matriz[indice_tecnico][indice_dia] < cantidad:
            raise ValueError("No hay tantas asignaciones para quitar en esa celda.")
        self._matriz[indice_tecnico][indice_dia] -= cantidad

    def obtener_pico_de_carga(self) -> Dict:
        max_carga = 0
        idx_tec_max = -1
        idx_dia_max = -1
        for i in range(len(self._tecnicos)):
            for j in range(len(self.DIAS_SEMANA)):
                if self._matriz[i][j] > max_carga:
                    max_carga = self._matriz[i][j]
                    idx_tec_max = i
                    idx_dia_max = j
        if idx_tec_max == -1:
            return {"Técnico": "N/A", "Día": "N/A", "Máx_carga": 0}
        return {
            "Técnico": self._tecnicos[idx_tec_max].nombreCompleto,
            "Día": self.DIAS_SEMANA[idx_dia_max],
            "Máx_carga": max_carga,
        }

    def totales_por_tecnico(self) -> List[int]:
        totales = []
        for fila in self._matriz:
            suma = 0
            for valor in fila:
                suma += valor
            totales.append(suma)
        return totales

    def totales_por_dia(self) -> List[int]:
        totales = [0 for _ in range(len(self.DIAS_SEMANA))]
        for fila in self._matriz:
            for j in range(len(self.DIAS_SEMANA)):
                totales[j] += fila[j]
        return totales

    @staticmethod
    def _indice_del_maximo(valores: List[int]) -> int:
        indice = -1
        mayor = 0
        for i in range(len(valores)):
            if valores[i] > mayor:
                mayor = valores[i]
                indice = i
        return indice

    def resumen_carga(self) -> Dict:
        por_tecnico = self.totales_por_tecnico()
        por_dia = self.totales_por_dia()
        it = self._indice_del_maximo(por_tecnico)
        idd = self._indice_del_maximo(por_dia)
        return {
            "Técnico": self._tecnicos[it].nombreCompleto if it >= 0 else "N/A",
            "Total_técnico": por_tecnico[it] if it >= 0 else 0,
            "Día": self.DIAS_SEMANA[idd] if idd >= 0 else "N/A",
            "Total_día": por_dia[idd] if idd >= 0 else 0,
        }

    def obtener_matriz_completa(self) -> Tuple[List[str], List[str], List[List[int]]]:
        nombres_tecnicos = [t.nombreCompleto for t in self._tecnicos]
        return nombres_tecnicos, list(self.DIAS_SEMANA), [fila.copy() for fila in self._matriz]