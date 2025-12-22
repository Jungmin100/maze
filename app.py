import streamlit as st
from PIL import Image, ImageDraw

# =========================
# 설정
# =========================
IMAGE_PATH = "maze.png"
STEP = 4
PLAYER_RADIUS = 2

st.set_page_config(page_title="미로 게임", layout="centered")
st.title("🌀 미로 탈출 게임 (키보드 조작)")
st.caption("W / A / S / D 키로 이동하세요")

# =========================
# 이미지 로드
# =========================
maze_img = Image.open(IMAGE_PATH).convert("RGB")
width, height = maze_img.size
pixels = maze_img.load()

# =========================
# 시작 위치 (맨 위 중앙)
# =========================
if "x" not in st.session_state:
    st.session_state.x = width // 2
    st.session_state.y = 8

# =========================
# 이동 가능 판정
# =========================
def can_move(x, y):
    if x < 0 or y < 0 or x >= width or y >= height:
        return False
    r, g, b = pixels[int(x), int(y)]
    return r > 200 and g > 200 and b > 200

# =========================
# 이동 처리
# =========================
def move(dx, dy):
    nx = st.session_state.x + dx
    ny = st.session_state.y + dy
    if can_move(nx, ny):
        st.session_state.x = nx
        st.session_state.y = ny

# =========================
# 키보드 입력 (핵심 수정)
# =========================
key_input = st.text_input(
    "키 입력 (클릭 후 W/A/S/D)",
    key="key_input",
)

if key_input:
    last = key_input[-1].lower()

    if last == "w":
        move(0, -STEP)
    elif last == "s":
        move(0, STEP)
    elif last == "a":
        move(-STEP, 0)
    elif last == "d":
        move(STEP, 0)

# =========================
# 플레이어 표시
# =========================
display_img = maze_img.copy()
draw = ImageDraw.Draw(display_img)
draw.ellipse(
    (
        st.session_state.x - PLAYER_RADIUS,
        st.session_state.y - PLAYER_RADIUS,
        st.session_state.x + PLAYER_RADIUS,
        st.session_state.y + PLAYER_RADIUS,
    ),
    fill="red",
)

st.image(display_img, use_container_width=True)

# =========================
# 리셋
# =========================
if st.button("처음부터"):
    st.session_state.x = width // 2
    st.session_state.y = 8
