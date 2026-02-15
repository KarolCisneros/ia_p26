---
title: "Optimización"
---

# Optimización

En IA, casi todo se reduce a optimizar: minimizar una pérdida, maximizar una utilidad, encontrar los mejores parámetros. Entrenar una red neuronal es resolver un problema de optimización. Ajustar una regresión es resolver un problema de optimización. Incluso elegir la mejor jugada en un juego puede verse como optimización.

Este módulo enseña el **lenguaje** de la optimización — cómo formular problemas, entender el paisaje de soluciones, y usar herramientas computacionales para resolverlos.

## Contenido

| Sección | Tema | Idea clave |
|:------:|------|-----------|
| 7.1 | [Formulación matemática](01_formulacion.md) | Los 3 componentes: objetivo, variables, restricciones |
| 7.2 | [Paisaje y conceptos](02_paisaje_y_conceptos.md) | Mínimos, máximos, puntos silla, convexidad |
| 7.3 | [Algoritmos (intuiciones)](03_algoritmos.md) | Gradiente, Lagrange, simplex, metaheurísticas |
| 7.4 | [Ejemplos en Python](04_ejemplos_python.md) | scipy.optimize en acción |
| Lab | [Laboratorio de imágenes](lab_optimization.py) | Genera todas las visualizaciones |
| Notebook 1 | [Formulación y paisaje](notebooks/01_formulacion_y_paisaje.ipynb) | Interactivo: formula y visualiza |
| Notebook 2 | [Algoritmos y código](notebooks/02_algoritmos_y_codigo.ipynb) | Interactivo: GD, scipy, LP |

## Cómo correr el lab (para imágenes)

```bash
cd clase/07_optimization
python lab_optimization.py
```

Esto genera imágenes en `images/` que se usan en las notas.

## Notebooks interactivos

Los notebooks están diseñados para ejecutarse en Google Colab:

- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/01_formulacion_y_paisaje.ipynb) **Formulación y paisaje** — formula problemas y visualiza superficies
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/02_algoritmos_y_codigo.ipynb) **Algoritmos y código** — descenso de gradiente, scipy, programación lineal

## Objetivos de aprendizaje

Al terminar este módulo podrás:

1. **Formular** un problema de optimización: identificar objetivo $f(x)$, variables de decisión $x$, y restricciones.
2. **Distinguir** entre mínimos locales, globales, puntos silla, y entender por qué importa.
3. **Explicar** qué es convexidad y por qué simplifica la optimización ("todo mínimo local es global").
4. **Describir** intuitivamente cómo funcionan descenso de gradiente, multiplicadores de Lagrange y el método simplex.
5. **Resolver** problemas de optimización en Python usando `scipy.optimize`.
6. **Conectar** estos conceptos con el entrenamiento de modelos de ML.

---

**Siguiente:** [Formulación matemática →](01_formulacion.md)
