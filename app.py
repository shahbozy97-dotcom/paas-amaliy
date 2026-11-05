import streamlit as st

st.title("Bulutli kalkulyator")

a = st.number_input("Birinchi son", value=0)
b = st.number_input("Ikkinchi son", value=0)

amal = st.selectbox(
    "Amalni tanlang",
    ["Qo'shish", "Ayirish", "Ko'paytirish"]
)

if st.button("Hisoblash"):

    if amal == "Qo'shish":
        natija = a + b

    elif amal == "Ayirish":
        natija = a - b

    else:
        natija = a * b

    st.success(f"Natija: {natija}")
