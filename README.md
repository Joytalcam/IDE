# Sistema de Monitoreo Energético Industrial - Predicción IDE

Aplicación web para predecir y analizar el **Índice de Desempeño Energético (IDE)** en instalaciones de procesamiento avícola usando Machine Learning.

## Descripción General

Este proyecto es una aplicación Flask que permite:
- **Predecir** el IDE (eficiencia energética) basado en datos operacionales
- **Calcular** métricas energéticas derivadas (consumo en kWh, desviación del estándar)
- **Mantener un historial** de todas las predicciones realizadas
- **Visualizar** resultados comparativos contra línea base industrial

La aplicación utiliza un modelo de Machine Learning pre-entrenado y un scaler para normalizar los datos de entrada.

## Características Principales

- Interfaz web intuitiva para ingreso de datos
- Predicción en tiempo real usando modelo ML entrenado
- Cálculos automáticos de métricas energéticas:
  - IDE predicho por el modelo
  - IDE de línea base (ecuación de potencia)
  - Consumo energético (kWh)
  - Eficiencia operacional
  - Desviación IDE (% mejor/peor)
- Historial persistente en JSON
- Vista de historial completo de predicciones
- API REST para obtener datos del historial
- Limpiar historial bajo demanda
- Logs detallados en consola para debugging

## Prerequisitos

### Requisitos del Sistema
- **Python 3.7 o superior** (recomendado 3.9+)
- **Windows, macOS o Linux**
- **Al menos 2GB de RAM libre**

### Dependencias Python Requeridas
```
Flask==2.3.0          # Framework web
pandas==1.5.0         # Manipulación de datos
scikit-learn==1.2.0   # Machine Learning (modelos, escalado)
joblib==1.2.0         # Serialización de modelos
```

### Archivos de Modelo Requeridos
El proyecto requiere dos archivos en la carpeta `Modelo/`:
- `Modelo.joblib` - Modelo pre-entrenado de Machine Learning
- `scaler_X.joblib` - Scaler para normalización de datos

## Instalación

### 1. Clonar o descargar el proyecto
```bash
# Si está en un repositorio git
git clone <url-del-repositorio>
cd "APP3"
```

### 2. Crear un entorno virtual (recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

O instalarlas manualmente:
```bash
pip install Flask==2.3.0 pandas==1.5.0 scikit-learn==1.2.0 joblib==1.2.0
```

### 4. Verificar estructura de carpetas
Asegúrate de que la estructura sea:
```
APP3/
├── app.py
├── historial_predicciones.json  (se crea automáticamente)
├── requirements.txt
├── README.md
├── Modelo/
│   ├── Modelo.joblib
│   └── scaler_X.joblib
└── templates/
    ├── index.html
    ├── resultado.html
    └── historial.html
```

**IMPORTANTE:** Los archivos `Modelo.joblib` y `scaler_X.joblib` deben estar en la carpeta `Modelo/` para que la aplicación funcione.

##  Cómo Ejecutar

### Opción 1: Ejecutar desde PowerShell
```powershell
python app.py
```

### Opción 2: Ejecutar desde CMD
```cmd
python app.py
```

La aplicación se iniciará en: **http://127.0.0.1:5000**

Se abrirá automáticamente en tu navegador predeterminado.

### Salida esperada en consola
```
============================================================
  SISTEMA DE MONITOREO ENERGÉTICO INDUSTRIAL
  Predicción IDE - Análisis de Desempeño
============================================================
✓ Modelo encontrado: Modelo/Modelo.joblib
✓ Scaler encontrado: Modelo/scaler_X.joblib

  Features esperadas: ['Aves Ingresadas', 'Peso Promedio', 'Horas Productivas', 'LbsTotEquiv']
  URL: http://127.0.0.1:5000
============================================================
```

## Estructura del Proyecto

```
APP3/
├── app.py                          # Aplicación principal Flask
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
├── historial_predicciones.json    # Historial persistente (creado automáticamente)
│
├── Modelo/
│   ├── Modelo.joblib             # Modelo entrenado de ML
│   └── scaler_X.joblib           # Normalizador RobustScaler
│
└── templates/
    ├── index.html                 # Página principal con formulario
    ├── resultado.html             # Página de resultados de predicción
    └── historial.html             # Página del historial completo
```

