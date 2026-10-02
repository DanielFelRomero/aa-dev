# Guía de ejecución — AA Dev

## 1. Propósito de la sesión

La práctica se desarrolla como una secuencia guiada de cuatro etapas. En cada etapa se ejecuta un componente preconstruido, se observa el estado resultante de la arquitectura y se dedica un espacio breve al análisis de decisiones y trade-offs.

No se requiere modificar el código base para completar el recorrido. Las modificaciones de parámetros o datos se realizan únicamente cuando la guía las solicita como experimento.

## 2. Antes de comenzar

### Opción recomendada: GitHub Codespaces

1. Abrir el repositorio `aa-dev`.
2. Seleccionar **Code → Codespaces → Create codespace on main**.
3. Esperar la construcción del Dev Container.
4. Verificar que la terminal se encuentre en la raíz del repositorio.
5. Ejecutar:

```bash
make setup
make test
```

Se espera que las pruebas finalicen correctamente.

### ¿Se requiere configuración adicional?

En un Codespace correctamente construido no se requiere configuración adicional de servicios, credenciales, bases de datos externas ni variables de entorno.

El flujo utiliza exclusivamente el dataset sintético incluido en el repositorio y almacenamiento local.

En caso de utilizar un entorno local fuera de Codespaces, se requiere Python 3.12, las dependencias de `requirements.txt` y `make`.

## 3. Mapa de la práctica

| Etapa | Resultado principal | Evidencia que debe observarse | Discusión |
|---|---|---|---|
| 1 | Bronze | Tabla Delta y consulta analítica | Formatos y Lakehouse |
| 2 | Silver + Gold | Datos transformados y protegidos | Calidad y gobierno |
| 3 | Modelo + API | Métrica de entrenamiento y endpoint | Separación ML/serving |
| 4 | Monitoreo | Calidad y drift | Observabilidad y trade-offs |

---

# Etapa 1. Ingesta y almacenamiento

## Objetivo

Observar la transición desde el dato fuente hasta una capa Bronze gestionada como tabla Delta y consultable mediante DuckDB.

## Paso 1. Inspección del origen

Ejecutar:

```bash
head data/source/customers.csv
```

Revisar:

- columnas;
- tipos aparentes;
- variable objetivo;
- identificador técnico;
- ausencia de datos personales reales.

### Pregunta para discusión

¿Por qué el CSV puede ser suficiente como formato de intercambio, pero no necesariamente como formato principal de almacenamiento analítico?

## Paso 2. Ejecutar la ingesta

Ejecutar:

```bash
PYTHONPATH=src python scripts/01_ingest.py
```

Después revisar:

```bash
find data/bronze/customers_delta -maxdepth 2 -type f | sort
```

### Qué debe observarse

Debe aparecer una estructura de tabla Delta, incluyendo archivos de datos y metadatos de transacciones.

La discusión debe separar tres conceptos:

- formato de archivo;
- tabla gestionada;
- arquitectura Lakehouse.

## Paso 3. Analizar DuckDB

Ejecutar:

```bash
python -c "import duckdb; c=duckdb.connect(); c.execute('INSTALL delta'); c.execute('LOAD delta'); print(c.execute(\"SELECT COUNT(*) FROM delta_scan('data/bronze/customers_delta')\").fetchone()); c.close()"
```

### Pregunta de trade-off

¿Qué se gana utilizando DuckDB para este escenario local y qué se perdería frente a un motor distribuido?

### Tiempo sugerido

35–40 minutos.

---

# Etapa 2. Transformación, calidad y gobierno

## Objetivo

Observar cómo una capa Silver puede aplicar transformación, controles básicos de calidad y pseudonimización antes de generar un dataset Gold orientado al consumo analítico y a ML.

## Paso 1. Ejecutar transformación

Ejecutar:

```bash
PYTHONPATH=src python scripts/02_transform.py
```

## Paso 2. Revisar Silver

Inspeccionar el contenido:

```bash
find data/silver/customers_delta -maxdepth 2 -type f | sort
```

Y realizar una consulta rápida:

```bash
python -c "from deltalake import DeltaTable; print(DeltaTable('data/silver/customers_delta').to_pandas().head())"
```

### Qué debe observarse

El identificador original `customer_id` ya no forma parte de la tabla Silver. En su lugar aparece `customer_key`.

### Discusión

La transformación utiliza SHA-256 con un salt fijo para producir una clave determinística.

La discusión debe establecer que:

- la técnica corresponde a pseudonimización, no a anonimización completa;
- no reemplaza autenticación ni autorización;
- no constituye por sí sola control de acceso a columnas;
- existe un trade-off entre utilidad analítica y exposición del identificador.

## Paso 3. Revisar Gold

Ejecutar:

```bash
python -c "import pandas as pd; df=pd.read_parquet('data/gold/features.parquet'); print(df.head()); print(df.columns.tolist())"
```

### Pregunta de análisis

¿Por qué esta tabla puede considerarse una capa de características para ML, pero no un Feature Store completo?

## Experimento opcional de aula

Modificar de forma temporal un valor de `data/source/customers.csv` y ejecutar nuevamente las etapas 1 y 2.

Observar:

- propagación del cambio;
- reproducibilidad;
- necesidad de volver a generar capas derivadas.

