# Importo las bibliotecas necesarias
# pandas: para manipular y analizar datos tabulares del archivo CSV.
# folium: para crear mapas interactivos.
# streamlit: para construir una interfaz interactiva.
# streamlit_folium: para integrar los mapas de Folium dentro de la aplicación de Streamlit.
# PIL (Pillow): para trabajar con imágenes, en este caso, mostrar fotos de los Idols.
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium
from PIL import Image

# 1. Cargar datos desde el archivo CSV
# Usamos pandas para leer el archivo CSV con los datos de los Idols.
file_path = "myidolnara.csv"  # Ruta del archivo CSV
try:
    latest_data = pd.read_csv(file_path, encoding="latin1")
except FileNotFoundError:
    # Si el archivo no se encuentra, mostramos un mensaje de error y detenemos la ejecución.
    st.error(f"Archivo no encontrado: {file_path}")
    st.stop()

# 2. Limpieza de columnas
# Eliminamos espacios adicionales o caracteres extraños en los nombres de las columnas.
latest_data.rename(columns=lambda x: x.strip(), inplace=True)

# Renombramos específicamente la columna que puede estar afectada por caracteres adicionales como BOM (ï»¿).
if 'ï»¿pics' in latest_data.columns:
    latest_data.rename(columns={'ï»¿pics': 'pics'}, inplace=True)

# 3. Limpieza de coordenadas
# Las columnas 'Latitud' y 'Longitud' contienen caracteres extraños ('Â°', 'N', 'S', etc.).
# Removemos estos caracteres y convertimos las columnas a tipo float para que sean utilizables en los mapas.
latest_data['Latitud'] = (
    latest_data['Latitud']
    .str.replace('Â°', '', regex=False)
    .str.replace(' N', '', regex=False)
    .str.replace(' S', '', regex=False)
    .astype(float, errors='ignore')
)
latest_data['Longitud'] = (
    latest_data['Longitud']
    .str.replace('Â°', '', regex=False)
    .str.replace(' E', '', regex=False)
    .str.replace(' W', '', regex=False)
    .astype(float, errors='ignore')
)

# 4. Título de la aplicación
# Mostramos un título en la interfaz de Streamlit.
st.title("Información y Mapa Interactivo de Idols")

# 5. Selección del Idol
# Creamos un menú desplegable para que el usuario seleccione un Idol basado en la columna 'Nombres'.
nombre_idol = st.selectbox("Selecciona un Idol:", latest_data['Nombres'].unique())

# 6. Mostrar información del Idol seleccionado
if nombre_idol:
    # Filtramos los datos del Idol seleccionado por su nombre.
    idol_data = latest_data[latest_data['Nombres'] == nombre_idol]
    
    if not idol_data.empty:  # Verificamos que el filtro no esté vacío.
        # Subtítulo para la información del Idol.
        st.subheader(f"Información de {nombre_idol}")
        
        # Convertimos los datos relevantes a formato de lista para mostrar en viñetas.
        nacionalidad = idol_data.iloc[0]['Nacionalidad']
        latitud = idol_data.iloc[0]['Latitud']
        longitud = idol_data.iloc[0]['Longitud']
        hobbies = idol_data.iloc[0]['Hobbies']
        tipo_sangre = idol_data.iloc[0]['Tipo de sangre']
        mbti = idol_data.iloc[0]['MBTI']
        grupo = idol_data.iloc[0]['Grupo-solista']
        signo = idol_data.iloc[0]['Signo']
        edad = idol_data.iloc[0]['Edad']
        
        # Mostramos los datos en viñetas
        st.markdown(f"""
        - **Nacionalidad:** {nacionalidad}
        - **Hobbies:** {hobbies}
        - **Tipo de Sangre:** {tipo_sangre}
        - **MBTI:** {mbti}
        - **Grupo/Solista:** {grupo}
        - **Signo:** {signo}
        - **Edad:** {edad} años
        """)

        # 7. Mostrar la foto del Idol
        # Creamos la ruta relativa a la carpeta 'pics' y tratamos de abrir la imagen.
        foto_path = f"pics/{idol_data.iloc[0]['pics']}"
        try:
            imagen = Image.open(foto_path)
            # Mostramos la imagen con un subtítulo que indica el nombre del Idol.
            st.image(imagen, caption=f"Foto de {nombre_idol}", use_column_width=True)
        except FileNotFoundError:
            # Si no se encuentra la imagen, mostramos un mensaje de advertencia.
            st.warning(f"No se encontró la foto para '{nombre_idol}' en {foto_path}")
        
        # 8. Crear el mapa interactivo
        # Usamos Folium para crear un mapa centrado en las coordenadas del Idol.
        mapa = folium.Map(location=[latitud, longitud], zoom_start=10)
        # Añadimos un marcador en la ubicación del Idol con un popup que muestra su nombre y nacionalidad.
        folium.Marker(
            location=[latitud, longitud],
            popup=f"{nombre_idol}\nUbicación: {nacionalidad}",
            tooltip="Clic para más información"
        ).add_to(mapa)
        
        # 9. Mostrar el mapa en Streamlit
        # Renderizamos el mapa dentro de la aplicación.
        st.subheader("Mapa Interactivo")
        st_folium(mapa, width=700, height=500)
    else:
        # Si no se encuentra información del Idol, mostramos una advertencia.
        st.warning(f"No se encontró información para '{nombre_idol}'.")
