
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #0b1220;
}
header, footer {
    visibility: hidden;
}
.block-container {
    padding-top: 1rem;
    max-width: 1000px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center;color:#55f59a;">
🐍 SNAKE ARENA
</h1>
<p style="text-align:center;color:#b8c7d9;">
Olmalarni yig‘ing, rekordni yangilang!
</p>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: transparent;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
}
.panel {
    max-width: 600px;
    margin: auto;
    padding: 15px;
    background: #142238;
    border: 1px solid #29425e;
    border-radius: 20px;
}
.stats {
    display: flex;
    justify-content: space-around;
    gap: 10px;
    margin-bottom: 14px;
}
.stat {
    flex: 1;
    background: #0b1728;
    border-radius: 12px;
    padding: 12px;
}
.stat span {
    display: block;
    color: #8ca6c5;
    font-size: 13px;
}
.stat b {
    display: block;
    color: #62f5a0;
    font-size: 25px;
    margin-top: 5px;
}
canvas {
    width: 100%;
    max-width: 480px;
    aspect-ratio: 1;
    background: #091522;
    border: 3px solid #31516c;
    border-radius: 12px;
    display: block;
    margin: auto;
}
.controls {
    margin-top: 15px;
    display: grid;
    grid-template-columns: repeat(3, 65px);
    justify-content: center;
    gap: 7px;
}
button {
    border: 0;
    border-radius: 12px;
    padding: 13px;
    font-size: 19px;
    font-weight: bold;
    color: white;
    background: #24506a;
    cursor: pointer;
}
button:hover { background: #327c78; }
.empty { visibility: hidden; }
.actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 14px;
}
.actions button {
    font-size: 14px;
    padding: 12px 18px;
}
.start { background: #16864e; }
.pause { background: #a36b19; }
.reset { background: #a33b4c; }
.help {
    color: #9db2c9;
    font-size: 13px;
    margin-top: 12px;
}
#message {
    color: #66f3a0;
    font-weight: bold;
    min-height: 24px;
    margin-top: 10px;
}
</style>
</head>
<body>
<div class="panel">
    <div class="stats">
        <div class="stat">
            <span>🍎 BALL</span>
            <b id="score">0</b>
        </div>
        <div class="stat">
            <span>🏆 REKORD</span>
            <b id="best">0</b>
        </div>
        <div class="stat">
            <span>⚡ TEZLIK</span>
            <b id="speed">1</b>
        </div>
    </div>

    <canvas id="game" width="480" height="480"></canvas>

    <div id="message">Boshlash tugmasini bosing!</div>

    <div class="controls">
        <button class="empty"> </button>
        <button data-dir="up">⬆️</button>
        <button class="empty"> </button>
        <button data-dir="left">⬅️</button>
        <button data-dir="down">⬇️</button>
        <button data-dir="right">➡️</button>
    </div>

    <div class="actions">
        <button class="start" id="start">▶ BOSHLASH</button>
        <button class="pause" id="pause">⏸ PAUZA</button>
        <button class="reset" id="reset">🔄 QAYTA</button>
    </div>

    <div class="help">
        Klaviatura: ↑ ↓ ← → yoki W A S D<br>
        Olmani yeng va devorga tegmang!
    </div>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const N = 20;
const CELL = canvas.width / N;

let snake, food, direction, nextDirection;
let score = 0;
let best = 0;
let running = false;
let gameOver = false;
let timer = null;
let speed = 150;

const scoreEl = document.getElementById("score");
const bestEl = document.getElementById("best");
const speedEl = document.getElementById("speed");
const message = document.getElementById("message");

try {
    best = Number(localStorage.getItem("snakeBest") || 0);
} catch(e) {}
bestEl.textContent = best;

function reset() {
    clearInterval(timer);
    snake = [
        {x: 10, y: 10},
        {x: 9, y: 10},
        {x: 8, y: 10}
    ];
    direction = "right";
    nextDirection = "right";
    score = 0;
    speed = 150;
    running = false;
    gameOver = false;
    placeFood();
    updateStats();
    message.textContent = "Boshlash tugmasini bosing!";
    draw();
}

function placeFood() {
    do {
        food = {
            x: Math.floor(Math.random() * N),
            y: Math.floor(Math.random() * N)
        };
    } while (snake.some(p => p.x === food.x && p.y === food.y));
}

function updateStats() {
    scoreEl.textContent = score;
    bestEl.textContent = best;
    speedEl.textContent = Math.max(1, Math.floor((150-speed)/15)+1);
}

function setDirection(d) {
    const opposite = {
        up: "down",
        down: "up",
        left: "right",
        right: "left"
    };
    if (d !== opposite[direction]) {
        nextDirection = d;
    }
}

function start() {
    if (gameOver) reset();
    if (running) return;

    running = true;
    message.textContent = "O‘yin boshlandi! Omad!";
    clearInterval(timer);
    timer = setInterval(tick, speed);
}

function pause() {
    if (!running) return;
    running = false;
    clearInterval(timer);
    message.textContent = "⏸ O‘yin pauzada";
}

function tick() {
    direction = nextDirection;
    const head = {...snake[0]};

    if (direction === "up") head.y--;
    if (direction === "down") head.y++;
    if (direction === "left") head.x--;
    if (direction === "right") head.x++;

    const ate = head.x === food.x && head.y === food.y;

    if (
        head.x < 0 || head.x >= N ||
        head.y < 0 || head.y >= N ||
        snake.slice(0, ate ? snake.length : -1)
             .some(p => p.x === head.x && p.y === head.y)
    ) {
        endGame();
        return;
    }

    snake.unshift(head);

    if (ate) {
        score++;
        if (score > best) {
            best = score;
            try {
                localStorage.setItem("snakeBest", best);
            } catch(e) {}
        }
        placeFood();

        const newSpeed = Math.max(65, 150 - score * 5);
        if (newSpeed !== speed) {
            speed = newSpeed;
            clearInterval(timer);
            timer = setInterval(tick, speed);
        }
    } else {
        snake.pop();
    }

    updateStats();
    draw();
}

function endGame() {
    running = false;
    gameOver = true;
    clearInterval(timer);
    message.textContent = "💀 O‘YIN TUGADI! Qayta boshlashni bosing.";
    draw();
}

function draw() {
    ctx.fillStyle = "#091522";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Kataklar
    ctx.strokeStyle = "#142b3c";
    ctx.lineWidth = 1;
    for (let i = 0; i <= N; i++) {
        ctx.beginPath();
        ctx.moveTo(i * CELL, 0);
        ctx.lineTo(i * CELL, canvas.height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, i * CELL);
        ctx.lineTo(canvas.width, i * CELL);
        ctx.stroke();
    }

    // Olma
    ctx.font = `${CELL * 0.8}px Arial`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(
        "🍎",
        food.x * CELL + CELL/2,
        food.y * CELL + CELL/2
    );

    // Ilon
    snake.forEach((p, i) => {
        const pad = 2;
        ctx.fillStyle = i === 0 ? "#7dff9c" : "#21bd70";
        ctx.beginPath();
        ctx.roundRect(
            p.x * CELL + pad,
            p.y * CELL + pad,
            CELL - pad*2,
            CELL - pad*2,
            6
        );
        ctx.fill();
    });

    // O‘yin tugaganda qatlam
    if (gameOver) {
        ctx.fillStyle = "rgba(0,0,0,0.55)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "white";
        ctx.font = "bold 30px Arial";
        ctx.fillText("GAME OVER", canvas.width/2, canvas.height/2);
    }
}

document.addEventListener("keydown", e => {
    const keys = {
        ArrowUp: "up", w: "up", W: "up",
        ArrowDown: "down", s: "down", S: "down",
        ArrowLeft: "left", a: "left", A: "left",
        ArrowRight: "right", d: "right", D: "right"
    };

    if (keys[e.key]) {
        e.preventDefault();
        setDirection(keys[e.key]);
    }

    if (e.key === " " && running) pause();
    else if (e.key === " " && !running && !gameOver) start();
});

document.querySelectorAll("[data-dir]").forEach(btn => {
    btn.addEventListener("click", () => {
        setDirection(btn.dataset.dir);
    });
});

document.getElementById("start").addEventListener("click", start);
document.getElementById("pause").addEventListener("click", pause);
document.getElementById("reset").addEventListener("click", reset);

reset();
</script>
</body>
</html>
"""

components.html(game_html, height=790, scrolling=False)
