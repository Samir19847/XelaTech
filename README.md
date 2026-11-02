# XelaTech Soporte

Sistema de gestión de solicitudes de soporte técnico para el taller **XelaTech**, desarrollado en **Python** con interfaz gráfica **PyQt6**.
Permite registrar clientes, técnicos, equipos y repuestos; crear solicitudes de servicio; atenderlas mediante colas con prioridad; llevar el diagnóstico, el uso de repuestos y la entrega con calificación; y consultar 12 reportes con ordenamientos y búsquedas programados a mano.

---

## Requisitos

- Python 3.10 o superior
- PyQt6

```bash
pip install -r requirements.txt
```

## Cómo ejecutarlo

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

Los datos viven en memoria mientras el programa está abierto.

---

---

## Demostración rápida
Para probar el programa rápidamente, usa la pestaña **Datos de prueba**.
1. Abre la pestaña **Datos de prueba**, deja 8 solicitudes y pulsa **Generar**.
2. En **Atención**, revisa las colas y pulsa **Atender siguiente**.
3. Selecciona una solicitud y avánzala: diagnóstico → repuesto → reparación → lista → entregar con calificación.
4. En **Reportes y búsquedas**, genera los reportes y prueba el 11 con distintos criterios.

---



## Pestañas de la interfaz

| Pestaña | Qué se hace ahí |
|---|---|
| **Clientes** | Registrar clientes (Individual, Corporativo, Frecuente) y ver su cantidad de solicitudes |
| **Técnicos** | Registrar técnicos por especialidad y cambiar su disponibilidad |
| **Repuestos** | Registrar repuestos con existencia, mínimo, costo y precio; se marcan los agotados y los que están bajo el mínimo |
| **Equipos** | Registrar portátiles, equipos de escritorio, impresoras y consolas, cada uno con su dato propio |
| **Solicitudes** | Crear solicitudes, ponerlas en cola o cancelarlas |
| **Atención** | Ver las colas urgente y normal, atender la siguiente, avanzar estados, registrar diagnóstico, usar repuestos, entregar con calificación, deshacer el último cambio, ver el historial y cancelar |
| **Reportes y búsquedas** | Generar los reportes 1 al 12; ordenar ascendente o descendente los reportes 6, 7 y 8; hacer búsquedas |
| **Datos de prueba** | Generar solicitudes de ejemplo con `Random` (con semilla opcional) y ver las estadísticas de calificaciones |

---

### Estructuras de datos

| Estructura | Dónde se usa |
|---|---|
| **Listas** | Clientes, técnicos, equipos, solicitudes y repuestos en el gestor |
| **Colas (FIFO)** | Dos colas: urgente y normal. Las urgentes se atienden primero |
| **Pila** | Historial de estados de cada solicitud para deshacer el último cambio |
| **Arreglo de una dimensión** | Estadísticas de calificaciones (5 posiciones, una por estrella) y conteos de reportes |
| **Matriz** | Carga semanal: técnicos × días (lunes a viernes) |
| **Random** | `random.Random` con semilla opcional en el generador de datos |

### Algoritmos (sin `sort`, `sorted` ni funciones de ordenamiento del lenguaje)

| Algoritmo | Uso |
|---|---|
| **Bubble Sort** | Solicitudes por costo total |
| **Selection Sort** | Técnicos por servicios finalizados |
| **Shell Sort** | Repuestos por existencia (y códigos para la búsqueda binaria) |
| **Quick Sort** | Solicitudes por fecha y hora de recepción |
| **Búsqueda secuencial** | Clientes por nombre, solicitudes por estado y equipos por marca (parcial o exacta) |
| **Búsqueda binaria** | Solicitud por código; los datos se ordenan antes por el mismo campo |

---

## Reglas del negocio

**Estados de una solicitud**: Recibida → En espera → Asignada → En diagnóstico → En reparación → Lista para entregar → Entregada. Puede cancelarse hasta la etapa de diagnóstico; una vez en reparación ya no.

- Un equipo solo puede tener **una solicitud activa** a la vez.
- Una solicitud solo se crea para un **equipo que pertenezca al cliente** indicado.
- El técnico asignado debe tener la **especialidad** que requiere el equipo, estar **disponible** y no tener la carga completa; entre varios, se elige al que tiene menos trabajos activos.
- Las solicitudes **urgentes** se atienden antes que las normales; dentro de cada cola, por orden de llegada.
- Si la solicitud al frente de la cola no tiene técnico disponible, **se queda en la cola** y se informa; no se pierde.
- Cada asignación se anota en la **matriz de carga semanal** (sábado y domingo cuentan como lunes).
- Los **repuestos** solo se usan en diagnóstico o reparación; se descuentan de la existencia y se avisa cuando quedan en el mínimo o agotados.
- Para pasar a reparación o a "Lista para entregar" debe haber un **diagnóstico**.
- La **entrega** solo se hace desde "Lista para entregar" y exige una calificación **entera de 1 a 5**; solo en ese momento cambian las estadísticas del técnico.
- Las solicitudes entregadas o canceladas **ya no se pueden modificar**.
- Deshacer el último cambio restaura el estado anterior (y ajusta la cola y la matriz cuando corresponde).

### Validaciones adicionales (propias del proyecto)

1. Los repuestos solo pueden usarse en los estados En diagnóstico o En reparación.
2. La calificación debe ser un entero entre 1 y 5.
3. Solo se entrega una solicitud que esté en "Lista para entregar".
4. El estado "Asignada" solo se alcanza asignando un técnico (nunca a mano).
5. El equipo debe pertenecer al cliente de la solicitud.
6. El precio de venta de un repuesto no puede ser menor que su costo.
7. Se exige un diagnóstico antes de reparar o dejar lista una solicitud.

---
