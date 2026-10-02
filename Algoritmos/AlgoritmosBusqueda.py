from typing import List, Callable, Any, Optional

class AlgoritmosBusqueda:

    @staticmethod
    def busqueda_secuencial(lista: List[Any], termino_busqueda: str, key: Callable[[Any], str], busqueda_parcial: bool = True) -> List[Any]:
        resultados = []
        termino_busqueda = termino_busqueda.lower()
        
        for elemento in lista:
            valor_elemento = str(key(elemento)).lower()
            
            if busqueda_parcial:
                if termino_busqueda in valor_elemento:
                    resultados.append(elemento)
            else:
                if termino_busqueda == valor_elemento:
                    resultados.append(elemento)
                    
        return resultados

    @staticmethod
    def busqueda_binaria(lista: List[Any], codigo_buscado: Any, key: Callable[[Any], Any]) -> Optional[Any]:
        izquierda = 0
        derecha = len(lista) - 1
        
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            valor_medio = key(lista[medio])
            
            if valor_medio == codigo_buscado:
                return lista[medio]
                
            elif valor_medio < codigo_buscado:
                izquierda = medio + 1 
                
            else:
                derecha = medio - 1 
                
        return None 