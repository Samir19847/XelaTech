def leer_entero(texto: str, campo: str) -> int:
    try:
        return int(texto.strip())
    except ValueError:
        raise ValueError(f"{campo} debe ser un número entero.")


def leer_decimal(texto: str, campo: str) -> float:
    try:
        return float(texto.strip())
    except ValueError:
        raise ValueError(f"{campo} debe ser un número (por ejemplo 125.50).")