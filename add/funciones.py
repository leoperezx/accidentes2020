# Este archivo es un complemento solo con funciones para el archivo principal main.py

import pandas as pd
import plotly.express as px
from streamlit_folium import folium_static
import folium


# Organizando df 
def organizando_dataframe(df):
    '''
    La base de datos llega como texto plano y existen columnas 
    que se deben terminar de configurar.
    - La columna FECHA se configura como "datetime"
    - Los días llegan con un prefijo numérico, este se elimina 
    '''
      # Convirtiendo columna de fecha en tu DataFrame 
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    # Convirtiendo los nombres de los días a su forma correcta
    df["DIA_SEMANA"] = df['DIA_SEMANA'].replace({"1_LUNES":"LUNES","2_MARTES":"MARTES","3_MIERCOLES":"MIERCOLES","4_JUEVES":"JUEVES","5_VIERNES":"VIERNES","6_SABADO":"SABADO","7_DOMINGO":"DOMINGO"})

    return df

def generar_grafica_grupada_mes(df):
    
    accidentes_por_mes = df.groupby(pd.Grouper(key='FECHA', freq='M')).size().reset_index(name='Número de Accidentes')
    fig = px.line(accidentes_por_mes, x='FECHA', y='Número de Accidentes', title='Tendencia Mensual de Accidentes en 2020')
    return fig,accidentes_por_mes 

def generar_grafica_por_columna(df,columna,etiqueta_en_x):
    distribucion_dia = df[columna].value_counts().reset_index(name='Número de Accidentes')
    distribucion_dia.columns = [etiqueta_en_x, 'Número de Accidentes']
    fig = px.bar(distribucion_dia, x=etiqueta_en_x, y='Número de Accidentes', title='Distribución de Accidentes por '+etiqueta_en_x)
    return fig

def generar_mapa(data,opciones):
    
    data_filter = data.loc[data['GRAVEDAD'].isin(opciones)] 

    some_map = folium.Map(location=(3.535513,-76.297656),tiles="cartodbpositron", zoom_start=10)

    tool_tip="Click me!"    


    for row in data_filter.itertuples():
        pop_up=("<p>Nivel de gravedad:" + row.GRAVEDAD + "</p>" + "<p>Hipótesis del accidente:" + row.HIPOTESIS + "</p>")
        
        folium.Marker([row.LAT,row.LONG], popup=pop_up, tooltip=tool_tip, icon=folium.Icon(color='#F1F2F6',icon_color='#FFABAB')).add_to(some_map)

    return some_map