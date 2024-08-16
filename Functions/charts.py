import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_chart(df: pd.DataFrame, x_col, y_col, title, x_title = None, y_title = None, line_color= None, title_color=None, title_size=18, width=None, height=None):
    fig = px.line(df, x = x_col, y = y_col)

    max_value = df[y_col].max()
    min_value = df[y_col].min()
    max_point = df[df[y_col]== max_value]
    min_point = df[df[y_col]== min_value]

    fig.add_scatter(x=max_point[x_col], y = max_point[y_col], mode = 'markers+text', name="Max",
                    text= 'Max', textposition='top right', marker=dict(color='red', size=10))   

    fig.add_scatter(x=min_point[x_col], y=min_point[y_col], mode='markers+text', name="Min",
                    text='Min', textposition='bottom right', marker=dict(color='blue', size=10))
    if x_title:
        fig.update_xaxes(title_text = x_title)
    if y_title:
        fig.update_yaxes(title_text = y_title)
        
    fig.update_layout(
        title_text = title,
        title_font = dict(
            color = title_color,
            size = title_size
            ),
        hovermode="x unified"  # Hover unificado para mayor claridad
    )
    
    # Cambiar estilo de línea y color
    fig.update_traces(line=dict(width=3.5, color = "#2A3A4B", dash='dash'), line_color=line_color)
    #line_color
    if width and height:
        fig.update_layout(width=width, height=height)

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