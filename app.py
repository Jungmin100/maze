import streamlit as st
from PIL import Image, ImageDraw

# =========================
# 설정
# =========================
IMAGE_PATH = "maze.png"
STEP = 4                 # 이동 속도 (픽셀)
PLAYER_RADIUS = 2        # 🔴 빨간 점 크기 (아주 작게)

st.set_page_config(page_title="미로 게임", layout="centered")
st.title("🌀 미로 탈출 게임")

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
    st.session_state.y = 8   # 맨 위

# =========================
# 이동 가능 판정
# =========================
def can_move(x, y):
    if x < 0 or y < 0 or x >= width or y >= height:
        return False
    r, g, b = pixels[int(x), int(y)]
    return r > 200 and g > 200 and b > 200  # 흰색만 이동 가능

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
# 이동 버튼 UI
# =========================
c1, c2, c3 = st.columns(3)

with c2:
    st.button("↑", on_click=move, args=(0, -STEP))

with c1:
    st.button("←", on_click=move, args=(-STEP, 0))

with c3:
    st.button("→", on_click=move, args=(STEP, 0))

with c2:
    st.button("↓", on_click=move, args=(0, STEP))

# =========================
# 리셋
# =========================
if st.button("처음부터"):
    st.session_state.x = width // 2
    st.session_state.y = 8
