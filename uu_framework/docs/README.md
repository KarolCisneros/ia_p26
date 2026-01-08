# uu_framework

Generador de sitios estaticos para materiales de cursos universitarios.

## Descripcion

uu_framework es un framework ligero para renderizar notas de clase en Markdown como un sitio web estatico. Usa Eleventy + Tailwind CSS + Python para preprocesamiento.

## Requisitos

- Docker (recomendado) o:
  - Node.js 18+
  - Python 3.11+
  - npm

## Estructura del Proyecto

```
uu_framework/
├── config/
│   ├── site.yaml           # Configuracion principal
│   └── themes/             # Temas de colores
├── scripts/
│   ├── preprocess.py       # Orquestador de preprocesamiento
│   ├── extract_metadata.py # Extrae metadatos de archivos
│   ├── generate_indices.py # Genera arbol de jerarquia
│   ├── aggregate_tasks.py  # Agrega tareas/examenes
│   └── sync_check.py       # Verifica actualizaciones
├── eleventy/
│   ├── .eleventy.js        # Configuracion de Eleventy
│   ├── package.json        # Dependencias de Node
│   ├── _includes/          # Templates Nunjucks
│   └── src/css/            # Estilos CSS
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yaml
└── docs/
    ├── README.md           # Este archivo
    └── GUIA_ESTUDIANTE.md  # Guia para estudiantes
```

## Uso con Docker

### Construir el sitio

```bash
cd uu_framework/docker
docker compose run build
```

### Servidor de desarrollo

```bash
cd uu_framework/docker
docker compose up dev
# Visita http://localhost:8080
```

## Uso sin Docker

### Instalacion

```bash
# Instalar dependencias de Python
pip install pyyaml

# Instalar dependencias de Node
cd uu_framework/eleventy
npm install
```

### Construir

```bash
# Preprocesamiento
python3 uu_framework/scripts/preprocess.py

# Construir sitio
cd uu_framework/eleventy
npx @11ty/eleventy

# Construir CSS
npx tailwindcss -i ./src/css/main.css -o ../../_site/css/styles.css --minify
```

## Convencion de Nombres de Archivos

| Patron | Significado |
|--------|-------------|
| `00_*.md` | Archivo indice |
| `01_`, `02_` | Capitulos (orden numerico) |
| `01_a_`, `01_b_` | Sub-capitulos (orden alfabetico) |
| `A_`, `B_` | Apendices |
| `code/` | Directorio de codigo Python |

## Frontmatter YAML

```yaml
---
title: "Titulo del documento"    # Requerido
type: lesson                     # Opcional: lesson|homework|exam|project
date: 2026-01-15                 # Opcional
summary: "Resumen breve"         # Opcional
tags: [tag1, tag2]               # Opcional
due_date: 2026-02-01             # Opcional (para tareas)
---
```

## Componentes Inline

```markdown
:::homework{id="tarea-01" title="Mi Tarea" due="2026-02-01"}
Instrucciones de la tarea...
:::

:::exercise{title="Ejercicio"}
Pasos del ejercicio...
:::

:::prompt{title="Prompt para LLM"}
Texto del prompt...
:::

:::example{title="Ejemplo"}
Contenido del ejemplo...
:::

:::exam{id="parcial-01" title="Primer Parcial"}
Informacion del examen...
:::

:::project{id="proyecto-final" title="Proyecto Final" due="2026-05-15"}
Descripcion del proyecto...
:::
```

## Temas

### Eva Unit-01 (Predeterminado)

Tema oscuro inspirado en Evangelion Unit-01. Colores: purpura profundo con acentos verde neon.

### Light

Tema claro para mejor legibilidad en ambientes iluminados.

### OpenDyslexic

Toggle de fuente accesible para usuarios con dislexia.

## Configuracion

Edita `uu_framework/config/site.yaml`:

```yaml
site:
  name: "Nombre del Curso"
  base_url: "/nombre-repo"
  domain: "tu-dominio.com"

source:
  content_dir: "clase"
  exclude:
    - "archivos-a-ignorar"

theme:
  default: "eva01"
```

## Despliegue

El sitio se despliega automaticamente via GitHub Actions cuando se hace push a la rama `main`.

El sitio estara disponible en: `https://{domain}/{base_url}/`

## Desarrollo

### Agregar un nuevo tema

1. Crea `uu_framework/config/themes/mi-tema.yaml`
2. Crea `uu_framework/eleventy/src/css/themes/mi-tema.css`
3. Agrega el tema a `site.yaml` en `theme.available`

### Agregar un nuevo componente

1. Agrega el tipo en `.eleventy.js` en `componentTypes`
2. Crea el template en `_includes/components/`
3. Agrega estilos en `src/css/main.css`
