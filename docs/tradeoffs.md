# Espacios de análisis de trade-offs

## Formato: CSV vs Parquet

Debe analizarse el equilibrio entre interoperabilidad, simplicidad y eficiencia de lectura analítica.

## Parquet vs Delta Lake

Parquet resuelve el almacenamiento columnar del dato. Delta Lake añade una capa de metadatos y capacidades de gestión de tablas. La discusión debe distinguir claramente formato de archivo y capa de gestión.

## DuckDB vs motor distribuido

DuckDB permite resolver el flujo con una infraestructura mínima y tiempos de respuesta adecuados para un dataset pequeño. Un motor distribuido aporta escalabilidad horizontal, pero introduce mayor complejidad operacional.

## Pseudonimización vs acceso

La pseudonimización reduce la exposición directa de identificadores, pero no sustituye autenticación, autorización ni control de acceso.

## Dataset Gold vs Feature Store

Una tabla Gold preparada para ML no constituye por sí misma un Feature Store. Un Feature Store completo añade capacidades de gobierno, versionamiento, consistencia train/serve y, dependiendo de la arquitectura, componentes online y offline.

## Serving integrado vs desacoplado

Un servicio dedicado permite desacoplar la inferencia de los procesos de entrenamiento y facilita evolucionar cada componente de forma independiente. El coste es mayor complejidad operacional.

## Data drift vs model degradation

La detección de cambio en la distribución de variables no demuestra por sí sola una degradación del rendimiento predictivo. Para medir esta última se requieren etiquetas y métricas de desempeño apropiadas.
