import streamlit as st

st.title("Bulutli kalkulyator")

st.header("Ikki son yig'indisini hisoblash")

a = st.number_input("Birinchi son", value=0)

b = st.number_input("Ikkinchi son", value=0)

if st.button("Hisoblash"):
    natija = a + b
    st.success(f"Yig'indi: {natija}")
