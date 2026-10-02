from typing import List, Callable, Any

class AlgoritmosOrdenamiento:
    @staticmethod
    def bubble_sort(lista: List[Any], key: Callable[[Any], Any] = lambda x: x, descendente: bool = False) -> List[Any]:
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
    def shell_sort(lista: List[Any], key: Callable[[Any], Any] = lambda x: x, descendente: bool = False) -> List[Any]:
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