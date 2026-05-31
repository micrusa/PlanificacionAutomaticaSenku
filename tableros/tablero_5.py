def generar_tablero_5():
    lista_casillas = []

    for fila in range(1, 10):
        for col in range(1, 10):
            # No se incluyen aquellas en las que la suma de las distancias al centro en cada uno de los ejes sea mayor que 4:
            if abs(fila - 5) + abs(col - 5) > 4:
                continue
            lista_casillas.append((fila, col))

    hueco_inicial = (5, 5)
    objetivo = (5,5)

    return (lista_casillas, hueco_inicial, objetivo, 5)