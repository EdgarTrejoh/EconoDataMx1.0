import pandas as pd
#import plotly.graph_objects as go
#import plotly.express as px
import streamlit as st
import yfinance as yf 
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, date

   
def cargar_datos_gsheets_economics(worksheet_name: str, columns: list= None):
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(worksheet=worksheet_name, usecols=columns, ttl=2).dropna()
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos de la hoja de cálculo '{worksheet_name}': {str(e)}")
        return None    

@st.cache_resource(ttl=600)  # Almacena en caché los resultados durante 1 hora (3600 segundos)
def cargar_datos_gsheets_banca(worksheet_name: str):
    conn = st.connection("gsheets_2", type=GSheetsConnection)
    try:
        df = conn.read(worksheet=worksheet_name).dropna()
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos de la hoja de cálculo '{worksheet_name}': {str(e)}")
        #st.rerun()
        return None
    
@st.cache_resource(ttl=600) 
def cargar_datos_yfinance(symbol: str, period: str):
    try:
        df = yf.download(symbol, period=period)
        
        if df.empty:
            raise ValueError(f"No se encontraron datos para el símbolo '{symbol}' en el periodo '{period}'")
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(0)  # Obtener los nombres de la segunda jerarquía

        column_names = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
        df.columns = column_names[:len(df.columns)] 

        return df
    
    except Exception as e:
        st.error(f"Error al cargar los datos de Yahoo Finance para el símbolo '{symbol}': {str(e)}")
        return None

def filtrar_por_fecha(df: pd.DataFrame, fecha_minima: str):
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Fecha'] = df["Fecha"].dt.strftime('%Y-%m-%d')
    df = df[df['Fecha'] >= fecha_minima]
    return df

def filtrar_por_fechas(df: pd.DataFrame, fecha_minima, fecha_maxima):
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
    fecha_minima = pd.to_datetime(fecha_minima, format='%Y-%m-%d' )
    fecha_maxima = pd.to_datetime(fecha_maxima, format='%Y-%m-%d' )
    df_filtrado = df[(df['Fecha'] >= fecha_minima) & (df['Fecha']<=fecha_maxima)]
    return df_filtrado

def obtener_tipo_cambio(symbol: str, periodo):
    df = cargar_datos_yfinance(symbol, periodo)

    if df is None or df.empty:
        return None, None, None, None
    
    if len(df) < 2:
        st.warning(f"Datos insuficientes para calcular el tipo de cambio de '{symbol}' en el periodo '{periodo}'")
        return df['Close'].iloc[-1], None, df.index[-1].strftime('%Y-%m-%d'), None
    
    ultimo = df['Close'].iloc[-1]
    previo = df['Close'].iloc[-2]
    fecha = df.index[-1].strftime('%Y-%m-%d')
    resumen = df.describe()
    return ultimo, previo, fecha, resumen

def obtener_inflacion():
    df = cargar_datos_gsheets_economics('IE_004', [0,2])
    ultimo = df['Inflación Anual'].iloc[-1]
    fecha = df['Fecha'].iloc[-1]
    previo = df['Inflación Anual'].iloc[-2]
    resumen = df['Inflación Anual'].describe()
    return ultimo, previo, fecha, resumen

def obtener_tasa_referencia():
    df = cargar_datos_gsheets_economics('IE_001', [0, 1])
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')

    calendario = cargar_datos_gsheets_economics('IE_001', [7])
    calendario['Date'] = pd.to_datetime(calendario['Date'], format='%d/%m/%Y')

    fecha_actual = datetime.now()
    fechas_pasadas = calendario[calendario['Date'] <= fecha_actual]
    fecha_reciente = fechas_pasadas['Date'].iloc[-2]

    tasa_previa = df.loc[df['Fecha'] == fecha_reciente, 'TasaReferencia'].values[0]
    fecha_ultima = df['Fecha'].iloc[-1]
    tasa_ultima = df['TasaReferencia'].iloc[-1]
    resumen = df['TasaReferencia'].describe()
    return tasa_ultima, tasa_previa, fecha_ultima, resumen

def obtener_pib():
    df = cargar_datos_gsheets_economics('IE_006', [2,3,4])
    fecha_ultima = df['Periodo'].iloc[-1]
    pib_ultimo = df['PIB (%)'].iloc[-1]
    resumen = df['Producto interno bruto'].describe()
    return pib_ultimo, fecha_ultima, resumen