import streamlit as st
import pandas as pd
import add.funciones as fn
import plotly.express as px  # Una librería interactiva muy útil para Streamlit
from PIL import Image
from streamlit_folium import folium_static
import folium


# variables 
IMAGE = Image.open('add/img-map.jpg')
APP_FINAL = '''
El mapa presenta los distinto accidentes de motocicletas. Si le das click a cada punto, podrás conocer la hipotesis y la gravedad del accidente. Puedes seleccionear uno o varios tipo de gravedad de accidentes y hasta presentar todos los accidentes en el mapa. El mapa es interactivo y pudes acercarte y explorar mas de cerca con cada uno de los puntos.\n\n
Quedo atento a comentarios, preguntas, dudas, críticas constructivas, felicitaciones, ayuda y apoyo tanto en ideas para el análisis como para temas laborales<br><br>Todavía exisite mucha información sin analizar, muchas operaciones a realizar y funciones por aprender. Programo mientras aprendo, estudio mientras construyo.\n\n
Veras muchos cambios a lo largo de este proyecto. **Esto es de prueba y error**. En el siguiente enlace se encuentra los archivos base de [este trabajo y el trabajo previo](https://github.com/leoperezx/accidentes2020/tree/main). Gracias por llegar hasta aquí y estar interesado. 
'''

FIRMA = '''
--- 
> &copy; 2025 Twitter: [@leoperezx](https://twitter.com/leoperezx)
'''



CONCLUCIONES = "En general los accidentes aumentan al ir finalizando el año. Se presentan con menor frecuencia en los meses de Abril, Mayo y Junio. Es notable el ascenso de los accidentes a partir de Julio. en genral los días más comunes para los accidentes son los Lunes y los viernes, donde los accidentes de motocicletas son muy numerosos alcanzando una cifra cercana al 50 \% de todos los registros. \n \nLos accidentes en motocicletas tienen la mista tendencia al registro general, con muchos accidentes al final y principio del año donde y la mayoría se presentaron entre las 11 y las 12 horas del día, junto con otro pico entre las 13 y las 14 horas del día. Sin embargo los días más comunes para los accidentes en motocicleta en el año 2020 fueron los días Viernes y Lunes."

