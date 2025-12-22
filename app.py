import streamlit as st
from PIL import Image, ImageDraw

# =========================
# 기본 설정
# =========================
IMAGE_PATH = "maze.png"
STEP = 5                 # 이동 속도 (픽셀)
PLAYER_RADIUS = 6

# =========================
# 이미지 로드
# =========================
maze_img = Image.open(IMAGE_PATH).convert("RGB")
width, height = maze_img.size
pixels = maze_img.load()

# =========================
# 세션 상태 초기화
# =========================
if "x" not in st.session_state:
    st.session_state.x = width // 2
    st.session_state.y = height - 20

# =========================
# 이동 가능 여부
# =========================
def can_move(x, y):
    if x < 0 or y < 0 or x >= width or y >= height:
        return False
    r, g, b = pixels[x, y]
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
# UI
# =========================
st.set_page_config(page_title="미로 게임", layout="centered")
st.title("🌀 미로 탈출 게임")

# 플레이어 표시
display_img = maze_img.copy()
draw = ImageDraw.Draw(display_img)
draw.ellipse(
    (
        st.session_state.x - PLAYER_RADIUS,
        st.session_state.y - PLAYER_RADIUS,
        st.session_state.x + PLAYER_RADIUS,
        st.session_state.y + PLAYER_RADIUS,
    ),
    fill="red"
)

st.image(display_img, use_container_width=True)

# =========================
# 컨트롤 버튼
# =========================
col1, col2, col3 = st.columns(3)

with col2:
    if st.button("↑"):
        move(0, -STEP)

with col1:
    if st.button("←"):
        move(-STEP, 0)

with col3:
    if st.button("→"):
        move(STEP, 0)

with col2:
    if st.button("↓"):
        move(0, STEP)

# =========================
# 리셋
# =========================
if st.button("처음 위치로"):
    st.session_state.x = width // 2
    st.session_state.y = height - 20

