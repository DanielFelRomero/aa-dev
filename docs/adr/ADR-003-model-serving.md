# ADR-003: Separar entrenamiento y servicio de inferencia

- **Estado:** Aceptado para el laboratorio
- **Fecha:** 2026-10-02

## Contexto

El modelo se entrena desde Gold y luego se utiliza para inferencia. La práctica busca distinguir el ciclo de entrenamiento del consumo del modelo.

## Problema

Decidir si la inferencia se ejecuta en el script de entrenamiento o se expone como servicio independiente.

## Alternativas consideradas

- **Ejecución integrada:** sencilla para experimentos puntuales, pero acopla predicción al proceso de entrenamiento y no ofrece interfaz reutilizable.
- **FastAPI:** expone un contrato HTTP y desacopla entrenamiento y consumo, a costa de un proceso y responsabilidades operacionales.

## Decisión

Persistir el modelo y cargarlo en FastAPI, que expone endpoints de salud e inferencia.

## Justificación

Permite demostrar model serving, contrato API e independencia entre entrenamiento y solicitudes.

## Consecuencias

- **Beneficios:** contrato explícito, separación de responsabilidades y base para versionamiento y monitoreo.
- **Costes y riesgos:** proceso adicional; no incluye autenticación, alta disponibilidad ni despliegue productivo.
- **Atributos:** favorece mantenibilidad e interoperabilidad; aumenta complejidad operacional.

## Revisión

Revisar ante requisitos batch, latencia, concurrencia, autenticación, disponibilidad o gestión de versiones.
