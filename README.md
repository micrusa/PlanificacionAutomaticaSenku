# PlanificacionAutomaticaSenku

El Senku (Peg Solitaire) es un juego solitario que, a pesar de sus reglas sencillas, oculta un espacio de estados muy grande. Esto hace que las soluciones por fuerza bruta sean ineficientes y lo convierte en un caso de estudio ideal para algoritmos de planificación automática y el diseño de funciones heurísticas.

Este proyecto modela el juego usando PDDL para separar la lógica del dominio del motor de búsqueda, y desarrolla en Python un sistema capaz de resolverlo. Para optimizar la búsqueda, se implementa el algoritmo **Beam Search** potenciado por la **"Función Pagoda"**, una heurística que asigna pesos a las casillas para podar ramas no prometedoras del árbol de búsqueda.

### Objetivos
- Formalizar el dominio y problemas del Senku en PDDL.
- Implementar y comparar estrategias de búsqueda informada en Python.
- Evaluar la eficacia de la Función Pagoda en diferentes configuraciones de tablero.

### Estructura del repositorio
- `/pddl`: Dominio y problemas en PDDL.
- `/src`: Implementaciones en Python (búsquedas, heurísticas).
- `/results`: Experimentos y análisis de rendimiento.

Instalaciones:
pip install up-pyperplan
pip install up-enhsp
pip install up-fast-downward