from unified_planning.shortcuts import OneshotPlanner
from modelador import modelar
from tableros.tablero import todos_los_tableros
from guardador_soluciones import guardar_solucion


# Resuelve todos los tableros usando el planificador Oneshot fast-downward
def resolver_todos():
    tableros = todos_los_tableros()

    with OneshotPlanner(name="fast-downward") as planner:
        for tablero_info in tableros:
            lista_casillas, hueco_inicial, objetivo, num_tablero = tablero_info
            print(f"\nResolviendo Tablero {num_tablero} con Fast-Downward...")

            problema = modelar(lista_casillas, hueco_inicial, objetivo)

            if planner.supports(problema.kind):
                result = planner.solve(problema, timeout=30)

                if result.plan:
                    print(f"  Solución encontrada de {len(result.plan.actions)} pasos.")
                    plan = [str(action) for action in result.plan.actions]
                else:
                    print("  No se encontró solución.")
                    plan = None

                guardar_solucion("fast-downward", num_tablero, plan)
            else:
                print("  El planificador no soporta este tipo de problema.")
                guardar_solucion("fast-downward", num_tablero, None)


if __name__ == "__main__":
    resolver_todos()
