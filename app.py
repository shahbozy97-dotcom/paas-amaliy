
import streamlit as st
import random

st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #183b35);
}
h1 {
    text-align: center;
    color: #70ff9b;
}
div.stButton > button {
    height: 55px;
    font-size: 22px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🐍 SNAKE GAME</h1>", unsafe_allow_html=True)
st.caption("Olmani yig‘ing va rekordni yangilang!")

SIZE = 10

if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.food = (2, 7)
    st.session_state.score = 0
    st.session_state.best = 0
    st.session_state.over = False
    st.session_state.direction = "RIGHT"

def new_food(snake):
    cells = [
        (r, c)
        for r in range(SIZE)
        for c in range(SIZE)
        if (r, c) not in snake
    ]
    return random.choice(cells) if cells else None

def reset_game():
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.food = new_food(st.session_state.snake)
    st.session_state.score = 0
    st.session_state.over = False
    st.session_state.direction = "RIGHT"

def move(direction):
    if st.session_state.over:
        return

    snake = st.session_state.snake
    head_r, head_c = snake[0]

    directions = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }

    opposite = {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT"
    }

    if direction == opposite[st.session_state.direction] and len(snake) > 1:
        return

    st.session_state.direction = direction
    dr, dc = directions[direction]
    new_head = (head_r + dr, head_c + dc)

    ate = new_head == st.session_state.food
    body = snake if ate else snake[:-1]

    if (
        new_head[0] < 0 or new_head[0] >= SIZE
        or new_head[1] < 0 or new_head[1] >= SIZE
        or new_head in body
    ):
        st.session_state.over = True
        st.session_state.best = max(
            st.session_state.best,
            st.session_state.score
        )
        return

    st.session_state.snake = [new_head] + body

    if ate:
        st.session_state.score += 1
        st.session_state.best = max(
            st.session_state.best,
            st.session_state.score
        )
        st.session_state.food = new_food(st.session_state.snake)

def draw_board():
    snake = st.session_state.snake
    food = st.session_state.food

    board = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            pos = (r, c)

            if pos == snake[0]:
                row.append("🟢")
            elif pos in snake:
                row.append("🟩")
            elif pos == food:
                row.append("🍎")
            else:
                row.append("⬛")

        board.append(row)

    html = """
    <div style="display:grid;grid-template-columns:repeat(10,1fr);
    gap:3px;background:#0b1720;padding:8px;border-radius:12px;">
    """

    for row in board:
        for cell in row:
            html += f"""
            <div style="aspect-ratio:1;background:#1c3440;
            display:flex;align-items:center;justify-content:center;
            font-size:clamp(12px,3vw,22px);border-radius:4px;">
            {cell}
            </div>
            """

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.metric("🍎 Ball", st.session_state.score)
col2.metric("🏆 Rekord", st.session_state.best)

draw_board()

if st.session_state.over:
    st.error("💀 O‘YIN TUGADI!")
    st.warning(f"Sizning natijangiz: {st.session_state.score}")

st.markdown("### 🎮 Boshqaruv")

up = st.columns([1, 1, 1])
with up[1]:
    if st.button("⬆️", use_container_width=True):
        move("UP")

left, center, right = st.columns(3)

with left:
    if st.button("⬅️", use_container_width=True):
        move("LEFT")

with center:
    if st.button("⬇️", use_container_width=True):
        move("DOWN")

with right:
    if st.button("➡️", use_container_width=True):
        move("RIGHT")

if st.button("🔄 QAYTA BOSHLASH", use_container_width=True):
    reset_game()

st.caption("Ilonni tugmalar yordamida harakatlantiring.")