### Tiempo sugerido

40–45 minutos.

---

# Etapa 3. Entrenamiento y model serving

## Objetivo

Observar la separación entre la preparación de datos, el entrenamiento del modelo y la inferencia expuesta como servicio.

## Paso 1. Entrenar

Ejecutar:

```bash
PYTHONPATH=src python scripts/03_train.py
```

Registrar mentalmente:

- métrica mostrada;
- partición train/test;
- algoritmo;
- preprocesamiento;
- persistencia del artefacto.

### Pregunta de análisis

¿Qué responsabilidades corresponden al entrenamiento y cuáles al serving?

## Paso 2. Inspeccionar el artefacto

Ejecutar:

```bash
ls -lh data/gold/model.joblib
```

El archivo representa el artefacto utilizado posteriormente por el servicio.

## Paso 3. Iniciar FastAPI

Ejecutar:

```bash
make serve
```

Mantener esta terminal abierta.

Abrir una segunda terminal y ejecutar:

```bash
curl http://127.0.0.1:8000/health
```

Se espera:

```json
{"status":"ok"}
```

## Paso 4. Ejecutar una inferencia

Ejecutar:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age":40,"monthly_spend":90.0,"tenure_months":24,"support_calls":4}'
```

## Paso 5. Observar la API gráficamente

FastAPI genera automáticamente documentación interactiva.

Abrir en el navegador:

```
http://127.0.0.1:8000/docs
```

Esta vista permite ejecutar `/health` y `/predict` sin utilizar `curl`.

### Discusión de trade-off

¿Qué ventajas aporta un servicio separado frente a ejecutar directamente el modelo desde el mismo proceso de transformación?

### Tiempo sugerido

35–40 minutos.

---

# Etapa 4. Observabilidad y análisis de trade-offs

## Objetivo

Observar indicadores básicos sobre calidad de datos y distribución de variables, y diferenciar observabilidad de datos, servicio y modelo.

## Paso 1. Ejecutar monitoreo

Con el servicio aún ejecutándose o después de detenerlo, abrir otra terminal y ejecutar:

```bash
PYTHONPATH=src python scripts/05_observe.py
```

Revisar:

- número de registros;
- tasa de valores faltantes;
- cambio relativo de media;
- bandera de drift.

## Paso 2. Interpretar drift

La detección de drift no debe interpretarse automáticamente como degradación del modelo.

### Preguntas para discusión

- ¿Qué está observando realmente el indicador?
- ¿Qué evidencia adicional sería necesaria para afirmar degradación predictiva?
- ¿Qué diferencia existe entre data quality monitoring, service monitoring y model monitoring?

## Paso 3. Cierre arquitectónico

Revisar:

```
docs/architecture.md
docs/tradeoffs.md
```

Seleccionar una de las decisiones discutidas:

- CSV vs Parquet;
- Parquet vs Delta Lake;
- DuckDB vs procesamiento distribuido;
- pseudonimización vs acceso;
- Gold para ML vs Feature Store;
- serving integrado vs desacoplado;
- indicador de drift vs métricas de desempeño.

La discusión debe centrarse en:

1. contexto;
2. restricción;
3. alternativa;
4. atributo de calidad afectado;
5. trade-off;
6. consecuencia arquitectónica.

No se requiere crear un documento ni registrar formalmente la respuesta.

### Tiempo sugerido

35–40 minutos.

---

# Recorrido completo

Para una ejecución lineal, el orden recomendado es:

```bash
make setup
make test
PYTHONPATH=src python scripts/01_ingest.py
PYTHONPATH=src python scripts/02_transform.py
PYTHONPATH=src python scripts/03_train.py
make serve
```

En una segunda terminal:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age":40,"monthly_spend":90.0,"tenure_months":24,"support_calls":4}'
PYTHONPATH=src python scripts/05_observe.py
```

# ¿Qué se debe mirar durante la práctica?

El objetivo no es únicamente comprobar que los comandos terminan sin error. En cada etapa debe observarse el estado arquitectónico resultante.

| Momento | Evidencia |
|---|---|
| Fuente | CSV original |
| Bronze | Tabla Delta |
| Silver | Transformación y pseudonimización |
| Gold | Dataset de características |
| Training | Modelo persistido y métrica |
| Serving | Endpoint de inferencia |
| Monitoring | Indicadores de calidad y drift |

# ¿Qué ocurre si algo falla?

Antes de modificar código:

1. Revisar que el Codespace se haya construido completamente.
2. Ejecutar `make test`.
3. Confirmar que el comando anterior de la secuencia terminó correctamente.
4. Revisar que las carpetas derivadas existan.
5. Ejecutar nuevamente la etapa correspondiente.

Para reiniciar completamente el flujo:

```bash
make clean
make run-all
```

Después puede iniciarse nuevamente el servicio:

```bash
make serve
```

# Criterio pedagógico

La práctica debe ejecutarse como una experiencia de arquitectura:

**ejecutar → observar → interpretar → discutir → relacionar con una decisión arquitectónica**.

El código está preconstruido para reducir carga de implementación y desplazar la actividad hacia la comprensión de componentes, responsabilidades, atributos de calidad, restricciones y trade-offs.
