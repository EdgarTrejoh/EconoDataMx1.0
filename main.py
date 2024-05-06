import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import functions as fc
from streamlit_option_menu import option_menu
from st_paywall import add_auth

#Main page configuration
st.set_page_config(
     page_title="Inicio", 
     page_icon=":turtle:",
     #layout="wide",
     )

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def main():
    st.title(':green[ECONODATA-MX]')

    # Opción del menú
    menu_options = option_menu(
        menu_title='Menú Principal',
        options=["Inicio", "Indicadores", "Banca", "Vivienda", "Referencias"],
        icons=["rocket-takeoff-fill", "bar-chart-fill", "bank2", "house-fill", "bookmark-fill"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#DDE4EA"},
            "icon": {"color": "orange", "font-size": "15px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "center",
                "margin": "1px",
                "--hover-color": "#eee"
            },
            "nav-link-selected": {"background-color": "green"},
        }
    )

    if menu_options == "Inicio":
        st.title(f"Sección actual: {menu_options}")
        st.markdown("""
                    > *El objetivo del presente sitio es proporcionar 
                    información que refleje la evolución de diferentes 
                    indicadores económicos, así como  la condición financiera 
                    de la Banca Múltiple en México.*
        
                    """
                    )
        periodo = "1mo"
        
        #Obtener información para resumen de tipo de cambio y-finance
        df_tipo_cambio = fc.graficar.cargar_datos_yfinance('USDMXN=X', periodo)
        df_tipo_cambio_ultimo = df_tipo_cambio['Close'].iloc[-1]
        df_tc_fecha = df_tipo_cambio.index[-1]
        df_tc_fecha_str = df_tc_fecha.strftime('%Y-%m-%d')
        resumen_tipo_cambio = df_tipo_cambio.describe()
        
        #Obtener información para resumen de inflación
        df_inflacion = fc.graficar.cargar_datos_gsheets_economics('IE_004', [0,2])
        df_inflacion_ultimo = df_inflacion['Inflación Anual'].iloc[-1]
        df_inflacion_fecha = df_inflacion['Fecha'].iloc[-1] 
        resumen_df_inflacion = df_inflacion['Inflación Anual'].describe()
        
        #Obtener información para resumen de tasa de referencia Banxico
        df_tasa_referencia = fc.graficar.cargar_datos_gsheets_economics('IE_001', [0, 1])
        df_tasa_referencia_fecha = df_tasa_referencia['Fecha'].iloc[-1]
        df_resumen_tasa_referencia = df_tasa_referencia['TasaReferencia'].describe()
        df_tasa_referencia_ultimo = df_tasa_referencia['TasaReferencia'].iloc[-1]
        
        #Obtener información para resumen del PIB
        df_pib = fc.graficar.cargar_datos_gsheets_economics('IE_006', [2,3,4])
        df_pib_fecha = df_pib['Periodo'].iloc[-1]
        df_resumen_pib = df_pib['Producto interno bruto'].describe()
        df_pib_ultimo = df_pib ['PIB (%)'].iloc[-1] 
        st.subheader("Principales índices")
        
        indicador1, indicador2, indicador3, indicador4 =st.columns(4, gap='medium')
        
        with indicador1:
            st.info(':blue[Tipo de Cambio]', icon= "📌")
            st.metric(label="USD/MXP", value=f"${df_tipo_cambio_ultimo:,.2f}")
            st.text(f"Corte: {df_tc_fecha_str}")
            st.text(resumen_tipo_cambio)

        with indicador2:
            st.info(':blue[Tasa Referencia]', icon="📌")
            st.metric(label="Banxico", value=f"{df_tasa_referencia_ultimo:,.2f} %")
            st.text(f'Corte: {df_tasa_referencia_fecha}')
            st.text(df_resumen_tasa_referencia)

        with indicador3:
            st.info(':blue[Inflación Anual]',icon="📌")
            st.metric(label="INEGI", value=f"{df_inflacion_ultimo:,.2f} %")
            st.text(f"Corte: {df_inflacion_fecha}")
            st.text(resumen_df_inflacion)

        with indicador4:
            st.info(':blue[Variacion Anual PIB]',icon= "📌")
            st.metric(label="INEGI", value=f"{df_pib_ultimo:,.2f} %")
            st.text(f'Trimestre: {df_pib_fecha}')
            st.text(df_resumen_pib)
            
    #add_auth(required=True,
    #        login_button_text="Login with Google",
    #        login_button_color="#FD504D",
    #        login_sidebar=True)

    if menu_options == "Indicadores":
        st.title(f"Sección actual: {menu_options}")

        # Cargar datos de GSheets
        df_IE004 = fc.graficar.cargar_datos_gsheets_economics('IE_004', [0, 1, 2])
        if df_IE004 is not None:
            df_IE004 = pd.DataFrame(df_IE004)
            df_IE004 = fc.graficar.filtrar_por_fecha(df_IE004, '2000-01-01')
        
            # Crear las pestañas y la división de la página una sola vez
            tabs = st.tabs([":chart_with_upwards_trend: Inflacion", ":heavy_dollar_sign: Tipo de Cambio", ":classical_building: Tasa de Referencia", ":building_construction: PIB"])
            
            with tabs[0]:  # Pestaña de Inflacion

                # Dividir la página en dos columnas
                col1, col2 = st.columns([1,1], gap='medium')

                # Mostrar una gráfica en la primera columna
                with col1:
                    st.plotly_chart(fc.graficar.graficar_linea_bis(df_IE004, 'Fecha', 'SP1', 'Evolución Histórica del INPC','Fecha', 'INPC', width=380, height=480))

                # Mostrar la gráfica en la segunda columna
                with col2:
                    st.plotly_chart(fc.graficar.graficar_linea(df_IE004, 'Fecha','Inflación Anual', 'Inflación Anual Histórica','Inflación Anual (%)', width=380, height=480))

            with tabs[1]:
                    st.title("Evolución del Tipo de Cambio (USD/MXN)")
                    # Cargar datos de Yahoo Finance
                    
                    with st.form("form_exchange"):
                        period = st.selectbox("Periodo de información", ("5Y", "1Y", "YTD", "7mo", "5mo", "1mo"))
                        df_IE007 = fc.graficar.cargar_datos_yfinance('USDMXN=X', period)
                        df_IE007['Variacion'] = (df_IE007['Close']/df_IE007['Close'].shift()-1)*100
                        submitted = st.form_submit_button("Consultar")
                
                        if submitted:
                    
                            if df_IE007 is not None:
                            # Dividir la página en dos columnas
                                col1, col2 = st.columns([1, 1])

                            # Mostrar el DataFrame en la primera columna
                            with col1:
                                fig_ie007 = px.line(df_IE007,
                                                    x=df_IE007.index,
                                                    y = ['Close'],
                                                    title = "Evolución histórica del tipo de cambio"
                                                    )
                                
                                fig_ie007.update_layout(
                                        height = 380,
                                        width=280,
                                        showlegend = False,
                                        title_font=dict(
                                            color="#027034",
                                            size=14
                                            )
                                        )
                                
                                fig_ie007.update_yaxes(title_text="MXP / USD")
                                fig_ie007.update_xaxes(title="Fecha")
                                
                                st.plotly_chart(fig_ie007)
                                
                            # Mostrar la gráfica en la segunda columna
                            with col2:
                                fig_ie007_bis = px.line(df_IE007,
                                                        x=df_IE007.index,
                                                        y = ["Variacion"],
                                                        title = "Variación del tipo de cambio (%)"
                                                        )
                                fig_ie007_bis.update_layout(
                                        height = 380,
                                        width=280,
                                        showlegend = False,
                                        title_font=dict(
                                            color="#027034",
                                            size=14
                                            )
                                        )
                                
                                fig_ie007_bis.update_yaxes(title_text="Variación (%)")
                                fig_ie007_bis.update_xaxes(title="Fecha")

                                st.plotly_chart(fig_ie007_bis)

            with tabs[2]:
                    st.title("Tasa Referencia: Banco de México")
                    # Cargar datos de tasa objetivo de Banxico
                    df_IE001 = fc.graficar.cargar_datos_gsheets_economics('IE_001', [0, 1])
                    if df_IE001 is not None:
                        df_IE001 = pd.DataFrame(df_IE001)
                        st.plotly_chart(fc.graficar.graficar_linea(df_IE001, 'Fecha', 'TasaReferencia', 'Tasa de Referencia BANXICO', 'Tasa de Referencia BANXICO (%)', width=680, height=480))  

            with tabs[3]:
                st.title("Producto Interno Bruto")
                df_IE006 = fc.graficar.cargar_datos_gsheets_economics('IE_006', [2,4])
                if df_IE006 is not None:
                    df_IE006 = pd.DataFrame(df_IE006)
                    fig_df_IE006 = px.bar(df_IE006, x="Periodo", y = "PIB (%)")
                    st.plotly_chart(fig_df_IE006)


    elif menu_options == "Banca":
        st.title(f"Sección actual: {menu_options}")
        tabs001 = st.tabs([":books: Indicadores Financieros", ":clipboard: Captación(Saldo de Cuentas de Ahorro)", ":credit_card: Colocación (Saldo de Cartera de Créditos)"])        
        
        with tabs001[0]:
            df_C001 = fc.graficar.cargar_datos_gsheets_banca('C_001')
            
            with st.form("form_banca"):
                lista_banca = st.selectbox('Tipo de información', ("Activo Total", "Capital Contable", "Resultado Neto"))

                if lista_banca == 'Activo Total':                      
                    fig_df_c001 = fc.graficar.graficar_linea(df_C001, 'Fecha', 'Activo',  f'Evolución Histórica: <br>{lista_banca}',"Activo Total (mdp)", width=310, height=380)
                    df_C001['Dif_Activo'] = (df_C001['Activo']/df_C001['Activo'].shift(12)-1)*100
                    fig_df_c001_bis = fc.graficar.graficar_linea_bis(df_C001, 'Fecha', 'Dif_Activo', f'Variación anual <br>{lista_banca}',"", "Variación Anual (%)", width=310, height=380)

                elif lista_banca == 'Capital Contable':
                    fig_df_c001 = fc.graficar.graficar_linea(df_C001, 'Fecha', 'Capital', f'Evolución Histórica <br>{lista_banca}','Capital Contable (mdp)', width=310, height=380)
                    df_C001['Dif_Capital'] = (df_C001['Capital']/df_C001['Capital'].shift(12)-1)*100
                    fig_df_c001_bis = fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Capital', f'Varación anual <br>{lista_banca}','Variación Anual (%)', width=310, height=380)           
                        
                elif lista_banca == 'Resultado Neto':
                    fig_df_c001 = fc.graficar.graficar_linea(df_C001, 'Fecha', 'Resultado',  f'{"Evolución histórica:"}<br>{lista_banca}','Resultado Neto (mdp)', width=310, height=380)
                    df_C001['Dif_Resultado'] = (df_C001['Resultado']/df_C001['Resultado'].shift(12)-1)*100
                    fig_df_c001_bis = fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Resultado', f'Variación anual <br>{lista_banca}', "Variación Anual (%)",width=310, height=380)           

                submitted = st.form_submit_button("Consultar")
                
                if submitted:

                    col1, col2 = st.columns([1,1], gap='medium')
                    with col1:
                        st.plotly_chart(fig_df_c001)

                    with col2:
                        st.plotly_chart(fig_df_c001_bis)
        
        with tabs001[1]:
            
            with st.form("form_captacion"):
                lista_captacion = st.selectbox('Tipo de información', ('Captación Total','Depósitos de exigencia inmediata',  'Depósitos a plazo', 'Cuenta global de captación sin movimientos'))
                #st.write(f'Cifras de la banca: {lista_captacion}')

                submit_2 = st.form_submit_button("Consultar")
                if submit_2:
                    
                    if lista_captacion == 'Captación Total':
                        df_C001['Dif_Capt'] = (df_C001['Captacion']/df_C001['Captacion'].shift(12)-1)*100
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Captacion',  f'Evolución Histórica: <br>{lista_captacion}',"Saldo (mdp)", width=310, height=380))

                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Capt',  f'Variación anual: <br>{lista_captacion}',"Variación Anual (%)", width=310, height=380))

                    elif lista_captacion == 'Depósitos de exigencia inmediata':
                        df_C001['Dif_Depositos'] = (df_C001['Depositos']/df_C001['Depositos'].shift(12)-1)*100
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Depositos',  f'Evolución Histórica: <br>{lista_captacion}', "Saldo (mdp)", width=310, height=380))
                            
                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Depositos',  f'Variación anual: <br>{lista_captacion}', "Variación Anual (%)", width=310, height=380))                        
                    
                    elif lista_captacion == 'Depósitos a plazo':
                        df_C001['Dif_Plazo'] = (df_C001['Plazo']/df_C001['Plazo'].shift(12)-1)*100
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Plazo',  f'Evolución Histórica: <br>{lista_captacion}', "Saldo (mdp)", width=310, height=380))
                            
                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Plazo',  f'Variación anual: <br>{lista_captacion}',"Variación Anual (%)", width=310, height=380))

                    elif lista_captacion == 'Cuenta global de captación sin movimientos':
                        df_C001['Dif_CGC'] = (df_C001['CGC']/df_C001['CGC'].shift(12)-1)*100
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'CGC', f'Evolución Histórica: <br>{lista_captacion}', "Saldo (mdp)", width=310, height=380))
                            
                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_CGC',  f'Variación anual: <br>{lista_captacion}',"Variación Anual (%)", width=310, height=380))

        with tabs001[2]:
                        
            with st.form("form_cartera"):

                lista_cartera = st.selectbox('Tipo de información', ('Cartera de Crédito Total','Cartera Créditos de Consumo',  'Cartera Créditos Empresariales', 'Cartera de Tarjeta de Crédito', 'Cartera Créditos de Nomina', 'Cartera Créditos Personales',  'Cartera Créditos de Vivienda','Cartera Crédito Automotriz')) 
                #st.write(f'Cifras de la banca: {lista_cartera}')
                
                #Calcular variaciones anuales
                df_C001['Dif_C_total'] = (df_C001['Total']/df_C001['Total'].shift(12)-1)*100
                df_C001['Dif_Consumo'] = (df_C001['Consumo']/df_C001['Consumo'].shift(12)-1)*100
                df_C001['Dif_Empresas'] = (df_C001['Empresas']/df_C001['Empresas'].shift(12)-1)*100
                df_C001['Dif_TC'] = (df_C001['TC']/df_C001['TC'].shift(12)-1)*100
                df_C001['Dif_Nomina'] = (df_C001['Nomina']/df_C001['Nomina'].shift(12)-1)*100
                df_C001['Dif_Personales'] = (df_C001['Personales']/df_C001['Personales'].shift(12)-1)*100
                df_C001['Dif_Vivienda'] = (df_C001['Vivienda']/df_C001['Vivienda'].shift(12)-1)*100
                df_C001['Dif_Automotriz'] = (df_C001['Automotriz']/df_C001['Automotriz'].shift(12)-1)*100

                submit = st.form_submit_button("Consultar")
                if submit:
                    
                    if lista_cartera == 'Cartera de Crédito Total':
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Total',  f'Evolución Histórica: <br>{lista_cartera}','Saldo (mdp)', width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Total_IMOR', f'IMOR: {lista_cartera}', "Índice de Morosidad (%)", width=310, height=380))

                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_C_total',  f'Variación anual: <br>{lista_cartera}', "Variación Anual (%)", width=310, height=380))                        
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Total_PE', f'Pérdida esperada: <br>{lista_cartera}', "PE (%)",  width=310, height=380))

                    elif lista_cartera == 'Cartera Créditos de Consumo':
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Consumo',  f'Evolución Histórica: <br>{lista_cartera}',"Saldo (mdp)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Consumo_IMOR', f'IMOR: {lista_cartera}', "Índice de Morosidad (%)",  width=310, height=380))
                            
                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Consumo',  f'Variación anual: <br>{lista_cartera}', "Variación Anual (%)", width=310, height=380))                        
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Consumo_PE', f'Pérdida esperada: <br>{lista_cartera}',"PE (%)", width=310, height=380))

                    elif lista_cartera == 'Cartera Créditos Empresariales':
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Empresas',  f'Evolución Histórica <br>{lista_cartera}',"Saldo (mdp)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Empresas_IMOR', f'IMOR: {lista_cartera}', "Índice de Morosidad (%)", width=310, height=380))

                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Empresas',  f'Variación anual: <br>{lista_cartera}', "Variación Anual (%)", width=310, height=380))             
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Empresas_PE', f'Pérdidad Esperada: <br>{lista_cartera}', "PE (%)", width=310, height=380))

                    elif lista_cartera == 'Cartera de Tarjeta de Crédito':

                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'TC',  f'Evolución Histórica: <br>{lista_cartera}', "Saldo (mdp)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'TC_IMOR', f'IMOR: {lista_cartera}', "Índice de Morosidad (%)", width=310, height=380))

                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_TC',  f'Variación anual: <br>{lista_cartera}', "Variación Anual (%)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'TC_PE', f'Pérdida esperada: <br>{lista_cartera}', "PE (%)", width=310, height=380))

                    elif lista_cartera == 'Cartera Créditos de Nomina':

                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Nomina',  f'Evolución Histórica: <br>{lista_cartera}', "Saldo (mdp)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Nomina_IMOR', f'IMOR: {lista_cartera}', "Índice de Morosidad (%)", width=310, height=380))

                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Nomina',  f'Varición anual: <br>{lista_cartera}', "Variación Anual (%)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Nomina_PE', f'Pérdida esperada: <br>{lista_cartera}', "PE (%)", width=310, height=380))

                    elif lista_cartera == 'Cartera Créditos Personales':

                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Personales',  f'Evolución Histórica: <br>{lista_cartera}', "Saldo (mdp)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Personales_IMOR', f'IMOR: {lista_cartera}', "Índice de Morosidad (%)", width=310, height=380))
                        
                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Personales',  f'Variación anual: <br>{lista_cartera}', "Variación Anual (%)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Personales_PE', f'Pérdida esperada: <br>{lista_cartera}', "PE (%)", width=310, height=380))

                    elif lista_cartera == 'Cartera Créditos de Vivienda':

                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Vivienda',  f'Evolución Histórica: <br>{lista_cartera}', "Saldo (mdp)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Vivienda_IMOR', f'IMOR: {lista_cartera}', "Índice de Morosidad (%)", width=310, height=380))
                        
                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Vivienda',  f'Variación anual: <br>{lista_cartera}', "Variación Anual (%)", width=310, height=380)) 
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Vivienda_PE', f'Pérdida esperada: <br>{lista_cartera}', "PE (%)", width=310, height=380))
                            
                    elif lista_cartera == 'Cartera Crédito Automotriz':
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Automotriz',  f'Evolución Histórica: <br>{lista_cartera}', "Saldo (mdp)", width=310, height=380))
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Automotriz_IMOR', f'IMOR: {lista_cartera}', "Índice de Morosidad (%)", width=310, height=380))
                        with col2:
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Dif_Automotriz',  f'Variación anual: <br>{lista_cartera}', "Variación Anual (%)", width=310, height=380)) 
                            st.plotly_chart(fc.graficar.graficar_linea(df_C001, 'Fecha', 'Automotriz_PE', f'Pérdida esperada: <br>{lista_cartera}',  "PE (%)", width=310, height=380))

    elif menu_options == "Vivienda":
        st.title(f"Sección actual: {menu_options}")
        
        tabs002 = st.tabs([':house_buildings:Índice precios a la vivienda (SHF)',':chart: Tasa de interés Créditos a la Vivienda']) 
        
        with tabs002[0]:
            st.write("Índice de precios a la vivienda (SHF)")
         
            with st.form("form_SHF"):
                df_IE005 = fc.graficar.cargar_datos_gsheets_economics('IE_005', [1, 6, 7])
                lista = df_IE005['Global'].dropna().unique()
                value= st.selectbox('Tipo de información', lista) 
                df_IE005_bis = df_IE005[df_IE005['Global']==value]  
                df_IE005_bis['Diferencia'] = (df_IE005_bis['Indice']/df_IE005_bis['Indice'].shift(4)-1)*100
                df_nacional = df_IE005[df_IE005['Global']=="Nacional"]
                st.write("Información del Índice de Precios a la vivienda SHF")
                
                fig_df_ie005 = fc.graficar.graficar_linea_bis(df_IE005_bis, 'Trimestre', 'Indice',  f'Evolución del Índice SHF <br>{value}', width=310, height=380)
        
                fig_df_ie005_bis = fc.graficar.graficar_linea(df_IE005_bis, 'Trimestre', 'Diferencia',  f'Variación Anual: <br>{value}', "Variación Anual (%)", width=310, height=380)
                
                submitted = st.form_submit_button("Consultar")
                
                if submitted:
        
                    col1, col2 = st.columns([1,1], gap='medium')

                    with col1:
                        st.plotly_chart(fig_df_ie005_bis)

                # Mostrar la gráfica en la segunda columna
                    with col2:
                        st.plotly_chart(fig_df_ie005)

        with tabs002[1]:
            st.write('Tasa de interés créditos a la vivienda')

            df_IEO03 = fc.graficar.cargar_datos_gsheets_economics('IE_003',[0, 4, 5, 6] )

            def graficar_lineas(df, x_col, y_cols, titles):
                fig = go.Figure()
    
                for y_col, title in zip(y_cols, titles):
                    fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines', name=title))
                
                fig.update_layout(xaxis_title=x_col, yaxis_title="Tasa de interés (%)")
                
                return fig

            y_cols = []
            titles = []

            if st.checkbox("Tasa de interés mínima de créditos en pesos a tasa fija"):
                # Si el checkbox está seleccionado, agrega 'Variable1' a la lista de variables seleccionadas
                y_cols.append('SF43424')
                titles.append('Tasa de interés mínima')  # Cambia 'Variable1' por el título adecuado
    
            if st.checkbox("Tasa de interés máxima de créditos en pesos a tasa fija"):
                # Si el checkbox está seleccionado, agrega 'Variable2' a la lista de variables seleccionadas
                y_cols.append('SF43425')
                titles.append('Tasa de interés máxima')  # Cambia 'Variable2' por el título adecuado
    
            if st.checkbox("Tasa de interés promedio de créditos en pesos a tasa fija"):
                # Si el checkbox está seleccionado, agrega 'Variable3' a la lista de variables seleccionadas
                y_cols.append('SF43426')
                titles.append('Tasa de interés promedio')  # Cambia 'Variable3' por el título adecuado

            if y_cols:  # Verifica si se seleccionaron variables para mostrar
                fig = graficar_lineas(df_IEO03, 'Fecha', y_cols, titles)
                st.plotly_chart(fig)
            else:
                st.warning("Por favor, selecciona al menos una variable para mostrar.")

    elif menu_options == "Referencias":
        st.title(f"Sección actual: {menu_options}")

        with st.expander(":green[INEGI]"):
            #st.text("Inflación INEGI")
            st.markdown("### Notas")
            st.markdown("""
                        
                        Portal Web del Instituto Nacional de Estadística y Geografía [INEGI](https://www.inegi.org.mx/) 
                        
                        ---
                        """)
            
        with st.expander(":green[Banxico]"):
            st.markdown("### Notas")
            st.markdown("""
                        
                        Portal Web de Banco de México [BANXICO](https://www.banxico.org.mx/) 
                        
                        ---
                        """
                        )
        
        with st.expander(":green[CNBV]"):
            st.markdown("### Notas")
            st.markdown("""
                        
                        Portal Web de la Comisión Nacional Bancaria y de Valores [CNBV](https://www.gob.mx/cnbv) 
                        
                        ---
                        <p> 1/ Para la cartera total se considera la información de cartera de los
                        bancos junto con la cartera de sus respectivas Sociedades Financieras de 
                        Objeto Múltiple Reguladas a las que consolidan.</p>
                        
                        - **Hasta diciembre 2021**: **_Cartera total_** = Cartera vigente + cartera vencida. </p>
                        - **A partir de enero 2022**: **_Cartera total_** = Cartera de crédito con riesgo de crédito en etapa 1 + 2 + 3 + cartera de crédito valuada a valor razonable. </p>
                        ---

                        2/ Respecto al ***resultado neto*** se muestran saldos acumulados al cierre de mes.
                        
                        ---
                        
                        3/ Hasta diciembre 2021:  **_IMOR = Índice de Morosidad_** = cartera vencida / (Cartera vigente + cartera vencida).

                        - **A partir de enero 2022**: **_IMOR = Índice de Morosidad_** = cartera de crédito con riesgo de crédito en etapa 3 / (Cartera de crédito con riesgo de crédito en etapa 1 + 2 + 3).


                        """, unsafe_allow_html=True)

        with st.expander(":green[SHF]"):
            st.markdown("### Notas")
            st.markdown("""                    
                        Portal Web de Sociedad Hipotecaria Federal [SHF](https://www.gob.mx/shf) 
                        ---
                        """)

if __name__ == "__main__":
    main()

#theme
#hide_st_style= """

#<style>
#MainMenu{visibility:hidden;}
#footer{visibility:hidden;}
#header{visibility:hidden;}
#</style>
#"""