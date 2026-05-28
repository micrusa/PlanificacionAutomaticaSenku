def generar_tablero_4():
    lista_casillas = []
    for fila in range(1, 8):
        for col in range(1, 8):
            if (fila in [1, 2, 6, 7]) and (col in [1, 2, 6, 7]):
                continue
            lista_casillas.append((fila, col))

    hueco_inicial = (4, 4)

    return (lista_casillas, hueco_inicial)