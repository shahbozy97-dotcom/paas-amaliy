import streamlit as st
import time
from datetime import datetime

st.set_page_config(
    page_title="Digital Clock",
    page_icon="🕒",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10172a, #253b65);
}
.clock {
    text-align: center;
    color: white;
    padding: 45px 10px;
    border-radius: 25px;
    background: rgba(255,255,255,0.08);
    margin-top: 50px;
}
.time {
    font-size: 75px;
    font-weight: bold;
    color: #65e6ff;
}
.date {
    font-size: 24px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:white'>🕒 DIGITAL CLOCK</h1>", unsafe_allow_html=True)

clock = st.empty()

while True:
    now = datetime.now()

    clock.markdown(f"""
    <div class="clock">
        <div class="time">{now.strftime("%H:%M:%S")}</div>
        <div class="date">{now.strftime("%d-%m-%Y")}</div>
        <div class="date">{now.strftime("%A")}</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1)
