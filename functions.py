import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import yfinance as yf 
from streamlit_gsheets import GSheetsConnection

class graficar():
    def __init__(self):
        self.graficar_linea
        self.graficar_linea_bis
    
    def graficar_linea(df: pd.DataFrame, x_col: str, y_col: str, title: str, y_name_col: str,  width: int = 80, height: int = 80, title_color: str = '#131212', line_color: str = '#A109A1'):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines', name=y_col, line=dict(color=line_color)))
        fig.update_layout(title=dict(text=title, font=dict(color=title_color)), xaxis_title=x_col, yaxis_title=y_name_col, width=width, height=height)
        return fig
    
    def graficar_linea_bis(df: pd.DataFrame, x_col, y_col, title, x_title = None, y_title = None, line_color= None, title_color=None, title_size=18, width=None, height=None):
        fig = px.line(df, x=x_col, y=y_col)
        
        if x_title:
            fig.update_xaxes(title_text = x_title)
        if y_title:
            fig.update_yaxes(title_text = y_title)
        
        fig.update_layout(
            title_text = title,
            title_font = dict(
                color = title_color,
                size = title_size
            )
        )

        fig.update_traces(line=dict(color = line_color))

        if width and height:
            fig.update_layout(width=width, height=height)

        return fig
    
    def graficar_lineas(df, x_col, y_cols, titles, width=None, height=None):
        fig = go.Figure()
    
        for y_col, title in zip(y_cols, titles):
            fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines', name=title))
            fig.update_layout(xaxis_title=x_col, yaxis_title="Tasa de interés (%)", width=width, height=height)
                
        return fig

    def cargar_datos_gsheets_economics(worksheet_name: str, columns: list= None):
        conn = st.connection("gsheets", type=GSheetsConnection)
        try:
            df = conn.read(worksheet=worksheet_name, usecols=columns, ttl=2).dropna()
            return df
        except Exception as e:
            st.error(f"Error al cargar los datos de la hoja de cálculo '{worksheet_name}': {str(e)}")
            #st.rerun()
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

    def cargar_datos_yfinance(symbol: str, period: str):
        try:
            df = yf.download(symbol, period=period)
            return df
        except Exception as e:
            st.error(f"Error al cargar los datos de Yahoo Finance para el símbolo '{symbol}': {str(e)}")
            return None

    def filtrar_por_fecha(df: pd.DataFrame, fecha_minima: str):
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Fecha'] = df["Fecha"].dt.strftime('%Y-%m-%d')
        df = df[df['Fecha'] >= fecha_minima]
        return df

