# ADR-002: Consultar Gold directamente con DuckDB

- **Estado:** Aceptado para el laboratorio
- **Fecha:** 2026-10-02

## Contexto

Gold forma parte del Lakehouse. Se requiere consumo analítico además de ML, sin añadir plataforma BI o Data Warehouse independiente.

## Problema

Definir cómo exponer agregaciones y visualizaciones con infraestructura mínima y una única fuente analítica.

## Alternativas consideradas

- **DuckDB sobre Delta:** SQL local directo a la tabla; ligero para el laboratorio, sin representar procesamiento distribuido multiusuario.
- **Motor SQL distribuido:** escala procesamiento y concurrencia, pero requiere despliegue y administración.
- **Data Warehouse separado:** permite modelo dimensional y capa semántica, pero duplica persistencia y cargas que no son requisito actual.

## Decisión

Utilizar DuckDB para agregaciones directas sobre Gold y generar un reporte HTML ligero. No se materializa otra base de datos analítica.

## Justificación

Demuestra consumo analítico desde el Lakehouse y mantiene el foco en consultas, capas y atributos de calidad.

## Consecuencias

- **Beneficios:** evita duplicación, facilita SQL y reduce configuración.
- **Costes y riesgos:** concurrencia y escalabilidad local limitadas; HTML estático, no monitoreo en tiempo real.
- **Atributos:** simplicidad y coste favorables; rendimiento adecuado al tamaño de aula; escalabilidad y gobierno empresarial limitados.

## Revisión

Revisar ante necesidades de autoservicio, semántica centralizada, concurrencia, políticas de acceso o mayores volúmenes.
