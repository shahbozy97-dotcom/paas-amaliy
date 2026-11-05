import streamlit as st

st.title("Bulutli kalkulyator")

a = st.number_input("Birinchi son", value=0)
b = st.number_input("Ikkinchi son", value=0)

amal = st.selectbox(
    "Amalni tanlang",
    ["Qo'shish", "Ayirish", "Ko'paytirish", "Bo'lish"]
)

if st.button("Hisoblash"):

    if amal == "Qo'shish":
        natija = a + b
        st.success(f"Natija: {natija}")

    elif amal == "Ayirish":
        natija = a - b
        st.success(f"Natija: {natija}")

    elif amal == "Ko'paytirish":
        natija = a * b
        st.success(f"Natija: {natija}")

    elif amal == "Bo'lish":
        if b != 0:
            natija = a / b
            st.success(f"Natija: {natija}")
        else:
            st.warning("Sonni nolga bo'lish mumkin emas!")
