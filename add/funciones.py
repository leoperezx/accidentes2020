# Este archivo es un complemento solo con funciones para el archivo principal main.py
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import folium_static
import folium


# Organizando df 
def organizando_dataframe(df):
    '''
    La base de datos llega como texto plano y existen columnas 
    que se deben terminar de configurar. Recibe la base de datos
    original (crudo) y realiza las siguientes funciones: 
    - La columna FECHA se configura como "datetime".
    - Los días llegan con un prefijo numérico, este se elimina. 
    '''
      # Convirtiendo columna de fecha en tu DataFrame 
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    # Convirtiendo los nombres de los días a su forma correcta
    df["DIA_SEMANA"] = df['DIA_SEMANA'].replace({"1_LUNES":"LUNES","2_MARTES":"MARTES","3_MIERCOLES":"MIERCOLES","4_JUEVES":"JUEVES","5_VIERNES":"VIERNES","6_SABADO":"SABADO","7_DOMINGO":"DOMINGO"})

    return df

def generar_grafica_grupada_mes(df):
    ''' 
    Genera una gráfica genereal de todo el periodo del registro 
    de todos los accidentes registrados. Recibe la base de datos 
    con la columna de TIEMPO configurada en "datetime".
    '''
    accidentes_por_mes = df.groupby(pd.Grouper(key='FECHA', freq='M')).size().reset_index(name='Número de Accidentes')
    fig = px.line(accidentes_por_mes, x='FECHA', y='Número de Accidentes', title='Tendencia Mensual de Accidentes en 2020')
    return fig,accidentes_por_mes 

def generar_grafica_por_columna(df,columna,etiqueta_en_x):
    '''
    Genera una grafica sumando los valores únicos de una columna.
    Cada uno de los valores únicos se ubica en el eje "x" y la sumatória
    en el eje "y". La función recibe la base de datos con la columna de 
    TIEMPO configurada en "datetime", la columan de interés a sumar sus 
    valores únicos y la etiqueta del eje "x" a poner en la gráfica. 
    '''
    distribucion_dia = df[columna].value_counts().reset_index(name='Número de Accidentes')
    distribucion_dia.columns = [etiqueta_en_x, 'Número de Accidentes']
    fig = px.bar(distribucion_dia, x=etiqueta_en_x, y='Número de Accidentes', title='Distribución de Accidentes por '+etiqueta_en_x)
    return fig

def generar_grafica_hora_plotly(df):
    """
    Genera una gráfica de barras de la distribución de accidentes por hora usando Plotly Express.
    Asume que la columna 'HORA' contiene información de la hora en formato HH:MM:SS.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'HORA' en formato string (HH:MM:SS).

    Returns:
        plotly.graph_objects._figure.Figure: Objeto de figura de Plotly.
    """
    if 'HORA' not in df.columns:
        st.warning("La columna 'HORA' no se encuentra en los datos.")
        return None

    # Extraer la hora como entero
    df['HORA_SOLO'] = df['HORA'].str.split(':').str[0].astype(int)

    # Contar la frecuencia de accidentes por hora y ordenar por hora
    accidentes_por_hora = df['HORA_SOLO'].value_counts().sort_index().reset_index()
    accidentes_por_hora.columns = ['Hora del Día', 'Cantidad de Accidentes']

    # Crear la gráfica de barras con Plotly Express
    fig = px.bar(accidentes_por_hora,
                 x='Hora del Día',
                 y='Cantidad de Accidentes',
                 title='Distribución de Accidentes por Hora en Palmira',
                 labels={'Hora del Día': 'Hora del Día', 'Cantidad de Accidentes': 'Cantidad de Accidentes'})

    # Personalizar la gráfica
    fig.update_xaxes(type='category', tickvals=list(range(24)))
    fig.update_layout(yaxis_title='Cantidad de Accidentes',
                      xaxis_title='Hora del Día',
                      title_font=dict(size=16),
                      xaxis=dict(tickmode='array', tickvals=list(range(24))),
                      yaxis=dict(gridcolor='lightgray'))

    return fig

def generar_mapa(data,opciones):
    '''
    Genera un mapa de los accidentes con un multiselect con los valores 
    únicos de la columna GRAVEDAD. Recibe la base de datos y las opciones 
    con los valores a filtrar.
    '''
    # filtro de los datos
    data_filter = data.loc[data['GRAVEDAD'].isin(opciones)] 
    # Se crea un objeto map de folium como base para cargar los puntos de la base de datos filtrada.
    some_map = folium.Map(location=(3.535513,-76.297656),tiles="cartodbpositron", zoom_start=10)
    # Ajustes para el mapa
    tool_tip="Click me!"    
    # Iteración para agregar los puntos al mapa.
    for row in data_filter.itertuples():
        # configuración de la información extra para cada punto al hacer click.
        pop_up=("<p>Nivel de gravedad:" + row.GRAVEDAD + "</p>" + "<p>Hipótesis del accidente:" + row.HIPOTESIS + "</p>")
        # Adicionando cada punto de forma iterativa.
        folium.Marker([row.LAT,row.LONG], popup=pop_up, tooltip=tool_tip, icon=folium.Icon(color='#F1F2F6',icon_color='#FFABAB')).add_to(some_map)
    # se retorna el objeto con todos los datos configurados.
    return some_map