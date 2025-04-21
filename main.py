import streamlit as st
import pandas as pd
import add.funciones as fn
import plotly.express as px
from PIL import Image
from streamlit_folium import folium_static
import folium
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# variables
IMAGE = Image.open('add/img-map.jpg')
APP_FINAL = '''
Quedo atento a comentarios, preguntas, dudas, críticas constructivas, felicitaciones, ayuda y apoyo tanto en ideas para el análisis como para temas laborales<br><br>Todavía exisite mucha información sin analizar, muchas operaciones a realizar y funciones por aprender. Programo mientras aprendo, estudio mientras construyo.\n\n
Veras muchos cambios a lo largo de este proyecto. **Esto es de prueba y error**. En el siguiente enlace se encuentra los archivos base de [este trabajo y el trabajo previo](https://github.com/leoperezx/accidentes2020/tree/main). Gracias por llegar hasta aquí y estar interesado.
'''

FIRMA = '''
---
> &copy; 2025 Twitter: [@leoperezx](https://twitter.com/leoperezx)
'''

PRESENTACION_MAPA = "El mapa presenta los distinto accidentes de motocicletas. Si le das click a cada punto, podrás conocer la hipotesis y la gravedad del accidente. Puedes seleccionear uno o varios tipo de gravedad de accidentes hasta presentar todos los accidentes en el mapa. El mapa es interactivo y pudes acercarte y explorar mas de cerca con cada uno de los puntos."

CONCLUCIONES = "En general los accidentes aumentan al ir finalizando el año. Se presentan con menor frecuencia en los meses de Abril, Mayo y Junio. Es notable el ascenso de los accidentes a partir de Julio. en general los días más comunes para los accidentes son los lunes y los viernes, donde los accidentes de motocicletas son muy numerosos, alcanzando una cifra cercana al 50 \% de todos los registros. \n \nLos accidentes en motocicletas tienen la misma tendencia al registro general, con muchos accidentes al final y principio del año, donde y la mayoría de accidentes en motocicleta se presentaron entre las 11 y las 12 horas del día, junto con otro pico entre las 13 y las 14 horas del día. Sin embargo los días más comunes para los accidentes en motocicleta en el año 2020 fueron los días Viernes y Lunes."

