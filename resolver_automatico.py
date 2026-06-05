from unified_planning.shortcuts import OneshotPlanner
from modelador import modelar
from tableros.tablero import todos_los_tableros

# 1. Elegimos un tablero para probar. 
tablero_info = todos_los_tableros()[1]
if tablero_info and all(tablero_info):
    lista_casillas, hueco_inicial, objetivo, num_tablero = tablero_info
else:
    print("Error: No se pudo cargar la información del tablero.")
    exit()

# 2. Genera el problema en memoria usando el modelador
problema = modelar(lista_casillas, hueco_inicial, objetivo)

print("==================================================")
print(f"El problema del Senku (Tablero {num_tablero}) ha sido modelado.")
print(f"Tipo de problema: {problema.kind}")
print("==================================================")

# 3. Usamos el planificador 'fast-downward' que es compatible con el modelo
with OneshotPlanner(name='fast-downward') as planner:
    print(f"Planificador seleccionado: {planner.name}")
    
    # Comprobamos si el planificador puede resolver este tipo de problema
    if planner.supports(problema.kind):
        print("El planificador es compatible. Resolviendo...")
        
        # Resolvemos el problema
        result = planner.solve(problema)

        # 4. Imprimimos el resultado
        if result.plan:
            print("\n¡Solución encontrada!")
            print(f"Longitud del plan: {len(result.plan.actions)} movimientos.")
            for i, action in enumerate(result.plan.actions):
                print(f"{i+1:2d}: {action}")
        else:
            print("\nNo se encontró solución.")
            print(f"Razón del fallo: {result.status.name}")

    else:
        print("El planificador seleccionado no es compatible con el problema.")
