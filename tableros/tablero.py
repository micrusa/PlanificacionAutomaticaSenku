from .tablero_1 import generar_tablero_1

# from .tablero_2 import generar_tablero_2
from .tablero_3 import generar_tablero_3
from .tablero_4 import generar_tablero_4
from .tablero_5 import generar_tablero_5

# Devuelve el tablero como una tupla (lista_casillas, hueco_inicial, objetivo, num_tablero)
def tablero(N):
    if N == 1:
        return generar_tablero_1()
    elif N == 2:
        # return generar_tablero_2()
        pass
    elif N == 3:
        return generar_tablero_3()
    elif N == 4:
        return generar_tablero_4()
    elif N == 5:
        return generar_tablero_5()
    # The 'else' block here is equivalent to 'case _'
    else:
        pass
    return (None, None, None, None)

def todos_los_tableros():
    return [tablero(N) for N in [1, 3, 4, 5]]
