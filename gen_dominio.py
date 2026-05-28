from modelador import modelar
import tableros.tablero_1 as t1
from unified_planning.io import PDDLWriter

lista_casillas, hueco_inicial = t1.generar_tablero_1()
problema_senku = modelar(lista_casillas, hueco_inicial)
writer = PDDLWriter(problema_senku)
writer.write_domain("pddl/dominio.pddl")