## Cómo Usar la Aplicación

### Paso 1: Completar el Formulario
La página principal muestra un formulario con los siguientes campos obligatorios:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| **Aves Ingresadas** | Número | Cantidad total de aves procesadas |
| **Peso Promedio** | Número | Peso promedio en libras |
| **Horas Productivas** | Número | Horas de operación productiva |
| **LbsTotEquiv** | Número | Libras totales equivalentes procesadas |

### Paso 2: Enviar Predicción
Haz clic en el botón "Predecir" para procesar los datos.

### Paso 3: Ver Resultados
Se mostrarán los siguientes cálculos:
- **IDE Modelo**: Predicción de la red neuronal
- **IDE Baseline**: Estándar industrial calculado
- **Desviación IDE**: Porcentaje diferencia (negativo = mejor eficiencia)
- **Consumo Energético (kWh)**: IDE × Lbs Tot Equiv
- **Eficiencia Operacional**: Métrica normalizada de productividad

### Paso 4: Ver Historial
- Haz clic en "Ver Historial" para ver todas las predicciones
- Cada entrada muestra fecha, hora y todos los datos calculados
- Opción para limpiar todo el historial

## Rutas/Endpoints

### Rutas Web (GET/POST)

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Página principal con formulario |
| `/predecir` | POST | Procesar predicción y cálculos |
| `/historial` | GET | Ver historial completo en HTML |
| `/limpiar_historial` | POST | Limpiar historial de predicciones |

### API REST

| Ruta | Método | Descripción | Retorna |
|------|--------|-------------|---------|
| `/api/historial` | GET | Obtener historial en JSON | Array de predicciones |

**Ejemplo de uso de API:**
```bash
curl http://127.0.0.1:5000/api/historial
```

**Respuesta:**
```json
[
  {
    "fecha_hora": "2026-02-03 14:30:45",
    "lbs_tot_equiv": 500.5,
    "ide_modelo": 0.245,
    "ide_baseline": 0.312,
    "kwh": 122.725,
    "eficiencia_operacional": 0.0071,
    "desviacion_ide": -21.47,
    "datos_entrada": {
      "Aves Ingresadas": 5000,
      "Peso Promedio": 2.1,
      "Horas Productivas": 24,
      "LbsTotEquiv": 500.5
    }
  }
]
```

## Configuración

### Variables Clave en `app.py`

```python
# Rutas de modelos (relativas a carpeta del proyecto)
MODEL_PATH = "Modelo/Modelo.joblib"
SCALER_PATH = "Modelo/scaler_X.joblib"

# Features esperadas (DEBEN coincidir exactamente con el entrenamiento)
FEATURES = ['Aves Ingresadas', 'Peso Promedio', 'Horas Productivas', 'LbsTotEquiv']

# Parámetros de la ecuación IDE baseline (a * x^b)
A_BASELINE = 582.6204656920573
B_BASELINE = -0.713698689160424

# Archivo de persistencia
HISTORIAL_FILE = "historial_predicciones.json"
```

### Configuración del Servidor Flask
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```

- `debug=True`: Modo desarrollo (recarga automática en cambios)
- `host='127.0.0.1'`: Solo accesible localmente
- `port=5000`: Puerto de escucha

**Para acceso remoto**, cambia a `host='0.0.0.0'` en `app.py`.

## Funciones Principales

### Predicción
```python
def predecir()
```
- Valida entrada de datos
- Normaliza con scaler
- Predice IDE con el modelo
- Calcula todas las métricas derivadas
- Guarda en historial y JSON

### Cálculos Implementados

**IDE Baseline:**
```
IDE_baseline = 582.62 × (LbsTotEquiv ^ -0.714)
```

**Consumo Energético:**
```
kWh = IDE_modelo × LbsTotEquiv
```

**Eficiencia Operacional:**
```
Eficiencia = (Aves Ingresadas / Horas Productivas) / 14000
```

**Desviación IDE:**
```
Desviación (%) = ((IDE_modelo - IDE_baseline) / IDE_baseline) × 100
```

## Historial

El historial se persiste automáticamente en `historial_predicciones.json`:

```json
[
  {
    "fecha_hora": "2026-02-03 14:30:45",
    "lbs_tot_equiv": 500.5,
    "ide_modelo": 0.245,
    "ide_baseline": 0.312,
    "kwh": 122.725,
    "eficiencia_operacional": 0.0071,
    "desviacion_ide": -21.47,
    "datos_entrada": {...}
  }
]
```

Este archivo:
- Se crea automáticamente en la primera predicción
- Se carga al iniciar la aplicación
- Se actualiza después de cada nueva predicción
- Puede ser limpiado desde la interfaz

## Solución de Problemas

### Error: "No se encontró el modelo en..."
```
ERROR: No se encuentra el modelo en:
   Modelo/Modelo.joblib
