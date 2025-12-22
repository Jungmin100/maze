import streamlit as st
from PIL import Image, ImageDraw
import json

# =========================
# 설정
# =========================
IMAGE_PATH = "maze.png"
PLAYER_RADIUS = 4

st.set_page_config(page_title="미로 게임", layout="centered")
st.title("🌀 미로 탈출 게임 (마우스 드래그)")

# =========================
# 이미지 로드
# =========================
maze_img = Image.open(IMAGE_PATH).convert("RGB")
width, height = maze_img.size
pixels = maze_img.load()

# =========================
# 시작 위치 (맨 위)
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
# 마우스 위치 받기 (JS)
# =========================
mouse = st.components.v1.html(
    f"""
    <script>
    const sendPos = (e) => {{
        const rect = e.target.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        window.parent.postMessage({{x, y}}, "*");
    }};
    </script>
    <div style="width:{width}px;height:{height}px"
         onmousemove="sendPos(event)">
    </div>
    """,
    height=0,
)

# =========================
# 플레이어 표시
# =========================
img = maze_img.copy()
draw = ImageDraw.Draw(img)
draw.ellipse(
    (
        st.session_state.x - PLAYER_RADIUS,
        st.session_state.y - PLAYER_RADIUS,
        st.session_state.x + PLAYER_RADIUS,
        st.session_state.y + PLAYER_RADIUS,
    ),
    fill="red",
)

st.image(img, use_container_width=True)

# =========================
# 리셋
# =========================
if st.button("처음부터"):
    st.session_state.x = width // 2
    st.session_state.y = 8
