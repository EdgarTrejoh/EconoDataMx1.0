import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
from Functions import functions, charts
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
    IPC = "^MXX"
    TC = "USDMXN=X"
    col_1, col_2 = st.columns(2)

    with col_1:
        st.image('EconoData.jpg', width=110)
    
    with col_2:
        st.title(':grey[ECONODATA-MX]')
        st.markdown("""
                    [![Twitter](https://img.shields.io/badge/Twitter-@EconoDataMx-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white&labelColor=101010)](https://x.com/EconoDataMx)
                    """)

    # Option Menu
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
        
        #Obtener información del tipo de cambio 
        tipo_cambio_ultimo, tipo_cambio_previo, tc_fecha, resumen_tipo_cambio = functions.obtener_tipo_cambio(TC, periodo)
        
        #Obtener información del INPC
        inflacion_ultimo, inflacion_previo, inflacion_fecha, inflacion_resumen = functions.obtener_inflacion()
        
        #Obtener información de la tasa de referencia Banxico
        tasa_referencia_ultima, tasa_referencia_previa, tasa_referencia_fecha, resumen_tasa_referencia = functions.obtener_tasa_referencia()
        
        #Obtener información del PIB
        pib_ultimo, pib_fecha, resumen_pib = functions.obtener_pib()

        st.subheader("Principales índices")
        
        indicador1, indicador2, indicador3, indicador4 =st.columns(4, gap='medium')
        
        with indicador1:
            st.info(':blue[Tipo de Cambio]', icon= "📌")
            st.metric("USD/MPX", f"${tipo_cambio_ultimo:,.2f}", delta =f"{(tipo_cambio_ultimo - tipo_cambio_previo)/tipo_cambio_previo:.2%}", delta_color='inverse')
            st.text(f"Corte: {tc_fecha}")
        
        with indicador2:
            st.info(':blue[Tasa Referencia]', icon="📌")
            st.metric("Banxico", f"{tasa_referencia_ultima:,.2f} %", delta = f"{(tasa_referencia_ultima - tasa_referencia_previa)/tasa_referencia_previa:.2%}")
            st.text(f'Corte: {tasa_referencia_fecha}')
    
        with indicador3:
            st.info(':blue[Inflación Anual]',icon="📌")
            st.metric("INEGI", f"{inflacion_ultimo:,.2f} %", delta = f"{(inflacion_ultimo - inflacion_previo)/inflacion_previo:.2%}", delta_color='inverse')
            st.text(f"Corte: {inflacion_fecha}")
    
        with indicador4:
            st.info(':blue[Variacion Anual PIB]',icon= "📌")
            st.metric(label="INEGI", value=f"{pib_ultimo:,.2f} %")
            st.text(f'Trimestre: {pib_fecha}')
    
    with st.sidebar:
        st.warning("Para tener acceso a las secciones primero debes registrarte con tu cuenta de Google y pagar tu suscripción por única ocasión")
        add_auth(required=True)
        st.success("Ya puedes ingresar a todas las secciones")
        st.write(st.session_state.email)
    
        st.write(st.session_state.user_subscribed)

    if menu_options == "Indicadores":
        st.title(f"Sección actual: {menu_options}")

        # Cargar datos de GSheets
        df_IE004 = functions.cargar_datos_gsheets_economics('IE_004', [0, 1, 2])
        if df_IE004 is not None:
            df_IE004 = pd.DataFrame(df_IE004)
        
            # Crear las pestañas y la división de la página 
            tabs = st.tabs([
                ":chart_with_upwards_trend: Inflacion", 
                ":heavy_dollar_sign: Tipo de Cambio", 
                ":classical_building: Tasa de Referencia", 
                ":building_construction: PIB",
                ":chart: IPC"
                            ])
            
            with tabs[0]:  # Pestaña de Inflacion

                with st.form("form_indicador_inflacion"):

                    st.text("Selecciona el periodo de informaciòn que quieres consultar:")
                    start_Date = st.date_input("Fecha de inicio", datetime.date(2008, 1, 21), datetime.date(2008, 1, 21),datetime.date(2024, 9, 9),"start")
                    end_Date = st.date_input("Fecha de fin", datetime.date(2008, 1, 21), datetime.date(2008, 1, 21),datetime.date(2024, 9, 9), "end")

                    start_Date = pd.to_datetime(start_Date)
                    end_Date = pd.to_datetime(end_Date)    
                    df_IE004 = functions.filtrar_por_fechas(df_IE004, start_Date, end_Date)

                    submitted = st.form_submit_button("Consultar")
                
                    if submitted:

                        st.plotly_chart(charts.create_chart(df_IE004,'Fecha', 'Inflación Anual', 'Inflación Anual Histórica - Mx', 'Fecha', 'Inflación Anial (%)', '#0f52EA', '#0f52ea', 18, 600, 380, 3))

                        st.markdown("""
                                Fuente: INEGI. 
                                
                                Índice Nacional de Precios al Consumidor (INPC).
                                
                                """)
            
            with tabs[1]:
                    st.title("Evolución del Tipo de Cambio (USD/MXN)")
                    
                    # Cargar datos de Yahoo Finance
                    with st.form("form_exchange"):
                        period = st.selectbox("Periodo de información", ("5Y", "1Y", "YTD", "7mo", "5mo", "1mo"))
                        df_IE007 = functions.cargar_datos_yfinance('USDMXN=X', period)
                        df_IE007['Variacion'] = (df_IE007['Close']/df_IE007['Close'].shift()-1)*100
                        submitted = st.form_submit_button("Consultar")
                
                        if submitted:
                            if df_IE007 is not None:
                            # Dividir la página en dos columnas
                                col1, col2 = st.columns([1, 1])

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
                                            color="#131212",
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
                                                        title = "Variación del tipo de cambio (% vs. día anterior)"
                                                        )
                                    fig_ie007_bis.update_layout(
                                        height = 380,
                                        width=280,
                                        showlegend = False,
                                        title_font=dict(
                                            color="#131212",
                                            size=14
                                            )
                                        )
                                
                                    fig_ie007_bis.update_yaxes(title_text="Variación (%)")
                                    fig_ie007_bis.update_xaxes(title="Fecha")

                                    st.plotly_chart(fig_ie007_bis)

                            st.markdown ("[Fuente: Yahoo Finance](https://finance.yahoo.com/)")

            with tabs[2]:
                    st.title("Tasa Referencia: Banco de México")
                    # Cargar datos de tasa objetivo de Banxico
                    df_IE001 = functions.cargar_datos_gsheets_economics('IE_001', [0, 1])
                    if df_IE001 is not None:
                        df_IE001 = pd.DataFrame(df_IE001)
                        st.plotly_chart(charts.graficar_linea_bis(df_IE001, 'Fecha', 'TasaReferencia', 'Tasa de Referencia BANXICO', 'Tasa de Referencia BANXICO (%)', '#1882eb', '#0F0F0F', width=680, height=480))  
                        st.markdown("""
                            Fuente: Banco de México.                            
                            """)

            with tabs[3]:
                st.title("Producto Interno Bruto")
                df_IE006 = functions.cargar_datos_gsheets_economics('IE_006', [2,4])
                if df_IE006 is not None:
                    df_IE006 = pd.DataFrame(df_IE006)
                    fig_dfIE006 = px.bar(df_IE006, x="Periodo", y = "PIB (%)")
                    fig_dfIE006.update_layout(title="PIB Trimestral - Variación Anual")
                    st.plotly_chart(fig_dfIE006)
                    st.markdown("""
                            Fuente: INEGI.                            
                            """)

            with tabs[4]:
                st.title("Evolución del IPC (IPC-MX)")
                    
                # Cargar datos de Yahoo Finance
                with st.form("form_IPC"):
                    period = st.selectbox("Periodo de información", ("5Y", "1Y", "YTD", "7mo", "5mo", "1mo"))
                    df_IE003 = functions.cargar_datos_yfinance(IPC, period)
                    df_IE003['Variacion'] = (df_IE003['Close']/df_IE003['Close'].shift()-1)*100
                    submitted = st.form_submit_button("Consultar")
            
                    if submitted:
                
                        if df_IE003 is not None:
                        # Dividir la página en dos columnas
                            col1, col2 = st.columns([1, 1])

                            with col1:
                                fig_ie003 = px.line(df_IE003,
                                                x=df_IE003.index,
                                                y = ['Close'],
                                                title = "Evolución histórica del IPC"
                                                )
                            
                                fig_ie003.update_layout(
                                        height = 380,
                                        width=280,
                                        showlegend = False,
                                        title_font=dict(
                                            color="#131212",
                                            size=14
                                            )
                                        )
                                
                                fig_ie003.update_yaxes(title_text="unidades")
                                fig_ie003.update_xaxes(title="Fecha")
                                
                                st.plotly_chart(fig_ie003)
                                
                            # Mostrar la gráfica en la segunda columna
                            with col2:
                                fig_ie003_bis = px.line(df_IE003,
                                                        x=df_IE003.index,
                                                        y = ["Variacion"],
                                                        title = "Variación histórica del IPC -Mx (% vs. día anterior)"
                                                        )
                                fig_ie003_bis.update_layout(
                                    height = 380,
                                    width=280,
                                    showlegend = False,
                                    title_font=dict(
                                        color="#131212",
                                        size=14
                                        )
                                    )
                                
                                fig_ie003_bis.update_yaxes(title_text="Variación (%)")
                                fig_ie003_bis.update_xaxes(title="Fecha")

                                st.plotly_chart(fig_ie003_bis)

                            st.markdown ("[Fuente: Yahoo Finance](https://finance.yahoo.com/)")

    elif menu_options == "Banca":
        st.title(f"Sección actual: {menu_options}")
        tabs001 = st.tabs([":books: Indicadores Financieros", ":clipboard: Captación(Saldo de Cuentas de Ahorro)", ":credit_card: Colocación (Saldo de Cartera de Créditos)"])        

        with tabs001[0]:
            df_IE002 = functions.cargar_datos_gsheets_economics('IE_002')
            
            with st.form("form_banca"):
                lista_banca = st.selectbox('Tipo de información', ("Activo Total", "Capital Contable", "Resultado Neto"))

                metric_mapping = {
                    'Activo Total': {'col': 'Activo-SIS', 'label': 'Activo Total (mdp)', 'var_label': 'Dif_Activo'},
                    'Capital Contable': {'col': 'Capital-SIS', 'label': 'Capital Contable (mdp)', 'var_label': 'Dif_Capital'},
                    'Resultado Neto': {'col': 'Resultado-SIS', 'label': 'Resultado Neto (mdp)', 'var_label': 'Dif_Resultado'},
                }

                selected_metric = metric_mapping[lista_banca]

                fig_df_IE002 = charts.graficar_linea_bis(
                    df_IE002, 'Fecha', selected_metric['col'],  
                    f'Evolución Histórica: <br>{lista_banca}', 
                    'Fecha', selected_metric['label'], 
                    '#131212', '#444445', width=310, height=380
                )

                # Cálculo de la variación anual
                df_IE002[selected_metric['var_label']] = (df_IE002[selected_metric['col']] / df_IE002[selected_metric['col']].shift(12) - 1) * 100
    
                # Generación de la gráfica de variación anual
                fig_df_IE002_bis = charts.create_chart(
                    df_IE002, 'Fecha', selected_metric['var_label'], 
                    f'Variación anual <br>{lista_banca}', 
                    'Fecha', "Variación Anual (%)", 
                    '#0f52EA', '#444445', 18, 310, 380, 1.5
                )
            
                submitted = st.form_submit_button("Consultar")
                
                if submitted:
                    col1, col2 = st.columns(2, gap='medium')
                    with col1:
                        st.plotly_chart(fig_df_IE002)

                    with col2:
                        st.plotly_chart(fig_df_IE002_bis)
        
                    st.markdown("""
                            Fuente: Comisión Nacional Bancaria y de Valores.                            
                            """)

        with tabs001[1]:

            with st.form("form_captacion"):

                lista_captacion = st.selectbox('Tipo de información', (
                    'Captación Total',
                    'Depósitos de exigencia inmediata',  
                    'Depósitos a plazo', 
                    'Cuenta global de captación sin movimientos'
                ))

                submit_2 = st.form_submit_button("Consultar")
                
                if submit_2:
                
                    captacion_map = {
                        'Captación Total': ('Captacion-SIS', 'Dif_Capt'),
                        'Depósitos de exigencia inmediata': ('DepExigInm-SIS', 'Dif_Depositos'),
                        'Depósitos a plazo': ('DepPlazo-SIS', 'Dif_Plazo'),
                        'Cuenta global de captación sin movimientos': ('CtaGlobal-SIS', 'Dif_CGC')
                    }
                
                    col_data, dif_col = captacion_map[lista_captacion]
                    df_IE002[dif_col] = (df_IE002[col_data] / df_IE002[col_data].shift(12) - 1) * 100
                    col1, col2 = st.columns([1, 1], gap='medium')

                    with col1:
                        st.plotly_chart(charts.graficar_linea_bis(
                            df_IE002, 'Fecha', col_data,
                            f'Evolución Histórica: <br>{lista_captacion}',
                            'Fecha', "Saldo (mdp)",
                            '#131212', '#444445', width=310, height=380)
                        )

                    with col2:
                        st.plotly_chart(charts.create_chart(
                            df_IE002, 'Fecha', dif_col,
                            f'Variación anual <br>{lista_captacion}',
                            'Fecha', "Variación Anual (%)",
                            '#0f52EA', '#444445', 18, 310, 380, 1.5)
                        )

                st.markdown("Fuente: Comisión Nacional Bancaria y de Valores.")

        with tabs001[2]:
                        
            with st.form("form_cartera"):
                lista_cartera = st.selectbox('Tipo de información', (
                    'Cartera de Crédito Total',
                    'Cartera Créditos de Consumo',  
                    'Cartera Créditos Empresariales', 
                    'Cartera de Tarjeta de Crédito', 
                    'Cartera Créditos de Nómina', 
                    'Cartera Créditos Personales',  
                    'Cartera Créditos de Vivienda',
                    'Cartera Crédito Automotríz'
                )) 
                
                submit = st.form_submit_button("Consultar")
                if submit:
                        columnas = {
                            'CCT_Saldo-SIS': 'Dif_C_total',
                            'CCCT_Saldo-SIS': 'Dif_Consumo',
                            'CCE_Saldo-SIS': 'Dif_Empresas',
                            'CCCTC_Saldo-SIS': 'Dif_TC',
                            'CCCN_Saldo-SIS': 'Dif_Nomina',
                            'CCCP_Saldo-SIS': 'Dif_Personales',
                            'CCV_Saldo-SIS': 'Dif_Vivienda',
                            'CCCA_Saldo-SIS': 'Dif_Automotriz'
                        }

                        for original, nueva in columnas.items():
                            df_IE002[nueva] = (df_IE002[original] / df_IE002[original].shift(12) - 1) * 100    

                        cartera_map = {
                            'Cartera de Crédito Total': ('CCT_Saldo-SIS', 'CCT_IMOR-SIS','CCT_PE-SIS','Dif_C_total'),
                            'Cartera Créditos de Consumo': ('CCCT_Saldo-SIS', 'CCCT_IMOR-SIS','CCCT_PE-SIS','Dif_Consumo'),
                            'Cartera Créditos Empresariales': ('CCE_Saldo-SIS', 'CCE_IMOR-SIS','CCE_PE-SIS','Dif_Empresas'),
                            'Cartera de Tarjeta de Crédito': ('CCCTC_Saldo-SIS', 'CCCTC_IMOR-SIS','CCCTC_PE-SIS','Dif_TC'),
                            'Cartera Créditos de Nómina': ('CCCN_Saldo-SIS', 'CCCN_IMOR-SIS','CCCN_PE-SIS','Dif_Nomina'),
                            'Cartera Créditos Personales': ('CCCP_Saldo-SIS', 'CCCP_IMOR-SIS','CCCP_PE-SIS','Dif_Personales'),
                            'Cartera Créditos de Vivienda': ('CCV_Saldo-SIS', 'CCV_IMOR-SIS','CCV_PE-SIS','Dif_Vivienda'),
                            'Cartera Crédito Automotríz': ('CCCA_Saldo-SIS', 'CCCA_IMOR-SIS','CCCA_PE-SIS','Dif_Automotriz')
                        }

                        saldo, imor, pe, dif = cartera_map[lista_cartera] 
                        col1, col2 = st.columns([1,1], gap='medium')
                            
                        with col1:
                            st.plotly_chart(charts.graficar_linea_bis(
                                  df_IE002, 'Fecha', saldo,  
                                  f'Evolución Histórica: <br>{lista_cartera}', 'Fecha', 
                                  'Saldo (mdp)', '#131212', '#444445', width=310, height=380))
                            
                            st.plotly_chart(charts.create_chart(
                                  df_IE002, 'Fecha', imor, 
                                  f'IMOR: {lista_cartera}', 
                                  'Fecha', "Índice de Morosidad (%)", 
                                  '#0f52EA', '#444445', 18, 310, 380, 2.5))

                        with col2:
                            st.plotly_chart(charts.create_chart(
                                    df_IE002, 'Fecha', dif,
                                    f'Variación anual <br>{lista_cartera}',
                                    'Fecha', "Variación Anual (%)",
                                    '#0f52EA', '#444445', 18, 310, 380, 2.5)
                                )

                            st.plotly_chart(charts.graficar_linea_bis(df_IE002, 'Fecha', 
                                    pe, f'Pérdida esperada: <br>{lista_cartera}', 'Fecha', 
                                    "PE (%)", '#131212', '#444445', width=310, height=380))


                st.markdown("""
                            Fuente: Comisión Nacional Bancaria y de Valores.                            
                            """)

    elif menu_options == "Vivienda":
        st.title(f"Sección actual: {menu_options}")
        
        tabs002 = st.tabs([':house_buildings:Índice precios a la vivienda (SHF)',':chart: Tasa de interés Créditos a la Vivienda']) 
        
        with tabs002[0]:
            st.write("Índice de precios a la vivienda (SHF)")
         
            with st.form("form_SHF"):
                df_IE005 = functions.cargar_datos_gsheets_economics('IE_005', [1, 6, 7])
                lista = df_IE005['Global'].dropna().unique()
                value= st.selectbox('Tipo de información', lista) 
                df_IE005_bis = df_IE005[df_IE005['Global']==value]  
                df_IE005_bis['Diferencia'] = (df_IE005_bis['Indice']/df_IE005_bis['Indice'].shift(4)-1)*100
                df_nacional = df_IE005[df_IE005['Global']=="Nacional"]
                st.write("Información del Índice de Precios a la vivienda SHF")
                
                fig_df_ie005_val = charts.graficar_linea_bis(
                    df_IE005_bis, 'Trimestre', 'Indice',  
                    f'Evolución del Índice SHF <br>{value}', 
                    'Periodo', 'Valor índice', '#131212', '#444445',
                    width=310, height=380)

                fig_df_ie005_var = charts.create_chart(
                    df_IE005_bis, 'Trimestre', 'Diferencia',  
                    f'Variación Anual: Índice SHF <br>{value}',
                    'Periodo', "Variación Anual (%)", 
                    '#0f52EA', '#444445', 18, 310, 380, 1.5)

                submitted = st.form_submit_button("Consultar")
                
                if submitted:
        
                    col1, col2 = st.columns([1,1], gap='medium')

                    with col1:
                        st.plotly_chart(fig_df_ie005_val)

                # Mostrar la gráfica en la segunda columna
                    with col2:
                        st.plotly_chart(fig_df_ie005_var)

                    st.text("Fuete: SHF, Índice SHF de Precios a la Vivienda en México")

        with tabs002[1]:
            st.write('Tasa de interés créditos a la vivienda')

            df_IEO03 = functions.cargar_datos_gsheets_economics('IE_003',[0, 4, 5, 6] )

            def graficar_lineas(df, x_col, y_cols, titles, main_title, line_width = 2):
                fig = go.Figure()
    
                for y_col, title in zip(y_cols, titles):
                    fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines', 
                                name=title,  line=dict(width=line_width)))
                
                fig.update_layout(
                    title = main_title,
                    xaxis_title=x_col, 
                    yaxis_title="Tasa de interés (%)")
                
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
                fig = graficar_lineas(df_IEO03, 'Fecha', y_cols, titles, 'Tasa de interes de créditos a los Hogares - Mx.', line_width = 2.8)
                st.plotly_chart(fig)
                st.markdown("""
                Fuente: Banco de México con información proporcionada por los intermediarios e INFOSEL.                            
                """)

            else:
                st.warning("Por favor, selecciona al menos una variable para mostrar.")

    elif menu_options == "Referencias":
        st.title(f"Sección actual: {menu_options}")

        with st.expander(":green[INEGI]"):
            #st.text("Inflación INEGI")
            st.markdown("### Notas")
            st.markdown("""
                        
                        Portal Web del Instituto Nacional de Estadística y Geografía [INEGI](https://www.inegi.org.mx/) 
                        
                        #### Inflación

                        Como parte del “Ciclo de Actualización de la Información Económica”, el INEGI actualizó el año base del Índice Nacional de Precios al Consumidor (INPC) a la segunda quincena de julio de 2018 (2a. quincena julio 2018=100).
                        
                        ---

                        #### PIB (Producto Interno Bruto)
                        El Producto Interno Bruto trimestral ofrece, en el corto plazo, una visión oportuna, completa y coherente de la evolución de las actividades económicas del país, proporcionando información oportuna y actualizada, para apoyar la toma de decisiones.

                        """)
            
        with st.expander(":green[Banxico]"):
            st.markdown("### Notas")
            st.markdown("""
                        
                        Portal Web de Banco de México [BANXICO](https://www.banxico.org.mx/) 
                        
                        #### Tasa Objetivo de Banco de México
                        
                        1/ Meta establecida por el Banco de México para la tasa de interés en operaciones de fondeo interbancario a un día.

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

            with open("shf.txt", "r", encoding="utf-8") as file:
                texto = file.read()

            st.markdown("""                    
                        Portal Web de Sociedad Hipotecaria Federal  [SHF](https://www.gob.mx/shf)                      
                        
                        ---

                        """, unsafe_allow_html=True)

            st.markdown(texto)

if __name__ == "__main__":
    main()