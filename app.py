import pandas as pd
import streamlit as st

# Cargar los datos
def cargar_datos():
    recetas = pd.read_csv('recetas.csv')
    equipamiento = pd.read_csv('equipamiento.csv')
    ingredientes = pd.read_csv('ingredientes.csv')
    return recetas, equipamiento, ingredientes

# Buscar receta y devolver ingredientes y equipamiento
def buscar_receta(nombre_receta, num_personas, recetas, equipamiento, ingredientes):
    ingredientes_receta = ingredientes[ingredientes['receta'] == nombre_receta]
    ingredientes_receta['cantidad'] = ingredientes_receta.apply(lambda row: row['cantidad'] * num_personas / row['personas'], axis=1)
    equipos = equipamiento[equipamiento['receta'] == nombre_receta]
    return ingredientes_receta, equipos

# Configuración de la interfaz de Streamlit
def main():
    st.title('Calculadora de Equipamiento de Cocina')

    # Cargar datos
    recetas, equipamiento, ingredientes = cargar_datos()

    # Selección de receta
    receta_seleccionada = st.selectbox('Selecciona una receta', recetas['receta'].unique())

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
