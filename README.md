# Accidentes 2020

*Resumen*: Análisis de los accidentes de vehículos del año 2020 en la ciudad de Palmira, Valle, Colombia

*Descripción*: La siguiente aplicación es un trabajo en proceso de construcción ya que también es un ejercicio académico personal que ya lleva varios años. Me interesa aprendender sobre programación en _Python_, el anális de datos con _Pandas_ y la forma de representarlos de una forma clara y comprensible para cualquier persona con *Streamlit*. Creo que esta combinación de herramientas es ideal para aprender sobre el _Análisis de datos_ es por eso que dejo aquí un pequeño desarrollo con el cual demuestro mi habilidad con el animo de seguir mejorando y practicando.  

*Requerimientos*:

- pandas

- plotly.express

- folium

- streamlit_folium

### Captura

La siguiente imágen es una captura de la aplicación en funcionamiento. 

<img title="" src="add/Captura.png" alt="" width="659" data-align="center">

### Recomendaciones de IA

Despues de llegar a cierto punto con la aplicación, decidí pasar por una IA para leer su recomendación y saber como podría mejorar. He copiado toda la recomendación y pienso dejarla en este _README.md_ para recordar y realizar los cambios.

A medida que realice los cambios que me parezcan apropiados, seguramente los voy a ir borrando del texto.

''' _respuesta de la IA_

**Organización y Estructura:**

1. **Carpeta para Componentes Streamlit (Opcional pero Recomendable):** Si tu aplicación sigue creciendo y tienes lógica de interfaz de usuario más compleja, podrías considerar crear una carpeta para componentes personalizados de Streamlit. Por ejemplo, podrías tener funciones que generen selectores específicos, tarjetas de información, etc.

2. **Nombres de Archivos Descriptivos:** Los nombres `main.py` y `funciones.py` son bastante genéricos. Si tu archivo de funciones se enfoca en un área específica (ej. `graficos.py`, `mapas.py`, `data_processing.py`), podría ser más explícito a medida que el proyecto crece.

3. **Comentarios y Documentación (¡Excelente que ya los tengas!):** Sigue comentando tu código, especialmente las funciones en `funciones.py`. Considera usar docstrings más extensos en las funciones para explicar qué hacen, cuáles son sus argumentos y qué devuelven. Esto facilita la comprensión y el uso futuro de tus funciones.

**Funciones (`funciones.py`):**

1. **Manejo de Errores y Valores Faltantes:** En tus funciones de generación de gráficos, podrías añadir manejo para casos donde la columna especificada no exista en el DataFrame o tenga valores faltantes que puedan causar errores en la visualización.

2. **Flexibilidad en las Gráficas:** La función `generar_grafica_por_columna` es muy útil. Podrías hacerla aún más flexible permitiendo pasar argumentos adicionales a `plotly.express.bar`, como el título o los nombres de los ejes, directamente desde `main.py`.
   
   Python
   
   ```
   # En funciones.py
   def generar_grafica_por_columna(df, columna, etiqueta_en_x, titulo=None, color=None):
      distribucion = df[columna].value_counts().reset_index(name='Número de Accidentes')
      distribucion.columns = [etiqueta_en_x, 'Número de Accidentes']
      fig = px.bar(distribucion, x=etiqueta_en_x, y='Número de Accidentes', title=titulo, color=color)
      return fig
   
   # En main.py
   if 'DIA_SEMANA' in data.columns:
      fig_dia = fn.generar_grafica_por_columna(data,'DIA_SEMANA','Día de la Semana', titulo='Distribución de Accidentes por Día de la Semana', color='skyblue')
      st.plotly_chart(fig_dia)
   ```

3. **Separación de Lógica de Filtrado en el Mapa:** En la función `generar_mapa`, la lógica de filtrado (`data_filter = data.loc[data['GRAVEDAD'].isin(opciones)]`) se realiza dentro de la función. Podrías considerar pasar el DataFrame ya filtrado a la función `generar_mapa` desde `main.py`. Esto haría la función más reutilizable si quisieras mostrar mapas de otros subconjuntos de datos.

4. **Personalización del Mapa:** Podrías permitir más opciones de personalización del mapa desde `main.py`, como el zoom inicial, los colores de los marcadores, o incluso la elección de diferentes tipos de mapas base (`tiles`).

**Archivo Principal (`main.py`):**

1. **Mejor Organización del Layout:** A medida que añades más visualizaciones y controles, considera usar las utilidades de layout de Streamlit como `st.columns`, `st.expander`, y `st.tabs` para organizar la información de manera más clara y evitar que la página se vuelva demasiado larga y confusa.

2. **Interactividad Avanzada:** Explora más los widgets de Streamlit para hacer la aplicación más interactiva. Por ejemplo:
   
   - **Selectores Múltiples:** Permitir al usuario seleccionar múltiples barrios o tipos de vehículos para filtrar los análisis.
   - **Sliders:** Para filtrar por rangos de horas o fechas (si tuvieras un rango de años más amplio).
   - **Botones para Acciones:** Disparar análisis o visualizaciones específicas bajo demanda.

3. **Manejo de Fechas:** Si bien ya convertiste la columna 'FECHA' a datetime, podrías añadir selectores de rango de fechas para permitir al usuario analizar períodos específicos dentro del año 2020.

4. **Visualizaciones Adicionales:** Considera otras visualizaciones que podrían ser interesantes:
   
   - **Gráficos de dispersión:** Para explorar la relación entre dos variables (si tiene sentido en tu conjunto de datos).
   - **Mapas de calor:** Para visualizar la concentración de accidentes en diferentes áreas de Palmira.
   - **Gráficos de barras apiladas o agrupadas:** Para comparar la distribución de una variable (ej. gravedad) dentro de diferentes categorías (ej. día de la semana).

5. **Texto Explicativo y Conclusiones:** Sigue desarrollando la sección de conclusiones. Basándote en las visualizaciones, explica las tendencias y patrones que observas. Considera añadir recomendaciones basadas en tus hallazgos.

6. **Optimización del Rendimiento:** Para conjuntos de datos más grandes, considera técnicas de optimización como la carga por lotes o el uso de otras librerías de visualización que puedan manejar grandes cantidades de datos de manera más eficiente (aunque para el tamaño de datos de un año, probablemente no sea un problema ahora).

7. **Pruebas:** A medida que añades más funcionalidades, asegúrate de probar tu aplicación con diferentes selecciones y filtros para garantizar que todo funcione correctamente.

**General:**

1. **Streamlit Cloud:** Cuando estés listo para compartir tu aplicación, Streamlit Cloud es una forma muy sencilla de desplegarla de forma gratuita.

2. **Comunidad Streamlit:** Explora la comunidad de Streamlit (foros, documentación, ejemplos). Hay muchos recursos y ejemplos de proyectos similares que te pueden dar ideas.

'''

Además de todos estas mejoras, también debo revisar el trabajo anterior:
Todo el proceso se puede ver en:

- [limpieza de accidentes (1)](https://www.kaggle.com/code/leonardoperezhurtado/limpieza-accidentes-palmira-1)

- [Limpieza de accidentes (2)](https://www.kaggle.com/code/leonardoperezhurtado/limpieza-accidentes-palmira-2)
  
- [Trabajando con los datos de los accidentes (3)](https://www.kaggle.com/code/leonardoperezhurtado/datos-accidentes-palmira-3)

---

> &copy; 2025 Twitter: [@leoperezx](https://twitter.com/leoperezx)
