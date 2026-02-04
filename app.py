from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import RobustScaler
import os
import threading
import webbrowser
from datetime import datetime
import json

app = Flask(__name__)

# Configuración del modelo
MODEL_PATH = "Modelo/Modelo.joblib"
SCALER_PATH = "Modelo/scaler_X.joblib"

# IMPORTANTE: Usa EXACTAMENTE los mismos nombres que usaste al entrenar el modelo
FEATURES = ['Aves Ingresadas', 'Peso Promedio', 'Horas Productivas', 'LbsTotEquiv']

# Parámetros de la ecuación de línea base
A_BASELINE = 582.6204656920573
B_BASELINE = -0.713698689160424

# Almacenamiento histórico en memoria
historial_predicciones = []

# Archivo para persistencia (opcional)
HISTORIAL_FILE = "historial_predicciones.json"

# Variables globales para modelo y scaler
modelo_cargado = None
scaler_cargado = None


def cargar_modelo():
    """Carga el modelo (lo guardamos en joblib después del entrenamiento)"""
    global modelo_cargado
    if modelo_cargado is None:
        try:
            modelo_cargado = joblib.load(MODEL_PATH)
            print(f"✓ Modelo cargado exitosamente desde {MODEL_PATH}")
        except FileNotFoundError:
            raise Exception(f"No se encontró el modelo en: {MODEL_PATH}")
        except Exception as e:
            raise Exception(f"Error al cargar el modelo: {str(e)}")
    return modelo_cargado


def cargar_scaler():
    """Carga el scaler (necesario para normalizar los datos de entrada)"""
    global scaler_cargado
    if scaler_cargado is None:
        try:
            scaler_cargado = joblib.load(SCALER_PATH)
            print(f"✓ Scaler cargado exitosamente desde {SCALER_PATH}")
        except FileNotFoundError:
            raise Exception(f"No se encontró el scaler en: {SCALER_PATH}")
        except Exception as e:
            raise Exception(f"Error al cargar el scaler: {str(e)}")
    return scaler_cargado


def calcular_ide_baseline(lbs_tot_equiv):
    """Calcula el IDE de línea base con la ecuación de potencia que obtuvimos"""
    return A_BASELINE * (lbs_tot_equiv ** B_BASELINE)


def calcular_consumo_energetico(ide_modelo, lbs_tot_equiv):
    """Estima el consumo en kWh multiplicando IDE por libras procesadas"""
    return ide_modelo * lbs_tot_equiv


def calcular_eficiencia_operacional(aves_ingresadas, horas_productivas):
    """Calcula qué tan eficientes fuimos en el procesamiento (aves por hora normalizado)"""
    if horas_productivas == 0:
        return 0
    return (aves_ingresadas / horas_productivas) / 14000


def calcular_desviacion_ide(ide_modelo, ide_baseline):
    """Calcula cuánto nos desviamos del estándar (mejor o peor en %)"""
    if ide_baseline == 0:
        return 0
    return ((ide_modelo - ide_baseline) / ide_baseline) * 100


