from unified_planning.io import PDDLWriter

from modelador import modelar
from tableros.tablero_1 import generar_tablero_1

lista_casillas, hueco_inicial = generar_tablero_1()
problema_senku = modelar(lista_casillas, hueco_inicial)
writer = PDDLWriter(problema_senku)
writer.write_domain("pddl/dominio.pddl")
