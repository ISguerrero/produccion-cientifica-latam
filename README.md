# Panorama de la producción científica en Colombia y Latinoamérica

> Análisis de publicaciones científicas (2000–2025) con datos abiertos de OpenAlex: ¿qué áreas crecen, cómo se compara Colombia con la región y con quién colabora?

## 1. Contexto de negocio (reescríbelo con tus palabras)

Una agencia de ciencia e innovación (tipo MinCiencias) quiere decidir en qué áreas
de conocimiento invertir y con qué países fortalecer alianzas. Este proyecto responde:

1. **Volumen y crecimiento:** ¿cómo ha evolucionado la producción científica de Colombia frente a Brasil, México, Argentina, Chile y Perú?
2. **Áreas temáticas:** ¿en qué campos crece más Colombia y dónde está rezagada respecto a la región?
3. **Impacto:** ¿cómo se comporta la citación (mediana, % en el top 10 %) por área y país?
4. **Colaboración:** ¿con qué países e instituciones colabora Colombia? ¿Cambió tras 2015?
5. **Acceso abierto:** ¿qué proporción de la producción es de acceso abierto y cómo evoluciona?
6. **Instituciones:** ¿qué universidades y centros concentran la producción colombiana?

## 2. Fuentes de datos

| Fuente | Uso | Notas |
|---|---|---|
| [OpenAlex API](https://developers.openalex.org) | Conteos agregados (`group_by`) y muestra de obras | Requiere API key gratuita (openalex.org/settings/api) |
| OpenAlex snapshot (opcional) | Descarga masiva gratuita si quieres cargar todo en SQL | Pesado; solo si lo necesitas |
| Datos abiertos de Colombia / MinCiencias (opcional) | Contexto: inversión en I+D, grupos de investigación | datos.gov.co |
| Banco Mundial (opcional) | Gasto en I+D como % del PIB por país | Para normalizar la producción |

## 3. Stack

Python (requests, pandas, matplotlib/seaborn, networkx) · SQL (SQLite o PostgreSQL) · Power BI o Tableau · Git/GitHub

## 4. Estructura del repositorio

```
produccion-cientifica-latam/
├── README.md
├── requirements.txt
├── .env.example            # OPENALEX_API_KEY=tu_clave  (el .env real va en .gitignore)
├── data/
│   ├── raw/                # respuestas de la API, sin tocar
│   └── processed/          # datos limpios
├── sql/                    # consultas (rankings, ventanas, crecimiento)
├── notebooks/
│   ├── 01_extraccion.ipynb
│   ├── 02_limpieza.ipynb
│   ├── 03_eda.ipynb
│   └── 04_colaboracion_redes.ipynb
├── src/
│   └── extract_openalex.py
└── dashboard/              # .pbix / enlace a Tableau Public + capturas
```

## 5. Plan por semanas

| Semana | Entregable |
|---|---|
| 1 | Repo creado, API key, script de extracción funcionando, primeros conteos por año y país |
| 2 | Limpieza, carga a SQLite/PostgreSQL, consultas SQL (crecimiento, ranking por área, funciones de ventana) |
| 3 | EDA en Python: tendencias, impacto, acceso abierto; red de colaboración con networkx |
| 4 | Dashboard (Power BI/Tableau), hallazgos, recomendaciones y README final con capturas |

## 6. Consultas SQL que vale la pena mostrar

- Crecimiento anual por país con `LAG()` y media móvil con `AVG() OVER (...)`.
- Ranking de áreas por país con `RANK()` / `DENSE_RANK()`.
- Participación de Colombia en la región por área con CTEs.
- Top instituciones colombianas y su evolución.

## 7. Hallazgos y recomendaciones

*(Se completan al final. Cada hallazgo debe terminar en una recomendación accionable.)*

## 8. Limitaciones

- OpenAlex asigna países según la afiliación de los autores; hay obras con afiliaciones faltantes o mal normalizadas.
- Los conteos por área dependen de la clasificación temática de OpenAlex, que cambia entre versiones.
- Producción ≠ calidad: por eso se incluyen métricas de citación.
