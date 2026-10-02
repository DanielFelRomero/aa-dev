# AA Dev — Práctica de Arquitecturas Analíticas

Repositorio de apoyo para una práctica de tres horas orientada al análisis de una arquitectura analítica moderna mediante cuatro etapas integradas.

## Propósito

La práctica permite experimentar, en un entorno reproducible, decisiones asociadas con almacenamiento de datos, arquitectura Lakehouse, calidad y gobierno, preparación de datos para machine learning, exposición de modelos y observabilidad.

El objetivo principal no consiste en desarrollar una solución de producción. El objetivo consiste en observar cómo determinadas decisiones arquitectónicas afectan atributos de calidad y discutir los trade-offs entre alternativas.

## Guía de ejecución

La guía paso a paso se encuentra en [guia_practica.md](guia_practica.md). Se recomienda utilizarla como documento principal durante la sesión.

## Arquitectura de referencia

Fuente CSV → Bronze (Delta Lake) → Silver (Delta Lake) → Gold (Delta Lake) → consumo analítico con DuckDB y entrenamiento → serving → observabilidad.

Gold se consulta directamente como parte del Lakehouse. No se incorpora un Data Warehouse independiente.

La práctica utiliza componentes locales para representar conceptos arquitectónicos sin afirmar que el entorno constituye una plataforma Lakehouse productiva.

## Etapas

### 1. Ingesta y almacenamiento

Se ingesta un conjunto sintético de 1.000 registros a Bronze como tabla Delta Lake.

### 2. Transformación, calidad y gobierno

Se construye Silver con transformación y pseudonimización determinística. Gold se conserva como tabla Delta para consumo analítico y ML.

### 3. Entrenamiento y serving

Se entrena un modelo supervisado con Scikit-learn, se persiste el artefacto y se expone mediante FastAPI.

### 4. Observabilidad y trade-offs

Se ejecutan consultas agregadas sobre Gold, se revisan visualizaciones HTML e indicadores de calidad y drift, y se analizan decisiones con el formato ADR.

## Filosofía de trabajo

Los scripts son preconstruidos, documentados y probados. La actividad se centra en ejecutar, observar, interpretar y discutir. No se requiere entregar un informe ni otro artefacto formal.

## Entorno

- Python 3.12
- DuckDB
- delta-rs / `deltalake`
- pandas
- PyArrow
- scikit-learn
- FastAPI
- Uvicorn

Las versiones exactas se encuentran en `requirements.txt`.

## Inicio rápido

```bash
make setup
make test
make run-all
make serve
```

La documentación interactiva de FastAPI puede consultarse en:

```
http://127.0.0.1:8000/docs
```

## Visualización

La práctica ofrece dos mecanismos visuales de bajo costo:

1. La estructura de archivos permite observar la evolución de las capas Bronze, Silver y Gold.
2. FastAPI ofrece una interfaz web interactiva para explorar el contrato y ejecutar las operaciones del servicio.

Las consultas analíticas se ejecutan con DuckDB directamente sobre Gold; `scripts/07_analytics.py` genera visualizaciones HTML sin añadir un Data Warehouse ni un servidor BI. El análisis de trade-offs utiliza ADR como formato de discusión, sin entregables formales.
