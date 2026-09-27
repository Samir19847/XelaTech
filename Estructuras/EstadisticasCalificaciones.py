from typing import List, Dict

class EstadisticasCalificaciones:
    def __init__(self):
        self._calificaciones: List[int] = [0,0,0,0,0]

    def RegistrarCalificaciones(self, estrellas:int):
        if 1<= estrellas <=5:
            self._calificaciones[estrellas - 1] += 1
        else:
            raise ValueError("La calificación debe estar comprendida entre 1 y 5 estrellas.")

    def ObtenerPromedio(self) -> float:
        totalVotos= sum(self._calificaciones)
        if totalVotos==0:
            return 0.0

        sumaPromedio=sum(
            (i+1)*cantidad
            for i, cantidad in enumerate(self._calificaciones)
        )
        return round(sumaPromedio / totalVotos, 2)

    def ObtenerResumenConteo(self)->Dict[str, int]:
        return {
            f"{i+1}_estrellas": self._calificaciones[i]
            for i in range(5)
        }

    def ObtenerArreglo(self)->List[int]:
        return list(self._calificaciones)
