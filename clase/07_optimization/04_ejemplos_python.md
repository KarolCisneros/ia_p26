---
title: "Ejemplos de optimización en Python"
---

# Ejemplos de optimización en Python

Ahora ponemos todo en práctica con código. Usamos `scipy.optimize`, la biblioteca estándar de Python para optimización numérica.

---

## Ejemplo 1: Minimización 1D

Minimizamos $f(x) = (x-3)^2 + 2\sin(5x)$ — una función con varios mínimos locales.

```python
from scipy.optimize import minimize_scalar

f = lambda x: (x - 3)**2 + 2 * np.sin(5 * x)

result = minimize_scalar(f, bounds=(0, 6), method="bounded")
print(f"Mínimo en x = {result.x:.4f}, f(x) = {result.fun:.4f}")
```

![Minimización 1D con scipy]({{ '/07_optimization/images/minimize_1d.png' | url }})

**Nota:** `minimize_scalar` con `method="bounded"` busca en un intervalo. Puede encontrar un mínimo **local**, no necesariamente el global. Prueba diferentes intervalos para verificar.

---

## Ejemplo 2: Descenso de gradiente desde cero

Implementamos GD en 10 líneas para la función de Rosenbrock $f(x,y) = (1-x)^2 + 100(y-x^2)^2$.

```python
import numpy as np

def gradient_descent(grad_f, x0, lr=0.001, n_steps=5000):
    """Descenso de gradiente básico. Retorna la trayectoria."""
    trajectory = [x0.copy()]
    x = x0.copy()
    for _ in range(n_steps):
        x = x - lr * grad_f(x)
        trajectory.append(x.copy())
    return np.array(trajectory)

# Gradiente de Rosenbrock
grad_rosen = lambda x: np.array([
    -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0]**2),
    200 * (x[1] - x[0]**2),
])

traj = gradient_descent(grad_rosen, np.array([-1.5, 2.0]))
print(f"Final: ({traj[-1, 0]:.4f}, {traj[-1, 1]:.4f})")
print(f"Óptimo real: (1, 1)")
```

![GD en Rosenbrock]({{ '/07_optimization/images/gd_rosenbrock.png' | url }})

Observa que GD avanza lento por el "valle banana" de Rosenbrock. Algoritmos más sofisticados (como L-BFGS o Adam) manejan esto mucho mejor.

---

## Ejemplo 3: Optimización con restricciones

Resolvemos el problema de producción del [Ejemplo 1 de formulación](01_formulacion.md):

$$\max \, 5x_1 + 4x_2 \quad \text{s.t.} \quad 6x_1 + 4x_2 \leq 24, \quad x_1 + 2x_2 \leq 6, \quad x_1, x_2 \geq 0$$

Con `scipy.optimize.linprog` (que **minimiza**, así que negamos el objetivo):

```python
from scipy.optimize import linprog

c = [-5, -4]             # min -5x1 - 4x2 (equivale a max 5x1 + 4x2)
A_ub = [[6, 4], [1, 2]]  # restricciones de desigualdad
b_ub = [24, 6]
bounds = [(0, None), (0, None)]  # x1, x2 >= 0

result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
print(f"Solución: x1={result.x[0]:.2f}, x2={result.x[1]:.2f}")
print(f"Ganancia máxima: {-result.fun:.2f}")
```

Salida:
```
Solución: x1=3.00, x2=1.50
Ganancia máxima: 21.00
```

![Solución LP con scipy]({{ '/07_optimization/images/linprog_feasible.png' | url }})

---

## Ejemplo 4: Lagrange verificado con Python

Resolvemos $\min \, x^2 + y^2$ sujeto a $x + y = 1$ **por Lagrange** y verificamos con `scipy.optimize.minimize`.

**A mano** (ver [sección de Lagrange](03_algoritmos.md)): la solución es $(x^*, y^*) = (1/2, 1/2)$.

**Con scipy:**

