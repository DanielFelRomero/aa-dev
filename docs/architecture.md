# Arquitectura de referencia

## Contexto

La práctica implementa una arquitectura analítica local que permite observar conceptos normalmente presentes en arquitecturas de datos modernas.

La arquitectura se divide en ingestión, almacenamiento Bronze, transformación y calidad en Silver, dataset analítico Gold, entrenamiento de machine learning, serving y observabilidad.

## Principios

### Separación de responsabilidades

Cada componente mantiene una responsabilidad específica:

- DuckDB: procesamiento analítico local.
- Delta Lake: gestión de tablas sobre almacenamiento basado en archivos.
- Parquet: formato columnar.
- Scikit-learn: entrenamiento del modelo.
- FastAPI: exposición del servicio de inferencia.
- Scripts: automatización de la ejecución de cada etapa.

### Reproducibilidad

El entorno fija versiones de dependencias y utiliza una semilla de aleatoriedad conocida.

### Calidad y gobierno

La calidad se observa como un atributo transversal. La protección del identificador se realiza antes de la generación del dataset Gold.

## Alcance

La arquitectura es deliberadamente local. No implementa:

- almacenamiento de objetos gestionado;
- catálogo de datos empresarial;
- control de acceso de producción;
- clúster distribuido;
- Feature Store;
- plataforma MLOps completa.

Estos elementos pueden ser objeto de discusión arquitectónica.
