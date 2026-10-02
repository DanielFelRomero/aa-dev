# ADR-001: Utilizar Delta Lake para las capas del Lakehouse

- **Estado:** Aceptado para el laboratorio
- **Fecha:** 2026-10-02

## Contexto

El laboratorio representa Bronze, Silver y Gold con instalación local, recursos modestos y 1.000 registros sintéticos. Se requiere diferenciar formato de archivo y gestión de tablas sin desplegar plataforma distribuida ni Data Warehouse.

## Problema

Seleccionar la persistencia de capas curadas para habilitar gestión y consulta de tablas con complejidad operacional acotada.

## Alternativas consideradas

- **Parquet sin capa transaccional:** formato columnar abierto y simple, sin log de tabla ni semántica transaccional propia.
- **Delta Lake local:** conserva datos en Parquet y añade log transaccional y metadatos; representa el patrón de tabla Lakehouse, con dependencia adicional.
- **Base relacional:** ofrece SQL, pero desplaza el ejercicio a un motor de base de datos y no representa la tabla Lakehouse basada en archivos.

## Decisión

Utilizar Delta Lake mediante delta-rs en Bronze, Silver y Gold sobre el sistema de archivos local. DuckDB consulta Gold mediante su extensión Delta.

## Justificación

Permite observar gestión de tablas sobre archivos abiertos y consumo SQL sin desplegar clúster ni Data Warehouse.

## Consecuencias

- **Beneficios:** capas inspeccionables, metadatos de tabla y flujo reproducible.
- **Costes y riesgos:** dependencias y compatibilidad de operaciones; no demuestra escalabilidad distribuida.
- **Atributos:** simplicidad y coste favorecidos; escalabilidad local limitada; portabilidad basada en archivos abiertos.

## Revisión

Revisar ante requisitos de volumen, concurrencia, despliegue multiusuario, disponibilidad o almacenamiento de objetos.
