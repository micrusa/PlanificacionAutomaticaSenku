from .tablero_4 import generar_tablero_4


def generar_tablero_1():
    # Es el tablero 4 pero añadiendo las casillas [2,2], [6,2], [2,6], [6,6] y cambiando la posición inicial
    lista_casillas, hueco_inicial, objetivo, i = generar_tablero_4()
    lista_casillas.extend([(2, 2), (6, 2), (2, 6), (6, 6)])

    return (lista_casillas, (4, 3), (4,5), 1)
