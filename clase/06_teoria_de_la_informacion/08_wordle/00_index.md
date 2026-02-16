---
title: "Proyecto Wordle: Teoría de la Información en Acción"
---

# Proyecto Wordle: Teoría de la Información en Acción

:::project{id="PROJ-WORDLE" title="Proyecto Wordle" due="TBD" points="TBD"}
Diseña, implementa y compara estrategias de Wordle usando herramientas de teoría de la información (entropía, ganancia de información, score esperado). Trabaja en el [repositorio del torneo](https://github.com/sonder-art/rtorneo_wordle_p26) y participa en el torneo del curso.
:::

## Contenido

| Sección | Tema | Idea clave |
|:------:|------|-----------|
| W.1 | [El juego de Wordle](01_el_juego.md) | Reglas, feedback y estructura de información |
| W.2 | [Estrategia aleatoria](02_estrategia_aleatoria.md) | Baseline: adivinar al azar |
| W.3 | [Máxima probabilidad](03_maxima_probabilidad.md) | Greedy: siempre la más probable |
| W.4 | [Entropía ingenua](04_entropia_ingenua.md) | Maximizar bits esperados (3B1B S1) |
| W.5 | [Entropía ponderada](05_entropia_ponderada.md) | Incorporar frecuencia con sigmoide (3B1B S2) |
| W.6 | [Score esperado](06_score_esperado.md) | Minimizar intentos totales (3B1B S3) |
| W.7 | [Look-ahead](07_look_ahead.md) | Mirar dos pasos al futuro (3B1B S4) |
| W.8 | [Preguntas abiertas](08_preguntas_abiertas.md) | Direcciones creativas y extensiones |

## Repositorio del torneo

Todo el código del proyecto vive en un repositorio separado:

**[github.com/sonder-art/rtorneo_wordle_p26](https://github.com/sonder-art/rtorneo_wordle_p26)**

El repositorio contiene:

- Motor del juego (`WordleEnv`) que soporta palabras de 4, 5 y 6 letras
- Clase base `Strategy` con `GameConfig` para implementar estrategias
- Torneo automático paralelo con scoring Borda Count sobre 6 rondas
- Tres benchmarks incluidos: Random, MaxProb, Entropy
- Dashboard web para visualizar resultados
- Corpus de palabras en español (uniform y frequency)

### Setup rápido

```bash
git clone git@github.com:sonder-art/rtorneo_wordle_p26.git
cd rtorneo_wordle_p26
pip install -r requirements.txt
python3 run_all.py
```

### Formato del torneo

Tu estrategia compite en **6 rondas**: palabras de {4, 5, 6} letras en modos {uniform, frequency}. Se rankean por promedio de intentos usando **Borda Count**. Ver [reglas completas](https://github.com/sonder-art/rtorneo_wordle_p26/blob/main/docs/rules.md) y [guía de equipo](https://github.com/sonder-art/rtorneo_wordle_p26/blob/main/docs/team_guide.md).

### Entrega

1. Copia el template: `cp -r estudiantes/_template estudiantes/mi_equipo`
2. Edita `estudiantes/mi_equipo/strategy.py` — **único archivo evaluado**
3. Prueba: `python3 experiment.py --strategy "MiEstrategia_mi_equipo" --verbose`
4. Abre un PR en el repositorio del torneo

## Referencia

- [3Blue1Brown: Solving Wordle using information theory](https://www.3blue1brown.com/lessons/wordle) — el video que inspira la progresión de estrategias de este proyecto.

---

**Volver:** [← Índice del módulo](../00_index.md)
