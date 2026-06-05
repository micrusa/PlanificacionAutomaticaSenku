from unified_planning.shortcuts import *
from modelador import modelar
from tableros.tablero import todos_los_tableros

# --- PASO 1: Implementa tu Heurística (Función Pagoda) ---
# Necesitarás un mapa de coordenadas a valores de la pagoda
# Ejemplo para un tablero simple. Deberás crear los tuyos.
PAGODA_VALUES = {
    (0,0): 1, (0,1): 2, (0,2): 1,
    (1,0): 2, (1,1): 3, (1,2): 2,
    (2,0): 1, (2,1): 2, (2,2): 1,
}

def heuristica_pagoda(estado: Problem):
    """Calcula el valor heurístico de un estado (problema)."""
    valor = 0
    # El fluente 'ocupada' está en el problema
    ocupada_fluent = estado.fluent("ocupada")
    for obj in estado.objects(estado.user_type("Casilla")):
        # Si la casilla está ocupada en el estado actual...
        if estado.initial_value(ocupada_fluent(obj)):
            # Extraemos las coordenadas del nombre del objeto 'c_x_y'
            coords = tuple(map(int, obj.name.split('_')[1:]))
            valor += PAGODA_VALUES.get(coords, 0) # Sumamos su valor pagoda
    return valor

# --- PASO 2: Implementa la Lógica de Sucesores ---
def obtener_sucesores(estado: Problem):
    """Genera todos los estados posibles a partir del estado actual."""
    sucesores = []
    accion_saltar = estado.action("saltar")
    
    # Iteramos sobre todas las combinaciones de 3 casillas
    # Esto es ineficiente, pero es un punto de partida.
    # Una mejora sería iterar solo sobre los 'movimiento_valido'
    casillas = list(estado.objects(estado.user_type("Casilla")))
    
    from itertools import permutations
    for p in permutations(casillas, 3):
        de, sobre, a = p
        # Construimos la acción concreta
        accion_concreta = accion_saltar(de, sobre, a)
        
        # Comprobamos si las precondiciones se cumplen en el estado actual
        es_aplicable = True
        for precondicion in accion_concreta.action.preconditions:
            # Simplificación: esto necesita una evaluación más robusta
            # Pero para este modelo, podemos comprobar los valores iniciales
            if not estado.initial_value(precondicion.arg(0) if precondicion.is_not() else precondicion):
                es_aplicable = False
                break
        
        if es_aplicable:
            # Si es aplicable, creamos el nuevo estado
            nuevo_estado = estado.clone()
            # Aplicamos los efectos de la acción al nuevo estado
            for efecto in accion_concreta.action.effects:
                nuevo_estado.set_initial_value(efecto.fluent, efecto.value)
            sucesores.append(nuevo_estado)
            
    return sucesores # Esta función es compleja, es el corazón del motor

# --- PASO 3: El Bucle Principal de Beam Search ---
def beam_search(problema_inicial, ancho_beam=10):
    """Algoritmo de Búsqueda en Haz."""
    
    # La "viga" (beam) es una lista de tuplas (estado, heuristica)
    beam = [(problema_inicial, heuristica_pagoda(problema_inicial))]

    for i in range(100): # Límite de profundidad para no entrar en bucles infinitos
        print(f"Profundidad: {i}, Ancho del Beam: {len(beam)}")
        
        candidatos = []
        for estado_actual, _ in beam:
            # Comprobamos si el estado actual es un objetivo
            if estado_actual.goals[0].is_true(): # Simplificación
                 print("¡Solución encontrada!")
                 return estado_actual # Devolvemos el estado final

            # Generamos todos los sucesores del estado actual
            # ¡Esta es la función que tienes que implementar con cuidado!
            sucesores = obtener_sucesores(estado_actual)
            for sucesor in sucesores:
                candidatos.append((sucesor, heuristica_pagoda(sucesor)))

        if not candidatos:
            print("No hay más movimientos posibles.")
            return None

        # Ordenamos todos los candidatos por su valor heurístico (menor es mejor)
        candidatos.sort(key=lambda x: x[1])
        
        # Nos quedamos con los 'N' mejores para la siguiente iteración
        beam = candidatos[:ancho_beam]

    print("Límite de profundidad alcanzado. No se encontró solución.")
    return None

# --- Ejecución ---
if __name__ == "__main__":
    # 1. Elige un tablero
    tablero_info = todos_los_tableros()[0] # Ejemplo con el primer tablero
    lista_casillas, hueco_inicial, objetivo, _ = tablero_info

    # 2. Modela el problema inicial
    problema_inicial = modelar(lista_casillas, hueco_inicial, objetivo)

    # 3. Ejecuta la búsqueda
    solucion = beam_search(problema_inicial, ancho_beam=5)