def main():
    # Configuración de la página de Streamlit
    st.set_page_config(page_title="Análisis de Accidentes de Tránsito", layout="wide")    # Título de la aplicación
    st.title("Análisis de Accidentes de Tránsito en Palmira - 2020")

    # --- Carga de Datos ---
    @st.cache_data
    def cargar_datos(archivo_csv):
        data = pd.read_csv(archivo_csv)
        return data

    data = cargar_datos("add/Accidentes_limpio.csv")
    data = fn.organizando_dataframe(data) # <---- Línea añadida aquí

    # --- Sección de Filtros ---
    st.sidebar.header("Filtros")

    # Filtro por día de la semana
    dias_semana_unicos = data['DIA_SEMANA'].unique()
    dias_seleccionados = st.sidebar.multiselect("Seleccionar día(s) de la semana", dias_semana_unicos, default=dias_semana_unicos)
    data_filtrada = data[data['DIA_SEMANA'].isin(dias_seleccionados)]

    # Filtro por rango de fechas
    fecha_min = data_filtrada['FECHA'].min().date()
    fecha_max = data_filtrada['FECHA'].max().date()
    rango_fechas = st.sidebar.date_input("Seleccionar rango de fechas", (fecha_min, fecha_max))
    if len(rango_fechas) == 2:
        fecha_inicio, fecha_fin = rango_fechas
        data_filtrada = data_filtrada[(data_filtrada['FECHA'].dt.date >= fecha_inicio) & (data_filtrada['FECHA'].dt.date <= fecha_fin)]

    # --- Sección de Análisis General y Específico de Motocicletas ---
    st.header("Análisis de Accidentes")

    data_motos_filtrada = data_filtrada[data_filtrada['CLASE_DE_VEHICULO'].str.contains('MOTO', case=False, na=False)].copy()

    # Crear subplots
    fig = make_subplots(rows=3, cols=2,
                        subplot_titles=('Tendencia General de Accidentes',
                                        'Distribución General por Día de la Semana',
                                        'Distribución General por Clase de Vehículo',
                                        'Distribución General por Hipótesis (Top 10)',
                                        'Tendencia de Accidentes de Motocicletas',
                                        'Distribución de Accidentes de Motocicletas por Día de la Semana'))

    # Gráfica 1: Tendencia General
    if 'FECHA' in data_filtrada.columns:
        accidentes_por_mes_filtrados = data_filtrada.groupby(pd.Grouper(key='FECHA', freq='M')).size().reset_index(name='Número de Accidentes')
        fig.add_trace(go.Scatter(x=accidentes_por_mes_filtrados['FECHA'], y=accidentes_por_mes_filtrados['Número de Accidentes'],
                                 mode='lines', name='General'), row=1, col=1)
    else:
        st.warning("La columna 'FECHA' no se encuentra en los datos filtrados para la tendencia general.")

    # Gráfica 2: Distribución General por Día de la Semana
    if 'DIA_SEMANA' in data_filtrada.columns:
        distribucion_dia = data_filtrada['DIA_SEMANA'].value_counts().reset_index(name='Número de Accidentes')
        distribucion_dia.columns = ['Día de la Semana', 'Número de Accidentes']
        fig.add_trace(go.Bar(x=distribucion_dia['Día de la Semana'], y=distribucion_dia['Número de Accidentes'],
                             name='General'), row=1, col=2)
    else:
        st.warning("La columna 'DIA_SEMANA' no se encuentra en los datos filtrados para la distribución por día general.")

    # Gráfica 3: Distribución General por Clase de Vehículo
    if 'CLASE_DE_VEHICULO' in data_filtrada.columns:
        distribucion_vehiculos = data_filtrada['CLASE_DE_VEHICULO'].value_counts().nlargest(10).reset_index(name='Número de Accidentes')
        distribucion_vehiculos.columns = ['Clase de Vehículo', 'Número de Accidentes']
        fig.add_trace(go.Bar(x=distribucion_vehiculos['Clase de Vehículo'], y=distribucion_vehiculos['Número de Accidentes'],
                             name='General'), row=2, col=1)
    else:
        st.warning("La columna 'CLASE_DE_VEHICULO' no se encuentra en los datos filtrados para la distribución general de vehículos.")

    # Gráfica 4: Distribución General por Hipótesis (Top 10)
    if 'HIPOTESIS' in data_filtrada.columns:
        n_hipotesis_principales = 10
        distribucion_hipotesis = data_filtrada['HIPOTESIS'].value_counts().nlargest(n_hipotesis_principales).reset_index(name='Número de Accidentes')
        distribucion_hipotesis.columns = ['Hipótesis', 'Número de Accidentes']
        fig.add_trace(go.Bar(x=distribucion_hipotesis['Hipótesis'], y=distribucion_hipotesis['Número de Accidentes'],
                             name='General'), row=2, col=2)
    else:
        st.warning("La columna 'HIPOTESIS' no se encuentra en los datos filtrados para la distribución de hipótesis.")

    # Gráfica 5: Tendencia de Accidentes de Motocicletas
    if 'FECHA' in data_motos_filtrada.columns and not data_motos_filtrada.empty:
        accidentes_motos_mes = data_motos_filtrada.groupby(pd.Grouper(key='FECHA', freq='M')).size().reset_index(name='Número de Accidentes')
        fig.add_trace(go.Scatter(x=accidentes_motos_mes['FECHA'], y=accidentes_motos_mes['Número de Accidentes'],
                                 mode='lines', name='Motocicletas'), row=3, col=1)
    else:
        st.info("No se encontraron registros de accidentes de motocicletas en el periodo seleccionado para la tendencia.")

    # Gráfica 6: Distribución de Accidentes de Motocicletas por Día de la Semana
    if 'DIA_SEMANA' in data_motos_filtrada.columns and not data_motos_filtrada.empty:
        distribucion_dia_motos = data_motos_filtrada['DIA_SEMANA'].value_counts().reset_index(name='Número de Accidentes')
        distribucion_dia_motos.columns = ['Día de la Semana', 'Número de Accidentes']
        fig.add_trace(go.Bar(x=distribucion_dia_motos['Día de la Semana'], y=distribucion_dia_motos['Número de Accidentes'],
                             name='Motocicletas'), row=3, col=2)
    else:
        st.info("No se encontraron registros de accidentes de motocicletas en el periodo seleccionado para la distribución por día.")

    fig.update_layout(height=1200, width=900, title_text="Análisis General vs. Específico de Motocicletas")
    st.plotly_chart(fig)

    # --- Sección de Comparativas Interactivas (Se puede mantener o ajustar) ---
    st.header("Comparativas Interactivas")

    if 'FECHA' in data_filtrada.columns and 'FECHA' in data_motos_filtrada.columns and not data_motos_filtrada.empty:
        st.subheader("Comparación de Tendencia General vs. Motocicletas en el Periodo Seleccionado")
        comparar_tendencia = st.checkbox("Mostrar tendencia de motocicletas junto con la tendencia general (en gráfica separada)")
        accidentes_por_mes_general_filtrado = data_filtrada.groupby(pd.Grouper(key='FECHA', freq='M')).size().reset_index(name='Número de Accidentes')
        fig_comparativa_tendencia = px.line(accidentes_por_mes_general_filtrado, x='FECHA', y='Número de Accidentes', title='Tendencia General de Accidentes en el Periodo Seleccionado', color_discrete_sequence=['blue'])
        if comparar_tendencia:
            accidentes_motos_mes_filtrado = data_motos_filtrada.groupby(pd.Grouper(key='FECHA', freq='M')).size().reset_index(name='Número de Accidentes')
            fig_comparativa_tendencia.add_scatter(x=accidentes_motos_mes_filtrado['FECHA'], y=accidentes_motos_mes_filtrado['Número de Accidentes'], mode='lines', name='Motocicletas', line=dict(color='red'))
        st.plotly_chart(fig_comparativa_tendencia)

    # --- Conclusiones y Recomendaciones ---
    st.header("Conclusiones y Recomendaciones")
    st.write(CONCLUCIONES)
    st.markdown("---")
    st.subheader("Mapa interactivo de accidentes de motocicletas - Palmira 2020")
    st.write(PRESENTACION_MAPA)
    data_filter_mapa = data_filtrada[(data_filtrada['CLASE_DE_VEHICULO']=='MOTO')]

    options = st.multiselect('¿Gravedad de accidente en motocicleta que desea consultar?',
        ['DAÑOS','HERIDOS','MUERTO'],key="selection_mapa")

    if st.button("Crear mapa"):
        mapa = fn.generar_mapa(data_filter_mapa,options)
        folium_static(mapa)
    else:
        st.image(IMAGE, width=600, caption="Imagen provicional")

    st.write(APP_FINAL)
    st.markdown(FIRMA)

if __name__=="__main__":
    main()