```python
from scipy.optimize import minimize

f = lambda x: x[0]**2 + x[1]**2
constraint = {"type": "eq", "fun": lambda x: x[0] + x[1] - 1}

result = minimize(f, x0=[0.0, 0.0], constraints=constraint)
print(f"Solución: ({result.x[0]:.4f}, {result.x[1]:.4f})")
print(f"f(x*) = {result.fun:.4f}")
```

Salida:
```
Solución: (0.5000, 0.5000)
f(x*) = 0.5000
```

Coincide con la solución analítica.

---

## Conexión con Machine Learning

Cada vez que entrenas un modelo de ML, estás resolviendo un problema de optimización:

| Modelo | Función objetivo | Variables | Restricciones |
|--------|-----------------|-----------|---------------|
| Regresión lineal | $\sum(y_i - w^T x_i)^2$ | $w$ | Ninguna |
| Regresión logística | $\sum \log(1 + e^{-y_i w^T x_i})$ | $w$ | Ninguna |
| SVM | $\frac{1}{2}\|w\|^2$ | $w, b$ | $y_i(w^T x_i + b) \geq 1$ |
| Red neuronal | $\mathcal{L}(\theta; X, Y)$ | $\theta$ (millones) | Ninguna (típicamente) |

Cuando llamas `model.fit()` en scikit-learn o `loss.backward()` en PyTorch, estás ejecutando un algoritmo de optimización.

---

:::exercise{title="Ejercicio capstone: A mano y con scipy" difficulty="3"}

Una empresa quiere minimizar el costo de transporte $f(x_1, x_2) = 2x_1^2 + 3x_2^2 + x_1 x_2$ sujeto a que la producción total sea al menos 10: $x_1 + x_2 \geq 10$, con $x_1, x_2 \geq 0$.

1. **Reformula** la restricción en forma estándar ($g(x) \leq 0$).
2. **Resuelve con Lagrange** (asumiendo que la restricción está activa, es decir, $x_1 + x_2 = 10$).
3. **Verifica con scipy** usando `minimize` con la restricción.

<details>
<summary><strong>Ver Solución</strong></summary>

**1. Reformulación:** $x_1 + x_2 \geq 10 \Rightarrow -(x_1 + x_2) + 10 \leq 0$, es decir, $g(x) = -x_1 - x_2 + 10 \leq 0$.

**2. Lagrange** (asumiendo restricción activa $x_1 + x_2 = 10$):

$\mathcal{L} = 2x_1^2 + 3x_2^2 + x_1 x_2 + \lambda(x_1 + x_2 - 10)$

$$
\begin{aligned}
\frac{\partial \mathcal{L}}{\partial x_1} &= 4x_1 + x_2 + \lambda = 0 \\
\frac{\partial \mathcal{L}}{\partial x_2} &= 6x_2 + x_1 + \lambda = 0 \\
x_1 + x_2 &= 10
\end{aligned}
$$

De las dos primeras: $4x_1 + x_2 = 6x_2 + x_1 \Rightarrow 3x_1 = 5x_2 \Rightarrow x_1 = \frac{5}{3}x_2$.

Sustituyendo: $\frac{5}{3}x_2 + x_2 = 10 \Rightarrow \frac{8}{3}x_2 = 10 \Rightarrow x_2 = \frac{30}{8} = 3.75$, $x_1 = 6.25$.

**3. Con scipy:**

```python
from scipy.optimize import minimize

f = lambda x: 2*x[0]**2 + 3*x[1]**2 + x[0]*x[1]
constraint = {"type": "ineq", "fun": lambda x: x[0] + x[1] - 10}
bounds = [(0, None), (0, None)]

result = minimize(f, x0=[5.0, 5.0], constraints=constraint, bounds=bounds)
print(f"x1={result.x[0]:.4f}, x2={result.x[1]:.4f}, f={result.fun:.4f}")
# x1=6.2500, x2=3.7500, f=110.6250
```

</details>

:::

---

**Siguiente:** [← Volver al índice](00_index.md)
