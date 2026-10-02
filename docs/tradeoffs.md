# Análisis de decisiones arquitectónicas mediante ADR

El análisis de trade-offs se estructura mediante **Architecture Decision Records (ADR)**. Cada discusión parte de un contexto y una restricción, identifica alternativas plausibles, examina consecuencias y relaciona la decisión con atributos de calidad.

Los ADR de referencia se encuentran en `docs/adr/`. Estos documentos representan decisiones adoptadas para el laboratorio; no constituyen respuestas universales ni entregables estudiantiles.

## Estructura del ADR

- **ID y título:** identificador y nombre breve de la decisión.
- **Estado:** propuesto, aceptado, rechazado o sustituido.
- **Contexto:** situación, necesidades, restricciones y atributos de calidad relevantes.
- **Problema:** decisión arquitectónica que requiere resolución.
- **Alternativas consideradas:** opciones realistas con ventajas y limitaciones.
- **Decisión:** alternativa adoptada y alcance.
- **Justificación:** relación entre la decisión y los requisitos.
- **Consecuencias:** beneficios, costes, riesgos y limitaciones.
- **Atributos de calidad afectados:** rendimiento, escalabilidad, seguridad, mantenibilidad, disponibilidad, portabilidad y coste operacional.
- **Revisión:** cambios de contexto que justificarían reconsiderar la decisión.

La plantilla está disponible en `docs/adr/ADR_TEMPLATE.md`.

## Decisiones representadas

- **ADR-001 — Delta Lake para Bronze, Silver y Gold:** contrasta Parquet sin log transaccional, Delta Lake y una base relacional.
- **ADR-002 — Consumo analítico con DuckDB:** contrasta consultas directas sobre el Lakehouse, un motor distribuido y un Data Warehouse separado.
- **ADR-003 — Separación del model serving:** contrasta inferencia integrada en el script y servicio HTTP dedicado.

## Escenarios opcionales para discusión

Estos escenarios amplían el contexto de una decisión sin requerir que se desplieguen componentes adicionales durante la práctica.

### Escenario A — Almacenamiento de objetos con MinIO

**Contexto:** el Lakehouse debe ser compartido por varios procesos o entornos, y los datos deben persistir independientemente del ciclo de vida de una máquina de cómputo.

**Alternativas:** sistema de archivos local frente a almacenamiento de objetos compatible con S3, como MinIO.

**Aspectos para discutir:** endpoint y credenciales S3, bucket y políticas, persistencia del volumen, redes, secretos, concurrencia, operaciones de escritura Delta, compatibilidad de clientes, backups y monitorización. MinIO separaría almacenamiento y cómputo, pero incorporaría operación de servicio y no aportaría por sí solo catálogo, gobierno ni motor distribuido.

### Escenario B — Alternativas de procesamiento

**Contexto:** aumenta el volumen, la concurrencia o el número de transformaciones.

**Alternativas:** DuckDB local frente a un motor distribuido como Spark.

**Aspectos para discutir:** volumen y particionamiento, latencia, paralelismo, coste, despliegue, observabilidad y capacidades del equipo. El cambio de motor debe justificarse mediante requisitos, no solamente por el tamaño del conjunto de datos.

### Escenario C — Gestión de secretos y control de acceso

**Contexto:** se incorporan datos confidenciales, múltiples perfiles de usuario o servicios desplegados.

**Alternativas:** configuración local controlada para el laboratorio frente a gestor de secretos e identidad de workload; autorización en la aplicación frente a políticas aplicadas por una plataforma que las haga cumplir.

**Aspectos para discutir:** RBAC asigna permisos a roles; CLS restringe columnas y RLS restringe filas. Estas políticas requieren un motor, catálogo o capa de acceso que las aplique efectivamente. En el laboratorio local, ocultar columnas durante una transformación no equivale a CLS, y filtrar filas en un script no constituye RLS centralizado. MinIO puede aplicar políticas de acceso a objetos, pero no equivale a políticas de consulta por columna o fila dentro de tablas.

### Escenario D — Base de datos de grafos

**Contexto:** el caso de uso necesita recorrer relaciones de múltiples saltos, detectar comunidades, caminos o patrones de conexión entre entidades.

**Alternativas:** modelar relaciones como tablas/columnas en el Lakehouse frente a incorporar una base de datos de grafos.

**Aspectos para discutir:** patrón de consulta, complejidad de joins y recorridos, consistencia, sincronización, duplicación, gobernanza y coste operacional. Una base de grafos no reemplaza automáticamente al Lakehouse; se justifica cuando el patrón de consulta relacional es central para el dominio. Para el dataset tabular de clientes del laboratorio, añadirla no es necesario.

## Criterio de análisis

En cada discusión se debe responder: ¿qué requisito nuevo justifica la alternativa?, ¿qué atributos de calidad mejora o compromete?, ¿qué componentes y responsabilidades adicionales introduce?, ¿qué costes operacionales aparecen? La conclusión depende del contexto planteado y no de una clasificación universal de tecnologías.
