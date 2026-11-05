import streamlit as st

st.title("PaaS bulutli ilovasi")

st.header("Talaba ma'lumotlari")

ism = st.text_input("Ismingizni kiriting")

guruh = st.text_input("Guruhingizni kiriting")

if st.button("Natijani ko'rsatish"):
    if ism.strip() and guruh.strip():
        st.success(f"Salom, {ism}!")
        st.write(f"Guruhingiz: {guruh}")
    else:
        st.warning("Barcha maydonlarni to'ldiring")
