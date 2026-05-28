from modelador import modelar
import tableros.tablero_4 as t2
from unified_planning.io import PDDLWriter

lista_casillas, hueco_inicial = t2.generar_tablero_4()
problema_senku = modelar(lista_casillas, hueco_inicial)
writer = PDDLWriter(problema_senku)
writer.write_domain("pddl/dominio.pddl")