from tableros.tablero import todos_los_tableros


# Dibuja un tablero en consola de forma visual
# lista_casillas: lista de tuplas (x,y)
# hueco_inicial: tupla (x,y)
# num_tablero: int
def renderizar_tablero(lista_casillas, hueco_inicial, num_tablero):
    print(f"\n=== TABLERO {num_tablero} ===")

    # Encontramos los límites del tablero
    min_fila = min(x for x, y in lista_casillas)
    max_fila = max(x for x, y in lista_casillas)
    min_col = min(y for x, y in lista_casillas)
    max_col = max(y for x, y in lista_casillas)

    # Imprimimos columna por fila (y es la fila, x es la columna)
    for y in range(min_col, max_col + 1):
        linea = ""
        for x in range(min_fila, max_fila + 1):
            if (x, y) == hueco_inicial:
                linea += " ·"  # Hueco inicial vacío
            elif (x, y) in lista_casillas:
                linea += " O"  # Casilla con ficha
            else:
                linea += "  "  # Fuera del tablero
        print(linea)


if __name__ == "__main__":
    for tablero_info in todos_los_tableros():
        lista_casillas, hueco_inicial, _, num_tablero = tablero_info
        if lista_casillas:
            renderizar_tablero(lista_casillas, hueco_inicial, num_tablero)
