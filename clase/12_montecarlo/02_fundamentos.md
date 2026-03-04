---
title: "Fundamentos Formales"
---

# Fundamentos Formales

> *"In its simplest form, the Monte Carlo method is just the sample mean."*
> — Art Owen, *Monte Carlo theory, methods and examples* (2013)

---

## El problema central

Monte Carlo resuelve un problema muy general:

> **Dado**: una variable aleatoria $X \sim p$ y una función $f$
> **Queremos**: calcular $\mu = \mathbb{E}[f(X)] = \int f(x)\, p(x)\, dx$
> **Obstáculo**: el integral no tiene forma cerrada o es computacionalmente intratable

Esto abarca casi todo lo interesante en probabilidad aplicada: probabilidades ($f = \mathbf{1}_A$), momentos ($f(x) = x^k$), varianzas, valores esperados de payoffs financieros, probabilidades posteriores en modelos bayesianos...

---

## El estimador de Monte Carlo

El estimador es sorprendentemente simple. Dados $n$ puntos muestreados **independientemente** de $p$:

$$X_1, X_2, \ldots, X_n \stackrel{\text{i.i.d.}}{\sim} p$$

el estimador Monte Carlo es el **promedio muestral**:

$$\hat{\mu}_n = \frac{1}{n} \sum_{i=1}^n f(X_i)$$

Eso es todo. No hay magia adicional: muestrea y promedia.

---

## Por qué funciona: la Ley de los Grandes Números

El estimador $\hat{\mu}_n$ es correcto porque la **Ley de los Grandes Números (LLN)** garantiza su convergencia.

**Teorema (LLN fuerte):** Si $X_1, X_2, \ldots$ son i.i.d. con distribución $p$ y:

$$\text{Supuesto: } \mathbb{E}[|f(X)|] < \infty$$

entonces:

$$\hat{\mu}_n \xrightarrow{\text{c.s.}} \mu \quad \text{cuando } n \to \infty$$

La convergencia es *casi segura* — no solo en probabilidad. El supuesto es mínimo: basta que $f$ sea integrable bajo $p$.

Esto garantiza que el estimador es **consistente**: con suficientes muestras, se aproxima tanto como se quiera al valor verdadero.

---

## Cuán bueno es: el Teorema Central del Límite

La LLN dice que converge, pero no dice qué tan rápido. Para eso necesitamos el **Teorema Central del Límite (CLT)**.

**Supuesto adicional:** $\text{Var}[f(X)] = \sigma^2 < \infty$

Bajo este supuesto, para $n$ grande:

$$\sqrt{n}(\hat{\mu}_n - \mu) \xrightarrow{d} \mathcal{N}(0, \sigma^2)$$

En términos prácticos: para $n$ grande, $\hat{\mu}_n$ es aproximadamente normal con media $\mu$ y desviación estándar $\sigma/\sqrt{n}$.

Esto nos da directamente un **intervalo de confianza al $(1-\alpha)$**:

$$\hat{\mu}_n \pm z_{\alpha/2} \cdot \frac{\hat{\sigma}}{\sqrt{n}}$$

donde $\hat{\sigma}$ es la desviación estándar muestral de $f(X_1), \ldots, f(X_n)$ y $z_{0.025} = 1.96$ para el IC al 95%.

![Distribución del estimador MC — CLT en acción]({{ '/12_montecarlo/images/clt_demo.png' | url }})

La imagen muestra cómo la distribución de $\hat{\pi}_n$ sobre 1,000 experimentos independientes es aproximadamente normal, con varianza que cae como $\sigma^2/n$ — exactamente lo que predice el CLT.

---

## El error escala como $O(1/\sqrt{n})$

El resultado clave: el **error estándar** del estimador es:

$$\text{SE}(\hat{\mu}_n) = \frac{\sigma}{\sqrt{n}}$$

Para reducir el error a la mitad, necesitas 4 veces más muestras. Para reducirlo 10 veces, necesitas 100 veces más muestras. El error es $O(1/\sqrt{n})$.

![Escalamiento del error Monte Carlo]({{ '/12_montecarlo/images/error_scaling.png' | url }})

La gráfica log-log confirma la teoría: la pendiente empírica es $\approx -0.5$, exactamente $-1/2$.

---

## La ventaja dimensional

¿Por qué Monte Carlo es tan importante en alta dimensión? Compáralo con los métodos de cuadratura (integración en rejilla).

**Cuadratura en $d$ dimensiones:** Para lograr error $\varepsilon$, el número de puntos necesarios escala como:

$$n_{\text{cuad}} \propto \varepsilon^{-d/2}$$

Para $d = 20$ y $\varepsilon = 0.01$: $n_{\text{cuad}} \approx 10^{40}$. Imposible.

**Monte Carlo en $d$ dimensiones:** El error es $\sigma/\sqrt{n}$, **independiente de $d$**:

$$n_{\text{MC}} = \left(\frac{z_{\alpha/2} \cdot \sigma}{\varepsilon}\right)^2$$

Para $\varepsilon = 0.01$ y $\sigma = 0.5$: $n_{\text{MC}} \approx 10{,}000$. Independientemente de $d$.

![Monte Carlo vs. Cuadratura — costo en función de la dimensión]({{ '/12_montecarlo/images/dimension_comparison.png' | url }})

La gráfica muestra el cruce: para $d \lesssim 4$, los métodos de cuadratura pueden ser competitivos. Para $d \geq 4$, Monte Carlo domina. Para $d \geq 10$, la diferencia es astronómica.

Esta propiedad — que la tasa de convergencia no depende de $d$ — es la razón por la que Monte Carlo es indispensable en machine learning (redes neuronales con millones de parámetros), física estadística, y estadística bayesiana.

---

## Los tres requisitos

Monte Carlo funciona cuando se cumplen:

| Requisito | Condición | Qué pasa si se viola |
|:---:|---------|---------------------|
| **i.i.d.** | $X_1, \ldots, X_n$ independientes e idénticamente distribuidos de $p$ | El estimador puede ser sesgado o inconsistente |
| **Varianza finita** | $\text{Var}[f(X)] = \sigma^2 < \infty$ | El CLT no aplica; los ICs son inválidos |
| **Muestreable** | Se puede generar $X \sim p$ (directa o indirectamente) | Problema de inferencia — necesitas MCMC u otros métodos |

El tercer requisito es el más sutil: en muchos problemas prácticos (posteriors bayesianos complejos, distribuciones de alta dimensión), **no es fácil muestrear de $p$**. Resolver esto es el problema de MCMC (Markov Chain Monte Carlo), que es el siguiente paso después de este módulo.

---

## Resumen

```
Problema:   Calcular μ = E[f(X)],  X ~ p
Estimador:  μ̂ₙ = (1/n) Σ f(Xᵢ),   Xᵢ i.i.d. ~ p
Garantía:   LLN → μ̂ₙ →(c.s.) μ     [supuesto: E[|f|] < ∞]
Precisión:  CLT → error ∝ σ/√n      [supuesto: Var[f] < ∞]
IC 95%:     μ̂ₙ ± 1.96 · σ̂/√n
Costo:      n = (z·σ/ε)²  — independiente de la dimensión d
```

Con esto en mano, pasemos al notebook donde todo esto cobra vida con código.
