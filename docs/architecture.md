# Arquitectura de referencia

## Contexto

La práctica implementa una arquitectura Lakehouse local, basada en archivos y tablas Delta, para observar ingesta, transformación, almacenamiento y consumo analítico y de machine learning. No se construye un Data Warehouse independiente: Gold sirve directamente a consultas analíticas y al entrenamiento.

## Flujo lógico

Fuente CSV → Bronze (Delta Lake) → Silver (Delta Lake) → Gold (Delta Lake) → consumo analítico (DuckDB) y entrenamiento (scikit-learn) → serving (FastAPI) → observabilidad.

## Responsabilidades

- **CSV:** formato de intercambio para datos sintéticos de origen.
- **Delta Lake:** gestión de tablas transaccionales sobre archivos en Bronze, Silver y Gold.
- **DuckDB:** motor SQL analítico local que consulta Gold sin crear un almacén dimensional independiente.
- **Scikit-learn:** entrenamiento supervisado a partir de Gold.
- **FastAPI:** exposición del modelo como servicio de inferencia.
- **Reporte HTML:** visualización ligera de indicadores y resultados analíticos.
- **Scripts:** automatización reproducible de las etapas.

## Principios

- **Separación de responsabilidades:** almacenamiento, procesamiento, entrenamiento, inferencia y observabilidad diferenciados.
- **Reproducibilidad:** conjunto sintético de 1.000 registros y dependencias fijadas.
- **Consumo analítico desde el Lakehouse:** agregaciones directas sobre Gold mediante DuckDB.
- **Calidad y gobierno:** pseudonimización en Silver, sin sustituir autenticación, autorización ni controles de acceso.

## Alcance

La arquitectura es local y educativa. No implementa almacenamiento de objetos gestionado, catálogo empresarial, control de acceso productivo, clúster distribuido, Feature Store completo ni plataforma MLOps integral. Estos elementos se analizan como alternativas, no como dependencias obligatorias.