def guardar_historial():
    """Persiste el historial en JSON para no perder los datos entre sesiones"""
    try:
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(historial_predicciones, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar historial: {e}")


def cargar_historial():
    """Recupera el historial guardado cuando inicia la app"""
    global historial_predicciones
    try:
        if os.path.exists(HISTORIAL_FILE):
            with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
                historial_predicciones = json.load(f)
    except Exception as e:
        print(f"Error al cargar historial: {e}")
        historial_predicciones = []


@app.route('/')
def index():
    """Mostrar el formulario principal"""
    return render_template('index.html', features=FEATURES)


@app.route('/predecir', methods=['POST'])
def predecir():
    """Procesar la predicción con todos los cálculos del IDE y métricas"""
    try:
        # 1. Leer y validar los valores del formulario
        valores = []
        valores_dict = {}
        
        print("\n\n")
        print("█" * 60)
        print("█ DEBUG - NUEVA PREDICCIÓN")
        print("█" * 60)
        
        # Imprimir TODOS los datos del formulario
        print("\n1. DATOS DEL FORMULARIO:")
        for key in request.form:
            print(f"     '{key}' = '{request.form.get(key)}'")
        
        print("\n2. PROCESANDO FEATURES:")
        for feature in FEATURES:
            valor = request.form.get(feature)
            print(f"     '{feature}' -> {valor}", end="")
            
            if not valor:
                return render_template('index.html', 
                                     features=FEATURES,
                                     error=f"El campo '{feature}' es obligatorio")
            try:
                valor_float = float(valor)
                valores.append(valor_float)
                valores_dict[feature] = valor_float
                print(f" ✓ ({valor_float})")
            except ValueError:
                return render_template('index.html',
                                     features=FEATURES,
                                     error=f"El campo '{feature}' debe ser un número válido")
        
        # DEBUG: Imprimir valores recibidos
        print("\n3. VALORES PROCESADOS:")
        print(f"     Lista: {valores}")
        print(f"     Dict: {valores_dict}")
        
        # 2. Preparar datos para el modelo en el ORDEN CORRECTO
        # Usar DataFrame para mantener los nombres de las columnas
        df_entrada = pd.DataFrame([valores], columns=FEATURES)
        print("\n4. DATAFRAME DE ENTRADA:")
        print(df_entrada)
        print(f"     Columnas: {list(df_entrada.columns)}")
        
        # 3. Cargar el scaler y aplicarlo
        scaler_X = cargar_scaler()
        print("\n5. APLICANDO SCALER...")
        
        # Transformar y mantener como DataFrame para el Pipeline
        datos_escalados_array = scaler_X.transform(df_entrada)
        df_escalado = pd.DataFrame(
            datos_escalados_array,
            columns=FEATURES
        )
        
        print(f"     Array: {datos_escalados_array[0]}")
        print("     DataFrame escalado:")
        print(df_escalado)
        
        # 4. Cargar el modelo y hacer predicción
        modelo = cargar_modelo()
        print("\n6. PREDICCIÓN:")
        print(f"     Tipo de modelo: {type(modelo).__name__}")
        
        ide_modelo = modelo.predict(df_escalado)[0]
        
        print(f"     ✓ IDE MODELO: {ide_modelo}")
        print("█" * 60)
        print("\n")
        
        # 5. Realizar todos los cálculos adicionales
        # IMPORTANTE: Usar el nombre correcto de la variable
        lbs_tot_equiv = valores_dict['LbsTotEquiv']
        aves_ingresadas = valores_dict['Aves Ingresadas']
        horas_productivas = valores_dict['Horas Productivas']
        
        # Cálculo IDE de línea base
        ide_baseline = calcular_ide_baseline(lbs_tot_equiv)
        print(f"IDE Baseline calculado: {ide_baseline}")
        
        # Cálculo consumo energético
        kwh = calcular_consumo_energetico(ide_modelo, lbs_tot_equiv)
        print(f"Consumo energético (kWh): {kwh}")
        
        # Cálculo eficiencia operacional
        eficiencia_op = calcular_eficiencia_operacional(aves_ingresadas, horas_productivas)
        print(f"Eficiencia operacional: {eficiencia_op}")
        
        # Cálculo desviación IDE
        desviacion_ide = calcular_desviacion_ide(ide_modelo, ide_baseline)
        print(f"Desviación IDE (%): {desviacion_ide}")
        print("="*60 + "\n")
        
        # 6. Guardar en historial
        registro = {
            'fecha_hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'lbs_tot_equiv': lbs_tot_equiv,
            'ide_modelo': float(ide_modelo),  # Asegurar que sea float serializable
            'ide_baseline': float(ide_baseline),
            'kwh': float(kwh),
            'eficiencia_operacional': float(eficiencia_op),
            'desviacion_ide': float(desviacion_ide),
            'datos_entrada': valores_dict
        }
        
        historial_predicciones.append(registro)
        guardar_historial()
        
        # 7. Preparar datos para la vista
        resultados = {
            'ide_modelo': float(ide_modelo),
            'ide_baseline': float(ide_baseline),
            'kwh': float(kwh),
            'eficiencia_op': float(eficiencia_op),
            'desviacion_ide': float(desviacion_ide),
            'desviacion_tipo': 'mejor' if desviacion_ide < 0 else 'peor'
        }
        
        return render_template('resultado.html',
                             resultados=resultados,
                             datos_entrada=valores_dict,
                             historial=historial_predicciones)
    
    except Exception as e:
        print(f"\n❌ ERROR EN PREDICCIÓN: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('index.html',
                             features=FEATURES,
                             error=f"Error al realizar la predicción: {str(e)}")


@app.route('/api/historial')
def api_historial():
    """Devolver el historial en JSON (para consumo de APIs)"""
    return jsonify(historial_predicciones)


@app.route('/historial')
def ver_historial():
    """Ver todo el historial de predicciones en la web"""
    return render_template('historial.html', historial=historial_predicciones)


@app.route('/limpiar_historial', methods=['POST'])
def limpiar_historial():
    """Borrar todo el historial cuando lo necesites"""
    global historial_predicciones
    historial_predicciones = []
    guardar_historial()
    return render_template('index.html', 
                         features=FEATURES,
                         mensaje="Historial limpiado correctamente")


if __name__ == '__main__':
    # Cargar historial previo si existe
    cargar_historial()
    
    # Verificar que existen el modelo y scaler antes de iniciar
    print("\n" + "="*60)
    print("  SISTEMA DE MONITOREO ENERGÉTICO INDUSTRIAL")
    print("  Predicción IDE - Análisis de Desempeño")
    print("="*60)
    
    # Verificar modelo
    if not os.path.exists(MODEL_PATH):
        print(f"❌ ERROR: No se encuentra el modelo en:")
        print(f"   {MODEL_PATH}")
        print("   Por favor, verifica la ruta del modelo.")
    else:
        print(f"✓ Modelo encontrado: {MODEL_PATH}")
    
    # Verificar scaler
    if not os.path.exists(SCALER_PATH):
        print(f"❌ ERROR: No se encuentra el scaler en:")
        print(f"   {SCALER_PATH}")
        print("   Por favor, verifica la ruta del scaler.")
    else:
        print(f"✓ Scaler encontrado: {SCALER_PATH}")
    
    print(f"\n  Features esperadas: {FEATURES}")
    print("  URL: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    # Cargar modelo y scaler al inicio
    try:
        cargar_modelo()
        cargar_scaler()
    except Exception as e:
        print(f"❌ Error al cargar modelo/scaler: {e}")
    
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()

    # Iniciar servidor Flask
    app.run(debug=True, host='127.0.0.1', port=5000)