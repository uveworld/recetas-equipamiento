import pandas as pd
import streamlit as st

# Cargar los datos
def cargar_datos():
    recetas = pd.read_csv('recetas.csv')
    equipamiento = pd.read_csv('equipamiento.csv')
    ingredientes = pd.read_csv('ingredientes.csv')
    return recetas, equipamiento, ingredientes

# Buscar recetas por palabra clave
def buscar_recetas_por_palabra_clave(palabra_clave, recetas):
    recetas_encontradas = recetas[recetas['receta'].str.contains(palabra_clave, case=False, na=False)]
    return recetas_encontradas['receta'].unique()

# Buscar receta y devolver ingredientes y equipamiento
def buscar_receta(nombre_receta, num_personas, recetas, equipamiento, ingredientes):
    ingredientes_receta = ingredientes[ingredientes['receta'] == nombre_receta]
    ingredientes_receta['cantidad'] = ingredientes_receta.apply(lambda row: row['cantidad'] * num_personas / row['personas'], axis=1)
    ingredientes_receta['cantidad'] = ingredientes_receta['cantidad'].astype(str) + ' ' + ingredientes_receta['unidad']
    equipos = equipamiento[equipamiento['receta'] == nombre_receta]
    return ingredientes_receta, equipos

# Configuración de la interfaz de Streamlit
def main():
    st.title('Calculadora de Equipamiento de Cocina')

    # Cargar datos
    recetas, equipamiento, ingredientes = cargar_datos()

    # Barra de búsqueda
    palabra_clave = st.text_input('Buscar receta por palabra clave')

    receta_seleccionada = None
    if palabra_clave:
        recetas_encontradas = buscar_recetas_por_palabra_clave(palabra_clave, recetas)
        if len(recetas_encontradas) > 0:
            receta_seleccionada = st.selectbox('Resultados de la búsqueda', recetas_encontradas)
        else:
            st.write('No se encontraron recetas que coincidan con la palabra clave.')

    if not receta_seleccionada:
        receta_seleccionada = st.selectbox('O seleccionar una receta', recetas['receta'].unique())

    # Número de personas
    num_personas = st.number_input('Número de personas', min_value=1, step=1, value=4)

    if receta_seleccionada:
        ingredientes, equipos = buscar_receta(receta_seleccionada, num_personas, recetas, equipamiento, ingredientes)

        st.subheader('Ingredientes')
        st.write(ingredientes[['ingrediente', 'cantidad']])

        st.subheader('Equipamiento Necesario')
        st.write(equipos['equipamiento'])

if __name__ == "__main__":
    main()
