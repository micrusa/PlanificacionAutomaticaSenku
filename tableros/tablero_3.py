def generar_tablero_3():
    lista_casillas = []
    for fila in range(1, 9):
        for col in range(1, 9):
            if (fila in [1, 2, 3, 7, 8]) and (col in [1, 2, 3, 7, 8]):
                continue
            lista_casillas.append((fila, col))

    hueco_inicial = (4, 5)

    return (lista_casillas, hueco_inicial)