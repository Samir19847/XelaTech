from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView
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


def crear_tabla(encabezados) -> QTableWidget:
    tabla = QTableWidget(0, len(encabezados))
    tabla.setHorizontalHeaderLabels(encabezados)
    tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return tabla
def codigo_seleccionado(tabla):
    fila = tabla.currentRow()
    if fila < 0:
        return None
    item = tabla.item(fila, 0)
    return item.text() if item is not None else None

def llenar_tabla(tabla, filas, encabezados=None):
    anterior = codigo_seleccionado(tabla) if encabezados is None else None
    if encabezados is not None:
        tabla.setColumnCount(len(encabezados))
        tabla.setHorizontalHeaderLabels(encabezados)
    tabla.setRowCount(len(filas))
    for fila, valores in enumerate(filas):
        for columna, valor in enumerate(valores):
            tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
    if anterior is not None:
        for fila, valores in enumerate(filas):
            if str(valores[0]) == anterior:
                tabla.selectRow(fila)
                break

def con_seleccion(ventana, tabla, accion):
    codigo = codigo_seleccionado(tabla)
    if codigo is None:
        QMessageBox.warning(ventana, "Selecciona una solicitud", "Primero haz clic en una fila de la tabla.")
        return False, None
    try:
        return True, accion(codigo)
    except ValueError as error:
        QMessageBox.warning(ventana, "No se pudo realizar la acción", str(error))
        return False, None
