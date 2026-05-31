from unified_planning.io import PDDLWriter
from unified_planning.shortcuts import *


# Modela el problema
# casillas: lista de tuplas (x,y)
# casilla_inicial: tupla (x,y)
# casilla_objetivo: tupla (x,y)
# Siendo x la fila e y la columna
def modelar(casillas_coord, casilla_inicial, casilla_objetivo):
    problema = Problem("Senku")

    Casilla = UserType("Casilla")
    problema.user_types.append(Casilla)

    # Creamos un diccionario para acceder rápidamente a las casillas por coordenadas
    casillas = {}
    for x, y in casillas_coord:
        obj_casilla = Object(f"c_{x}_{y}", Casilla)
        problema.add_object(obj_casilla)
        casillas[(x, y)] = obj_casilla

    ocupada = Fluent("ocupada", BoolType(), casilla=Casilla)
    problema.add_fluent(ocupada, default_initial_value=True)
    problema.set_initial_value(ocupada(casillas[casilla_inicial]), False)

    movimiento_valido = Fluent(
        "movimiento_valido", BoolType(), de=Casilla, sobre=Casilla, a=Casilla
    )
    problema.add_fluent(movimiento_valido, default_initial_value=False)

    # Hacemos válidos los movimientos en los que estén alineadas las tres casillas y sobre esté entre de y a
    # En ambas direcciones
    for x, y in casillas_coord:
        if (x, y + 1) in casillas and (x, y + 2) in casillas:
            c_de = casillas[(x, y)]
            c_sobre = casillas[(x, y + 1)]
            c_a = casillas[(x, y + 2)]
            problema.set_initial_value(movimiento_valido(c_de, c_sobre, c_a), True)
            problema.set_initial_value(movimiento_valido(c_a, c_sobre, c_de), True)

        if (x + 1, y) in casillas and (x + 2, y) in casillas:
            c_de = casillas[(x, y)]
            c_sobre = casillas[(x + 1, y)]
            c_a = casillas[(x + 2, y)]
            problema.set_initial_value(movimiento_valido(c_de, c_sobre, c_a), True)
            problema.set_initial_value(movimiento_valido(c_a, c_sobre, c_de), True)

    saltar = InstantaneousAction("saltar", de=Casilla, sobre=Casilla, a=Casilla)
    de = saltar.de
    sobre = saltar.sobre
    a = saltar.a

    saltar.add_precondition(movimiento_valido(de, sobre, a))
    saltar.add_precondition(ocupada(de))
    saltar.add_precondition(ocupada(sobre))
    saltar.add_precondition(Not(ocupada(a)))

    saltar.add_effect(ocupada(de), False)
    saltar.add_effect(ocupada(sobre), False)
    saltar.add_effect(ocupada(a), True)

    problema.add_action(saltar)

    for x, y in casillas_coord:
        casilla = casillas[(x, y)]
        if x == casilla_objetivo[0] and y == casilla_objetivo[1]:
            problema.add_goal(ocupada(casilla))
        else:
            problema.add_goal(Not(ocupada(casilla)))

    return problema
