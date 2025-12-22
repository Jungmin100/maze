import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# =========================
# 기본 설정
# =========================
IMAGE_PATH = "maze.png"
PLAYER_RADIUS = 4   # 🔴 공 크기 줄임

st.set_page_config(page_title="미로 게임", layout="centered")
st.title("🌀 미로 탈출 게임 (드래그 방식)")

# =========================
# 이미지 로드
# =========================
maze_img = Image.open(IMAGE_PATH).convert("RGB")
width, height = maze_img.size
pixels = maze_img.load()

# =========================
# 세션 상태 (맨 위 시작)
# =========================
if "x" not in st.session_state:
    st.session_state.x = width // 2
    st.session_state.y = 10   # ⬆️ 맨 위에서 시작

# =========================
# 이동 가능 판정
# =========================
def can_move(x, y):
    if x < 0 or y < 0 or x >= width or y >= height:
        return False
    r, g, b = pixels[int(x), int(y)]
    return r > 200 and g > 200 and b > 200  # 흰색만 허용

# =========================
# Canvas (마우스 드래그)
# =========================
canvas = st_canvas(
    fill_color="rgba(255, 0, 0, 0.0)",
    stroke_width=1,
    stroke_color="red",
    background_image=maze_img,
    update_streamlit=True,
    height=height,
    width=width,
    drawing_mode="point",
    key="canvas",
)

# =========================
# 드래그 위치 처리
# =========================
if canvas.json_data and "objects" in canvas.json_data:
    if len(canvas.json_data["objects"]) > 0:
        obj = canvas.json_data["objects"][-1]
        new_x = obj["left"]
        new_y = obj["top"]

        if can_move(new_x, new_y):
            st.session_state.x = new_x
            st.session_state.y = new_y

# =========================
# 플레이어 표시
# =========================
overlay = maze_img.copy()
overlay_pixels = overlay.load()

for dx in range(-PLAYER_RADIUS, PLAYER_RADIUS + 1):
    for dy in range(-PLAYER_RADIUS, PLAYER_RADIUS + 1):
        px = int(st.session_state.x + dx)
        py = int(st.session_state.y + dy)
        if 0 <= px < width and 0 <= py < height:
            overlay_pixels[px, py] = (255, 0, 0)

st.image(overlay, use_container_width=True)

# =========================
# 리셋
# =========================
if st.button("처음부터 다시"):
    st.session_state.x = width // 2
    st.session_state.y = 10