```
**Solución:** Verifica que los archivos `Modelo.joblib` y `scaler_X.joblib` estén en la carpeta `Modelo/`

### Error: "El campo 'XYZ' es obligatorio"
**Solución:** Completa todos los campos del formulario. Deben ser números válidos.

### Puerto 5000 ya en uso
```
Address already in use
```
**Solución:** 
- Cierra otras aplicaciones usando el puerto 5000, o
- Cambia el puerto en `app.py`: `app.run(port=5001)`

### La aplicación no se abre automáticamente en el navegador
**Solución:** Abre manualmente http://127.0.0.1:5000 en tu navegador

### Error de importación (Module not found)
```
ModuleNotFoundError: No module named 'flask'
```
**Solución:** 
- Activa el entorno virtual
- Ejecuta: `pip install -r requirements.txt`

## Logs y Debugging

La aplicación genera logs detallados en consola durante la predicción:

```
====================================================
DEBUG - NUEVA PREDICCIÓN
====================================================

1. DATOS DEL FORMULARIO:
     'Aves Ingresadas' = '5000'
     'Peso Promedio' = '2.1'
     ...

2. PROCESANDO FEATURES:
     'Aves Ingresadas' -> 5000.0
     ...

3. VALORES PROCESADOS:
     Lista: [5000.0, 2.1, 24.0, 500.5]
     Dict: {...}

4. DATAFRAME DE ENTRADA:
   Aves Ingresadas  Peso Promedio  Horas Productivas  LbsTotEquiv
        5000.0           2.1              24.0          500.5

5. APLICANDO SCALER...
   Array: [0.245, ...]

6. PREDICCIÓN:
     Tipo de modelo: Pipeline
     IDE MODELO: 0.245
```

Estos logs ayudan a verificar que:
- Los datos se reciben correctamente
- El escalado es consistente
- La predicción se ejecuta exitosamente

## Notas de Seguridad

- La aplicación actualmente usa `debug=True` (solo para desarrollo)
- Acceso limitado a `127.0.0.1` (localhost)
- Para producción:
  - Cambia `debug=False`
  - Configura `host='0.0.0.0'` solo si es necesario acceso remoto
  - Implementa autenticación

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|----------|
| Python | 3.7+ | Lenguaje base |
| Flask | 2.3.0 | Framework web |
| Pandas | 1.5.0 | Procesamiento de datos |
| Scikit-learn | 1.2.0 | Modelos ML y escalado |
| Joblib | 1.2.0 | Serialización de modelos |
| HTML/CSS/JS | - | Interfaz frontend |

## Mejoras Futuras

- [ ] Gráficos de tendencias en el historial
- [ ] Exportar historial a Excel/CSV
- [ ] Autenticación de usuarios
- [ ] Base de datos en lugar de JSON
- [ ] Predicciones por lotes
- [ ] Alertas si desviación excede umbral
- [ ] Dashboard con KPIs
- [ ] Comparación entre periodos

## Licencia

Proyecto de TFM - UNIR 2025

## Autor

Ana María Jaramillo P.  
Universidad Internacional de La Rioja (UNIR)  
Trabajo de Fin de Máster - 2025


---

**Última actualización:** Febrero 3, 2026
