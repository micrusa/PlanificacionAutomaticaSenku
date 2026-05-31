from .tablero_1 import generar_tablero_1

# from .tablero_2 import generar_tablero_2
from .tablero_3 import generar_tablero_3
from .tablero_4 import generar_tablero_4
from .tablero_5 import generar_tablero_5

# Devuelve el tablero como una tupla (lista_casillas, hueco_inicial, objetivo, num_tablero)
def tablero(N):
    match N:
        case 1:
            return generar_tablero_1()
        case 2:
            # return generar_tablero_2()
            pass
        case 3:
            return generar_tablero_3()
        case 4:
            return generar_tablero_4()
        case 5:
            return generar_tablero_5()
        case _:
            pass
    return (None, None, None, None)


def todos_los_tableros():
    return [tablero(N) for N in [1, 3, 4, 5]]