def main():
    # Título de la aplicación
    st.title("Análisis de Accidentes de Tránsito en Palmira - 2020")

    # --- Carga de Datos ---
    @st.cache_data  # Para que Streamlit guarde en caché los datos y no los recargue cada vez
    def cargar_datos(archivo_csv):
        data = pd.read_csv(archivo_csv)
        return data

    data = cargar_datos("add/Accidentes_limpio.csv") # Reemplaza "tu_archivo_de_datos.csv" con el nombre real de tu archivo

    # --- Sección de Análisis General ---
    st.header("Análisis General de Accidentes")

    # Organizando la información
    data = fn.organizando_dataframe(data)

    # Lista de columnas:
    # GRAVEDAD,FECHA,HORA,JORNADA,DIA_SEMANA,BARRIOS_CORREGIMIENTO_VIA,DIRECCION,ZONA,AUTORIDAD,LAT,LONG,HIPOTESIS,CONDICION_DE_LA_VICTIMA,CLASE_DE_SINIESTRO,LESIONADO,HOMICIDIOS,CLINICA,SITIO,CLASE_DE_VEHICULO,MARCA,MATRICULA,TIPO_DE_SERVICIO,EMPRESA

    if 'FECHA' in data.columns:

        fig_tendencia,accidentes_por_mes = fn.generar_grafica_grupada_mes(data)
        st.plotly_chart(fig_tendencia)
    else:
        st.warning("La columna 'FECHA' no se encuentra en los datos para mostrar la tendencia temporal.")

    # Distribución por Día de la Semana
    if 'DIA_SEMANA' in data.columns: # generar_grafica_por_columna(data,'DIA_SEMANA','Día de la Semana')
        
        fig_dia = fn.generar_grafica_por_columna(data,'DIA_SEMANA','Día de la Semana')
        st.plotly_chart(fig_dia)
    else:
        st.warning("La columna 'DIA_SEMANA' no se encuentra en los datos para mostrar la distribución por día.")

    # distribución por Clase de vehículo
    if 'CLASE_DE_VEHICULO' in data.columns:
        
        fig_vehiculos = fn.generar_grafica_por_columna(data,'CLASE_DE_VEHICULO','Clase de vehículos')
        st.plotly_chart(fig_vehiculos)
    else:
        st.warning("La columna 'CLASE_DE_VEHICULO' no se encuentra en los datos para mostrar la distribución.")

    # Distribución por hipótesis
    if 'HIPOTESIS' in data.columns:
        n_hipotesis_principales = 10  # Por ejemplo, mostrar las 10 hipótesis más frecuentes

        distribucion_hipotesis = data['HIPOTESIS'].value_counts().nlargest(n_hipotesis_principales).reset_index(name='Número de Accidentes')
        distribucion_hipotesis.columns = ['Hipótesis', 'Número de Accidentes']

        fig_hipotesis_principales = px.bar(distribucion_hipotesis, x='Hipótesis', y='Número de Accidentes',
                                        title=f'Las {n_hipotesis_principales} Hipótesis de Accidentes Más Frecuentes')
        st.plotly_chart(fig_hipotesis_principales)
    else:
        st.warning("La columna 'HIPOTESIS' no se encuentra en los datos para mostrar la distribución.")

    # Ejemplo de cómo usar esta función en tu main.py
    if 'HORA' in data.columns:
        fig_hora_plotly = fn.generar_grafica_hora_plotly(data.copy()) # Usa .copy() para evitar modificar el DataFrame original
        if fig_hora_plotly:
            st.plotly_chart(fig_hora_plotly)
    else:
        st.warning("La columna 'HORA' no se encuentra en los datos para mostrar la distribución por hora.")

    # --- Sección de Análisis Específico de Motocicletas ---
    st.header("Análisis Específico de Accidentes de Motocicletas")

    # Filtrar los datos para incluir solo accidentes con motocicletas
    data_motos = data[data['CLASE_DE_VEHICULO'].str.contains('MOTO', case=False, na=False)] # Ajusta 'TIPO_VEHICULO' si el nombre de tu columna es diferente

    if not data_motos.empty:
        # Tendencia Temporal (Solo Motocicletas)
        st.subheader("Tendencia de Accidentes de Motocicletas a lo Largo del Tiempo")
        if 'FECHA' in data_motos.columns:
            accidentes_motos_mes = data_motos.groupby(pd.Grouper(key='FECHA', freq='M')).size().reset_index(name='Número de Accidentes')
            fig_tendencia_motos = px.line(accidentes_motos_mes, x='FECHA', y='Número de Accidentes', title='Tendencia Mensual de Accidentes de Motocicletas en 2020')
            st.plotly_chart(fig_tendencia_motos)
        else:
            st.warning("La columna 'FECHA' no se encuentra en los datos filtrados de motocicletas.")

        # Distribución por Día de la Semana (Solo Motocicletas)
        if 'DIA_SEMANA' in data_motos.columns:
            distribucion_dia_motos = data_motos['DIA_SEMANA'].value_counts().reset_index(name='Número de Accidentes')
            distribucion_dia_motos.columns = ['Día de la Semana', 'Número de Accidentes']
            fig_dia_motos = px.bar(distribucion_dia_motos, x='Día de la Semana', y='Número de Accidentes', title='Distribución de Accidentes de Motocicletas por Día de la Semana')
            st.plotly_chart(fig_dia_motos)
        else:
            st.warning("La columna 'DIA_SEMANA' no se encuentra en los datos filtrados de motocicletas.")

        # ... (Aquí irían las demás visualizaciones específicas para motocicletas)
    else:
        st.info("No se encontraron registros de accidentes de motocicletas en los datos.")

    # --- Sección de Comparativas Interactivas ---
    st.header("Comparativas Interactivas")

    # Ejemplo de selector para comparar la tendencia general con la de motocicletas
    if 'FECHA' in data.columns and 'FECHA' in data_motos.columns and not data_motos.empty:
        st.subheader("Comparación de Tendencia General vs. Motocicletas")
        comparar_tendencia = st.checkbox("Mostrar tendencia de motocicletas junto con la tendencia general")
        fig_comparativa_tendencia = px.line(accidentes_por_mes, x='FECHA', y='Número de Accidentes', title='Tendencia General de Accidentes en 2020', color_discrete_sequence=['blue'])
        if comparar_tendencia:
            fig_comparativa_tendencia.add_scatter(x=accidentes_motos_mes['FECHA'], y=accidentes_motos_mes['Número de Accidentes'], mode='lines', name='Motocicletas', line=dict(color='red'))
        st.plotly_chart(fig_comparativa_tendencia)

    # ... (Aquí irían más selectores para permitir al usuario elegir qué variables comparar)

    # --- Conclusiones y Recomendaciones ---
    st.header("Conclusiones y Recomendaciones")
    st.write(CONCLUCIONES)
    st.markdown("---")
    st.subheader("Mapa interactivo de accidentes de motocicletas - Palmira 2020")
    data_filter = data[(data['CLASE_DE_VEHICULO']=='MOTO')] # DAÑOS,HERIDOS,MUERTO

    options = st.multiselect('¿Gravedad de accidente en motocicleta que desea consultar?',
        ['DAÑOS','HERIDOS','MUERTO'],key="selection")

    if st.button("Crear mapa"):
        mapa = fn.generar_mapa(data_filter,options)
        folium_static(mapa)
    else: 
        st.image(IMAGE, width=600, caption="Imagen provicional")
    
    st.write(APP_FINAL)
    st.markdown(FIRMA)

if __name__=="__main__":
    main()
