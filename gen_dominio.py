from modelador import modelar
import tableros.tablero_2 as t2
from unified_planning.io import PDDLWriter

lista_casillas, hueco_inicial = t2.generar_tablero_2()
problema_senku = modelar(lista_casillas, hueco_inicial)
writer = PDDLWriter(problema_senku)
writer.write_domain("pddl/dominio.pddl")