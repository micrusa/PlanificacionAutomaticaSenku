import glob
import math
import os
import re

from unified_planning.io import PDDLReader

from guardador_soluciones import guardar_solucion


# Calcula el valor de la heurística pagoda para un estado
# estado: Problem de unified_planning
# pagoda_values: diccionario de Casilla a float
def heuristica_pagoda(estado, pagoda_values):
    valor = 0
    ocupada = next(f for f in estado.fluents if f.name.lower() == "ocupada")
    for obj in pagoda_values:
        if estado.initial_value(ocupada(obj)).is_true():
            valor += pagoda_values[obj]
    return valor


# Genera los estados sucesores válidos junto con la acción realizada
# estado: Problem de unified_planning
# movimientos_validos: lista de tuplas (de, sobre, a)
def obtener_sucesores(estado, movimientos_validos):
    sucesores = []
    ocupada = next(f for f in estado.fluents if f.name.lower() == "ocupada")

    for de, sobre, a in movimientos_validos:
        if (
            estado.initial_value(ocupada(de)).is_true()
            and estado.initial_value(ocupada(sobre)).is_true()
            and not estado.initial_value(ocupada(a)).is_true()
        ):
            nuevo_estado = estado.clone()
            nuevo_estado.set_initial_value(ocupada(de), False)
            nuevo_estado.set_initial_value(ocupada(sobre), False)
            nuevo_estado.set_initial_value(ocupada(a), True)

            accion = f"saltar({de.name}, {sobre.name}, {a.name})"
            sucesores.append((nuevo_estado, accion))

    return sucesores


# Comprueba si un estado cumple con el objetivo de tener una única ficha en el objetivo
# estado: Problem de unified_planning
# casilla_objetivo: tupla (x,y)
def es_objetivo(estado, casilla_objetivo):
    ocupada = next(f for f in estado.fluents if f.name.lower() == "ocupada")
    tipo_casilla = next(ut for ut in estado.user_types if ut.name.lower() == "casilla")
    casillas = estado.objects(tipo_casilla)
    for c in casillas:
        coords = tuple(map(int, c.name.split("_")[1:]))
        es_ocupada = estado.initial_value(ocupada(c)).is_true()
        if coords == casilla_objetivo:
            if not es_ocupada:
                return False
        else:
            if es_ocupada:
                return False
    return True


# Búsqueda Beam Search usando la heurística de Pagoda
def beam_search(problema_inicial, ancho_beam=40):
    # Encontramos la casilla objetivo desde el goal (que puede ser un And complejo en PDDL)
    casilla_objetivo = None
    comp_goals = problema_inicial.goals
    if len(comp_goals) == 1 and comp_goals[0].is_and():
        comp_goals = comp_goals[0].args

    for goal in comp_goals:
        if goal.is_fluent_exp():
            casilla_objetivo = goal.arg(0).constant_value()
            break

    x_g, y_g = map(int, casilla_objetivo.name.split("_")[1:])
    objetivo_coords = (x_g, y_g)

    # Obtenemos los fluentes y tipos de manera insensible a mayúsculas
    ocupada = next(f for f in problema_inicial.fluents if f.name.lower() == "ocupada")
    movimiento_valido = next(
        f for f in problema_inicial.fluents if f.name.lower() == "movimiento_valido"
    )
    tipo_casilla = next(
        ut for ut in problema_inicial.user_types if ut.name.lower() == "casilla"
    )

    casillas = list(problema_inicial.objects(tipo_casilla))

    # Precomputamos los movimientos válidos (estáticos)
    movimientos_validos = []
    for de in casillas:
        for sobre in casillas:
            for a in casillas:
                if problema_inicial.initial_value(
                    movimiento_valido(de, sobre, a)
                ).is_true():
                    movimientos_validos.append((de, sobre, a))

    # Precomputamos los valores de la pagoda específicos para este tablero
    phi = (math.sqrt(5) - 1) / 2
    pagoda_values = {}
    for c in casillas:
        x, y = map(int, c.name.split("_")[1:])
        pagoda_values[c] = phi ** (abs(x - x_g) + abs(y - y_g))

    # El beam contiene tuplas (estado, plan, valor_heuristico)
    beam = [(problema_inicial, [], -heuristica_pagoda(problema_inicial, pagoda_values))]

    for i in range(100):
        for estado, plan, _ in beam:
            if es_objetivo(estado, objetivo_coords):
                return plan

        candidatos = []
        for estado_actual, plan, _ in beam:
            sucesores = obtener_sucesores(estado_actual, movimientos_validos)
            for sucesor, accion in sucesores:
                nuevo_plan = plan + [accion]
                h_val = -heuristica_pagoda(sucesor, pagoda_values)
                candidatos.append((sucesor, nuevo_plan, h_val))

        if not candidatos:
            return None

        candidatos.sort(key=lambda x: x[2])

        # Eliminamos duplicados para diversificar la búsqueda
        vistos = set()
        beam = []
        for estado, plan, h in candidatos:
            ocupadas = tuple(
                c.name for c in casillas if estado.initial_value(ocupada(c)).is_true()
            )
            if ocupadas not in vistos:
                vistos.add(ocupadas)
                beam.append((estado, plan, h))
                if len(beam) == ancho_beam:
                    break

    return None


if __name__ == "__main__":
    import time

    anchos = [5, 10, 20, 40, 80, 160, 320, 640, 1280]
    reader = PDDLReader()

    # Buscamos todos los archivos de problemas en la carpeta pddl
    archivos_problemas = glob.glob("pddl/problema_*.pddl")
    archivos_problemas.sort()

    for ruta_problema in archivos_problemas:
        nombre_archivo = os.path.basename(ruta_problema)
        match = re.search(r"problema_(\d+)\.pddl", nombre_archivo)
        if match:
            num_tablero = int(match.group(1))
        else:
            continue

        print(
            f"\nResolviendo Tablero {num_tablero} con Beam Search (desde {nombre_archivo})..."
        )
        problema_inicial = reader.parse_problem("pddl/dominio.pddl", ruta_problema)

        for ancho in anchos:
            inicio = time.time()
            plan = beam_search(problema_inicial, ancho_beam=ancho)
            tiempo = time.time() - inicio
            if plan:
                print(f"  Ancho {ancho:2d}: Solución encontrada de {len(plan)} pasos. ({tiempo:.4f}s)")
                guardar_solucion("beam-search", num_tablero, plan, ancho_beam=ancho, tiempo_segundos=tiempo)
                break
            else:
                print(f"  Ancho {ancho:2d}: No se encontró solución. ({tiempo:.4f}s)")
            guardar_solucion("beam-search", num_tablero, plan, ancho_beam=ancho, tiempo_segundos=tiempo)

