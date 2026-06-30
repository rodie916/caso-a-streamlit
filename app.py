import streamlit as st

# >>> CAMBIO VISUAL para validar CI/CD: edita este título y haz push <
st.title("Calculadora de IMC")
st.write("Calcula tu Índice de Masa Corporal.")

peso = st.number_input("Peso (kg):", min_value=0.0, format="%.2f")
est  = st.number_input("Estatura (m):", min_value=0.0, format="%.2f")

if st.button("Calcular IMC"):
    if peso > 0 and est > 0:
        imc = peso / (est ** 2)
        st.write(f"Tu IMC es: {imc:.2f}")
        if imc < 18.5:   st.info("Bajo peso")
        elif imc < 25:   st.success("Peso normal")
        elif imc < 30:   st.warning("Sobrepeso")
        else:            st.error("Obesidad")
    else:
        st.warning("Ingresa valores válidos.")
