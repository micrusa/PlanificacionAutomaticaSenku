# PlanificacionAutomaticaSenku

El Senku (Peg Solitaire) es un juego solitario que, a pesar de sus reglas sencillas, oculta un espacio de estados muy grande. Esto hace que las soluciones por fuerza bruta sean ineficientes y lo convierte en un caso de estudio ideal para algoritmos de planificación automática y el diseño de funciones heurísticas.

Este proyecto modela el juego usando PDDL para separar la lógica del dominio del motor de búsqueda, y desarrolla en Python un sistema capaz de resolverlo. Para optimizar la búsqueda, se implementa el algoritmo **Beam Search** potenciado por la **"Función Pagoda"**, una heurística que asigna pesos a las casillas para podar ramas no prometedoras del árbol de búsqueda.

### Objetivos
- Formalizar el dominio y problemas del Senku en PDDL.
- Implementar y comparar estrategias de búsqueda informada en Python.
- Evaluar la eficacia de la Función Pagoda en diferentes configuraciones de tablero.

### Estructura del repositorio
- `/pddl`: Dominio y problemas en PDDL.
- `/soluciones`: Soluciones de los experimentos
- `/tableros`: Modelo de los tableros

### Archivos ejecutables:
- `buscador_beam.py`: Ejecuta el experimento de Beam Search
- `gen_pddl.py`: Genera archivos PDDL de dominio y problemas (para todos los tableros)
- `resolver_automatico.py`: Ejecuta el experimento de fast-downward. Es necesario instalar el planificador con `pip install up-fast-downward`