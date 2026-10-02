# AA Dev — Práctica de Arquitecturas Analíticas

Repositorio de apoyo para una práctica de tres horas orientada al análisis de una arquitectura analítica moderna mediante cuatro etapas integradas.

## Propósito

La práctica permite experimentar, en un entorno reproducible, decisiones asociadas con almacenamiento de datos, arquitectura Lakehouse, calidad y gobierno, preparación de datos para machine learning, exposición de modelos y observabilidad.

El objetivo principal no consiste en desarrollar una solución de producción. El objetivo consiste en observar cómo determinadas decisiones arquitectónicas afectan atributos de calidad y discutir los trade-offs entre alternativas.

## Arquitectura de referencia

```text
                 +----------------------+
                 |     Fuente CSV       |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |  Ingesta / Bronze    |
                 |   Parquet / Delta    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Transformaciones     |
                 | Silver + calidad     |
                 | + gobierno de datos  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |        Gold          |
                 | Dataset analítico    |
                 | de características   |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Entrenamiento ML     |
                 | Scikit-learn         |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Model Serving      |
                 |      FastAPI         |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Observabilidad     |
                 | calidad + servicio   |
                 | + drift              |
                 +----------------------+
```

## Etapas

### 1. Ingesta y almacenamiento

Se comparan formatos orientados a intercambio y almacenamiento analítico, y se construye una capa Bronze. Se utiliza Parquet como formato columnar y Delta Lake como capa de gestión sobre almacenamiento basado en archivos.

Preguntas guía:

- ¿Qué atributos de calidad justifican el uso de un formato columnar?
- ¿Qué diferencia existe entre un formato de archivo y una arquitectura Lakehouse?
- ¿Qué capacidades aporta Delta Lake sobre Parquet?

### 2. Transformación, calidad y gobierno

La capa Silver aplica transformaciones y controles de calidad. Se realiza una operación de protección sobre un atributo identificador mediante pseudonimización determinística y se diferencia explícitamente esta técnica de la anonimización y del control de acceso.

Preguntas guía:

- ¿Qué problema se resuelve con pseudonimización?
- ¿Qué problema no resuelve?
- ¿En qué punto del flujo debe aplicarse la protección de datos?
- ¿Qué trade-off aparece entre utilidad analítica y protección?

### 3. Dataset para ML y servicio de inferencia

La capa Gold genera un dataset analítico de características. Se entrena un modelo supervisado con Scikit-learn y se expone mediante FastAPI.

El dataset de características no se presenta como un Feature Store completo. La práctica muestra únicamente el concepto de una capa preparada para ML y permite discutir qué capacidades adicionales requeriría un Feature Store real.

Preguntas guía:

- ¿Qué diferencia existe entre un dataset Gold para ML y un Feature Store?
- ¿Qué responsabilidades deben mantenerse desacopladas entre entrenamiento y serving?
- ¿Qué trade-offs aparecen al seleccionar una estrategia de serving?

### 4. Observabilidad y decisión arquitectónica

Se observan métricas básicas de calidad de datos y servicio, junto con un ejemplo de detección de data drift. La práctica finaliza con espacios de análisis y discusión de trade-offs.

Preguntas guía:

- ¿Qué métricas pertenecen a observabilidad del servicio?
- ¿Qué métricas pertenecen a observabilidad del modelo o de los datos?
- ¿Por qué data drift no equivale automáticamente a degradación del modelo?
- ¿Qué decisión arquitectónica se justificaría en un escenario productivo?

## Secuencia recomendada

| Etapa | Tiempo aproximado |
|---|---:|
| Preparación y contexto | 15 min |
| 1. Ingesta y almacenamiento | 40 min |
| 2. Transformación, calidad y gobierno | 45 min |
| 3. ML y serving | 40 min |
| 4. Observabilidad y trade-offs | 40 min |
| **Total** | **180 min** |

El tiempo está pensado para una sesión aproximada de tres horas, incluyendo ejecución, preguntas y discusión. No se amplía el alcance de las cuatro etapas.

## Filosofía de trabajo

Los scripts del repositorio han sido diseñados para ser preconstruidos, documentados y probados. La práctica no depende de que cada participante escriba desde cero los componentes de infraestructura o de machine learning.

El trabajo se concentra en:

1. Ejecutar los flujos.
2. Observar resultados.
3. Modificar parámetros seleccionados.
4. Interpretar efectos.
5. Comparar alternativas.
6. Justificar decisiones arquitectónicas.

No se requiere entregar un informe ni un artefacto formal al finalizar la práctica. Los espacios de discusión y análisis forman parte central de la actividad.

## Entorno

La referencia utilizada es:

- Python 3.12
- DuckDB 1.5.6
- delta-rs / `deltalake` 1.6.6
- pandas 3.0.6
- PyArrow 25.0.1
- scikit-learn 1.9.1
- FastAPI, versión fijada en el entorno de la práctica
- Uvicorn para ejecución local del servicio

Las versiones se fijan para favorecer reproducibilidad. El repositorio no pretende representar un stack de producción universal.

## Compatibilidad y decisión de versiones

Python 3.12 constituye el denominador común conservador del stack. DuckDB, `deltalake`, pandas, PyArrow, scikit-learn y FastAPI ofrecen soporte para Python 3.12.

DuckDB incorpora una extensión `delta` para consultar tablas Delta. La práctica utiliza `deltalake` para crear y modificar tablas cuando sea necesario, y DuckDB para consultas analíticas sobre ellas. Esto evita asumir que todas las operaciones de escritura de Delta deben realizarse desde DuckDB.

Las extensiones binarias de DuckDB están ligadas a la versión de DuckDB y a la plataforma. Por este motivo, el entorno se mantiene versionado y las instrucciones de instalación cargan explícitamente la extensión `delta`.

## Estructura

```text
aa-dev/
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile
├── config/
│   └── settings.yaml
├── data/
│   ├── source/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── samples/
├── docs/
│   ├── architecture.md
│   ├── tradeoffs.md
│   └── data_dictionary.md
├── scripts/
│   ├── 01_ingest.py
│   ├── 02_transform.py
│   ├── 03_train.py
│   ├── 04_serve.py
│   └── 05_observe.py
├── src/
│   └── aa_dev/
│       ├── __init__.py
│       ├── delta_utils.py
│       ├── quality.py
│       ├── features.py
│       └── monitoring.py
├── tests/
│   ├── test_ingest.py
│   ├── test_quality.py
│   └── test_monitoring.py
├── requirements.txt
├── Makefile
└── README.md
```

## Inicio rápido

```bash
make setup
make run-all
```

Para iniciar el servicio de inferencia:

```bash
make serve
```

La API queda disponible localmente en `http://127.0.0.1:8000`.

## Datos

La práctica utiliza un conjunto tabular sintético incluido en el repositorio. No se utilizan datos personales reales.

## Nota arquitectónica

La implementación local representa una aproximación pedagógica a una arquitectura Lakehouse. No debe interpretarse como una instalación distribuida ni como evidencia de capacidades operativas propias de un Lakehouse gestionado en producción.
