from unified_planning.io import PDDLWriter

from modelador import modelar
from tableros.tablero import todos_los_tableros

tableros = todos_los_tableros()

for tablero in tableros:
    lista_casillas, hueco_inicial, objetivo, num_tablero = tablero
    problema_senku = modelar(lista_casillas, hueco_inicial, objetivo)
    writer = PDDLWriter(problema_senku)
    if num_tablero == 1:
        writer.write_domain("pddl/dominio.pddl")
    writer.write_problem(f"pddl/problema_{num_tablero}.pddl")
