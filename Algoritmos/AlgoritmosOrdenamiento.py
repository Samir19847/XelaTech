from typing import List, Callable, Any

class AlgoritmosOrdenamiento:

    BUBBLE_SORT = "Bubble Sort"
    SELECTION_SORT = "Selection Sort"
    SHELL_SORT = "Shell Sort"
    QUICK_SORT = "Quick Sort"
    @staticmethod
    def exigir_datos_suficientes(lista: List[Any], minimo: int = 2, que: str = "elementos"):
        """Antes de ordenar hay que comprobar que existan datos suficientes."""
        if len(lista) < minimo:
            raise ValueError(
                f"Datos insuficientes para ordenar: se necesitan al menos {minimo} {que} "
                f"y hay {len(lista)}."
            )

    @staticmethod
    def bubble_sort(lista: List[Any],
                    key: Callable[[Any], Any] = lambda x: x,
                    descendente: bool = False) -> List[Any]:
        if len(lista) < 2:
            return lista.copy()
        n = len(lista)
        lista_ordenada = lista.copy()
        for i in range(n):
            intercambio = False
            for j in range(0, n - i - 1):
                valor_actual = key(lista_ordenada[j])
                valor_siguiente = key(lista_ordenada[j + 1])
                condicion = valor_actual < valor_siguiente if descendente else valor_actual > valor_siguiente
                if condicion:
                    lista_ordenada[j], lista_ordenada[j + 1] = lista_ordenada[j + 1], lista_ordenada[j]
                    intercambio = True
            if not intercambio:
                break
        return lista_ordenada

    @staticmethod
    def selection_sort(lista: List[Any],
                       key: Callable[[Any], Any] = lambda x: x,
                       descendente: bool = False) -> List[Any]:
        lista_ordenada = lista.copy()
        n = len(lista_ordenada)
        for i in range(n - 1):
            indice_extremo = i
            for j in range(i + 1, n):
                candidato = key(lista_ordenada[j])
                actual = key(lista_ordenada[indice_extremo])
                if (candidato > actual) if descendente else (candidato < actual):
                    indice_extremo = j
            if indice_extremo != i:
                lista_ordenada[i], lista_ordenada[indice_extremo] = lista_ordenada[indice_extremo], lista_ordenada[i]
        return lista_ordenada

    @staticmethod
    def shell_sort(lista: List[Any],
                   key: Callable[[Any], Any] = lambda x: x,
                   descendente: bool = False) -> List[Any]:
        if len(lista) < 2:
            return lista.copy()
        n = len(lista)
        lista_ordenada = lista.copy()
        brecha = n // 2
        while brecha > 0:
            for i in range(brecha, n):
                temp = lista_ordenada[i]
                valor_temp = key(temp)
                j = i
                while j >= brecha:
                    valor_comparacion = key(lista_ordenada[j - brecha])
                    condicion = valor_comparacion < valor_temp if descendente else valor_comparacion > valor_temp
                    if condicion:
                        lista_ordenada[j] = lista_ordenada[j - brecha]
                        j -= brecha
                    else:
                        break
                lista_ordenada[j] = temp
            brecha //= 2
        return lista_ordenada

    @staticmethod
    def quick_sort(lista: List[Any],
                   key: Callable[[Any], Any] = lambda x: x,
                   descendente: bool = False) -> List[Any]:
        lista_ordenada = lista.copy()
        AlgoritmosOrdenamiento._quick_rec(lista_ordenada, 0, len(lista_ordenada) - 1, key, descendente)
        return lista_ordenada

    @staticmethod
    def _quick_rec(datos: List[Any], bajo: int, alto: int,
                   key: Callable[[Any], Any], descendente: bool):
        if bajo >= alto:
            return
        medio = (bajo + alto) // 2
        datos[medio], datos[alto] = datos[alto], datos[medio] 
        pivote = key(datos[alto])
        frontera = bajo
        for j in range(bajo, alto):
            valor = key(datos[j])
            if (valor > pivote) if descendente else (valor < pivote):
                datos[frontera], datos[j] = datos[j], datos[frontera]
                frontera += 1
        datos[frontera], datos[alto] = datos[alto], datos[frontera]  # el pivote queda en su lugar definitivo
        AlgoritmosOrdenamiento._quick_rec(datos, bajo, frontera - 1, key, descendente)
        AlgoritmosOrdenamiento._quick_rec(datos, frontera + 1, alto, key, descendente)

    @staticmethod
    def describir_ordenamiento(algoritmo: str, criterio: str, descendente: bool) -> str:
        orden = "descendente" if descendente else "ascendente"
        return f"Algoritmo: {algoritmo} | Criterio: {criterio} | Orden: {orden}"
