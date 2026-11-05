
import streamlit as st
import math

st.set_page_config(
    page_title="Pro Calculator",
    page_icon="🧮",
    layout="centered"
)

# Dizayn
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #202f4a);
}
h1 {
    color: #65e6ff;
    text-align: center;
}
.calculator {
    background: #172338;
    padding: 25px;
    border-radius: 20px;
}
.result {
    background: #0d1728;
    color: #65e6ff;
    padding: 20px;
    border-radius: 12px;
    text-align: right;
    font-size: 32px;
    font-weight: bold;
}
.stButton button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🧮 PRO CALCULATOR</h1>", unsafe_allow_html=True)
st.caption("Professional hisoblash tizimi")

# Tarix
if "history" not in st.session_state:
    st.session_state.history = []

# Sonlar
col1, col2 = st.columns(2)

with col1:
    a = st.number_input("Birinchi son", value=0.0, key="num1")

with col2:
    b = st.number_input("Ikkinchi son", value=0.0, key="num2")

st.markdown("---")

operation = st.selectbox(
    "Amalni tanlang",
    [
        "Qo‘shish (+)",
        "Ayirish (-)",
        "Ko‘paytirish (×)",
        "Bo‘lish (÷)",
        "Foiz (%)",
        "Darajaga ko‘tarish (^)",
        "Ildiz chiqarish (√)"
    ]
)

if st.button("🟢 HISOBLASH", use_container_width=True):
    try:
        if operation == "Qo‘shish (+)":
            result = a + b
            formula = f"{a} + {b}"

        elif operation == "Ayirish (-)":
            result = a - b
            formula = f"{a} - {b}"

        elif operation == "Ko‘paytirish (×)":
            result = a * b
            formula = f"{a} × {b}"

        elif operation == "Bo‘lish (÷)":
            if b == 0:
                st.error("Nolga bo‘lish mumkin emas!")
                st.stop()
            result = a / b
            formula = f"{a} ÷ {b}"

        elif operation == "Foiz (%)":
            result = a * b / 100
            formula = f"{a} ning {b}% i"

        elif operation == "Darajaga ko‘tarish (^)":
            result = a ** b
            formula = f"{a} ^ {b}"

        else:
            if a < 0:
                st.error("Manfiy sonning haqiqiy kvadrat ildizi mavjud emas!")
                st.stop()
            result = math.sqrt(a)
            formula = f"√{a}"

        st.success(f"Natija: {result:g}")

        st.session_state.history.insert(
            0, f"{formula} = {result:g}"
        )

    except OverflowError:
        st.error("Hisoblash natijasi juda katta!")
    except Exception as e:
        st.error(f"Xatolik: {e}")

# Tarix
st.markdown("---")
st.subheader("📜 Hisoblash tarixi")

if st.session_state.history:
    for item in st.session_state.history:
        st.write("🔹", item)

    if st.button("🗑 Tarixni tozalash"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("Hozircha hisoblash tarixi mavjud emas.")

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#65e6ff'>"
    "PRO CALCULATOR | Created with Python & Streamlit"
    "</p>",
    unsafe_allow_html=True
)
