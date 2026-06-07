import os


# Guarda el plan de movimientos de la solución en un archivo de texto
# metodo: 'beam-search' o 'fast-downward'
# num_tablero: int (1, 3, 4, 5)
# plan: lista de strings o None
# ancho_beam: int (opcional, solo para beam-search)
def guardar_solucion(metodo, num_tablero, plan, ancho_beam=None):
    os.makedirs(f"soluciones/{metodo}", exist_ok=True)

    if metodo == "beam-search":
        nombre_archivo = f"soluciones/beam-search/tablero_{num_tablero}_ancho_{ancho_beam}.txt"
    else:
        nombre_archivo = f"soluciones/fast-downward/tablero_{num_tablero}.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        if plan:
            f.write(f"Longitud del plan: {len(plan)} movimientos.\n")
            for i, accion in enumerate(plan):
                f.write(f"{i + 1:2d}: {accion}\n")
        else:
            f.write("No se encontró solución.\n")
