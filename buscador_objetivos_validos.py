import os
from unified_planning.shortcuts import OneshotPlanner
from modelador import modelar
from tableros.tablero import todos_los_tableros


# Busca y guarda las casillas objetivo válidas para cada tablero
def buscar_objetivos_validos():
    tableros = todos_los_tableros()
    os.makedirs("soluciones/casillas_objetivo_validas", exist_ok=True)

    with OneshotPlanner(name="fast-downward") as planner:
        for tablero_info in tableros:
            lista_casillas, hueco_inicial, objetivo_default, num_tablero = tablero_info
            print(f"\nBuscando objetivos válidos para Tablero {num_tablero}...")

            validos = []
            # Probamos cada casilla de la lista como objetivo
            for c in lista_casillas:
                problema = modelar(lista_casillas, hueco_inicial, c)

                if planner.supports(problema.kind):
                    # Usamos un timeout corto de 3 segundos por intento
                    result = planner.solve(problema, timeout=3)
                    if result.plan:
                        print(f"  Casilla {c} es VÁLIDA")
                        validos.append(c)
                    else:
                        print(f"  Casilla {c} es INVÁLIDA")
                else:
                    print(f"  El planificador no soporta este tipo de problema.")
                    break

            # Guardamos los resultados
            nombre_archivo = f"soluciones/casillas_objetivo_validas/tablero_{num_tablero}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(f"Longitud de la lista: {len(validos)} casillas.\n")
                for i, coord in enumerate(validos):
                    f.write(f"{i + 1:2d}: ({coord[0]}, {coord[1]})\n")


if __name__ == "__main__":
    buscar_objetivos_validos()
