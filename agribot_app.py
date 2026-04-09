import streamlit as st
import time
import random
from collections import deque

st.set_page_config(page_title="Autonomous Agri-Bot Simulator", page_icon="🤖", layout="wide")

GRID_COLS = 15
GRID_ROWS = 10

EMPTY = 0
OBSTACLE = 1
CROP = 2
VISITED = 3

OBSTACLES = [(2,3),(2,4),(5,1),(5,2),(8,5),(8,6),(11,2),(11,3),(13,6),(13,7),(3,8),(7,9),(10,7)]
CROPS =     [(1,1),(3,1),(6,3),(9,1),(12,1),(14,1),(1,8),(4,8),(7,8),(10,8),(13,8),(14,5),(12,3)]

DIRS = [(1,0),(0,1),(-1,0),(0,-1)]
DIR_LABELS = {"(1, 0)": "→ East", "(0, 1)": "↓ South", "(-1, 0)": "← West", "(0, -1)": "↑ North"}

def init_grid():
    grid = [[EMPTY]*GRID_COLS for _ in range(GRID_ROWS)]
    for x, y in OBSTACLES:
        if 0 <= y < GRID_ROWS and 0 <= x < GRID_COLS:
            grid[y][x] = OBSTACLE
    for x, y in CROPS:
        if 0 <= y < GRID_ROWS and 0 <= x < GRID_COLS:
            grid[y][x] = CROP
    return grid

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    open_list = [(0, start, [])]
    visited = set()
    while open_list:
        open_list.sort(key=lambda x: x[0])
        cost, curr, path = open_list.pop(0)
        if curr in visited:
            continue
        visited.add(curr)
        path = path + [curr]
        if curr == goal:
            return path
        for dx, dy in DIRS:
            nx, ny = curr[0]+dx, curr[1]+dy
            if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                if grid[ny][nx] != OBSTACLE and (nx,ny) not in visited:
                    g = len(path)
                    h = heuristic((nx,ny), goal)
                    open_list.append((g+h, (nx,ny), path))
    return None

def find_nearest_crop(grid, bot):
    best, best_dist = None, float('inf')
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            if grid[y][x] == CROP:
                d = heuristic(bot, (x,y))
                if d < best_dist:
                    best_dist = d
                    best = (x, y)
    return best

def render_grid(grid, bot, path_set):
    CELL = {
        EMPTY:    "⬜",
        OBSTACLE: "🪨",
        CROP:     "🌾",
        VISITED:  "🟩",
    }
    lines = []
    for y in range(GRID_ROWS):
        row = ""
        for x in range(GRID_COLS):
            if (x, y) == bot:
                row += "🤖"
            elif (x, y) in path_set:
                row += "🟦"
            else:
                row += CELL.get(grid[y][x], "⬜")
        lines.append(row)
    return "\n".join(lines)

def get_sensors(grid, bot):
    readings = {}
    for dx, dy in DIRS:
        nx, ny = bot[0]+dx, bot[1]+dy
        label = DIR_LABELS[str((dx,dy))]
        in_bounds = 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS
        blocked = not in_bounds or grid[ny][nx] == OBSTACLE
        readings[label] = blocked
    return readings

# ── State init ──────────────────────────────────────────────
if "grid" not in st.session_state:
    st.session_state.grid = init_grid()
    st.session_state.bot = (0, 0)
    st.session_state.path = []
    st.session_state.path_idx = 0
    st.session_state.crops_collected = 0
    st.session_state.obstacles_avoided = 0
    st.session_state.visited = {(0,0)}
    st.session_state.log = ["System ready. Press ▶ START to begin."]
    st.session_state.running = False
    st.session_state.mission = "idle"

def add_log(msg):
    ts = time.strftime("%H:%M:%S")
    st.session_state.log = [f"[{ts}] {msg}"] + st.session_state.log[:12]

def plan_path():
    target = find_nearest_crop(st.session_state.grid, st.session_state.bot)
    if not target:
        add_log("✅ All crops harvested! Mission complete.")
        st.session_state.mission = "complete"
        st.session_state.running = False
        return
    p = astar(st.session_state.grid, st.session_state.bot, target)
    if p:
        st.session_state.path = p
        st.session_state.path_idx = 1
        add_log(f"Navigating to crop at {target} — {len(p)} steps")
    else:
        add_log(f"⚠ No path to {target} — blocked")
        st.session_state.mission = "stuck"
        st.session_state.running = False

def step_bot():
    if st.session_state.path_idx >= len(st.session_state.path):
        plan_path()
        return
    next_pos = st.session_state.path[st.session_state.path_idx]
    sensors = get_sensors(st.session_state.grid, st.session_state.bot)
    st.session_state.obstacles_avoided += sum(sensors.values()) * 0.25
    x, y = next_pos
    st.session_state.bot = next_pos
    st.session_state.visited.add(next_pos)
    if st.session_state.grid[y][x] == CROP:
        st.session_state.grid[y][x] = VISITED
        st.session_state.crops_collected += 1
        add_log(f"🌾 Crop harvested at {next_pos}")
        st.session_state.path_idx += 1
        plan_path()
    else:
        if st.session_state.grid[y][x] == EMPTY:
            st.session_state.grid[y][x] = VISITED
        st.session_state.path_idx += 1

def reset_all():
    for key in ["grid","bot","path","path_idx","crops_collected","obstacles_avoided","visited","log","running","mission"]:
        if key in st.session_state:
            del st.session_state[key]

# ── UI ───────────────────────────────────────────────────────
st.markdown("""
<style>
.metric-box {background:#0f2620;border:1px solid #1a4a33;border-radius:10px;padding:12px 16px;text-align:center;}
.metric-label {font-size:11px;color:#4b8c6a;text-transform:uppercase;letter-spacing:0.1em;}
.metric-value {font-size:24px;font-weight:600;color:#4ade80;}
.log-box {background:#050d08;border:1px solid #0f2620;border-radius:8px;padding:12px;font-family:monospace;font-size:11px;max-height:180px;overflow-y:auto;}
.sensor-clear {background:#052010;border:1px solid #1a4a33;border-radius:8px;padding:8px 12px;color:#4ade80;font-size:12px;}
.sensor-blocked {background:#1a0808;border:1px solid #4a1a1a;border-radius:8px;padding:8px 12px;color:#f87171;font-size:12px;}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🤖 Autonomous Agri-Bot Simulator")
st.markdown("*Obstacle avoidance · A\\* pathfinding · Sensor array · Built by Asiya Sabiu Sulaiman*")
st.divider()

# Controls
col_a, col_b, col_c = st.columns([1,1,4])
with col_a:
    if st.session_state.mission in ("idle", "complete"):
        if st.button("▶ START", use_container_width=True):
            reset_all()
            time.sleep(0.05)
            st.session_state.grid = init_grid()
            st.session_state.bot = (0,0)
            st.session_state.path = []
            st.session_state.path_idx = 0
            st.session_state.crops_collected = 0
            st.session_state.obstacles_avoided = 0
            st.session_state.visited = {(0,0)}
            st.session_state.log = ["Agri-Bot initialised. Beginning field survey..."]
            st.session_state.running = True
            st.session_state.mission = "running"
            plan_path()
            st.rerun()
    elif st.session_state.running:
        if st.button("⏸ PAUSE", use_container_width=True):
            st.session_state.running = False
            add_log("Navigation paused.")
            st.rerun()
    else:
        if st.button("▶ RESUME", use_container_width=True):
            st.session_state.running = True
            add_log("Navigation resumed.")
            st.rerun()

with col_b:
    if st.button("↺ RESET", use_container_width=True):
        reset_all()
        st.rerun()

# Stats
total_crops = sum(1 for x,y in CROPS if 0<=y<GRID_ROWS and 0<=x<GRID_COLS)
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.metric("🌾 Crops Harvested", f"{st.session_state.get('crops_collected',0)} / {total_crops}")
with s2:
    st.metric("🪨 Obstacles Avoided", int(st.session_state.get('obstacles_avoided',0)))
with s3:
    st.metric("🗺 Cells Explored", len(st.session_state.get('visited', set())))
with s4:
    status = st.session_state.get('mission','idle').upper()
    st.metric("📡 Mission Status", status)

st.divider()

# Main layout
grid_col, panel_col = st.columns([2, 1])

with grid_col:
    path_set = set()
    if st.session_state.path:
        idx = st.session_state.path_idx
        path_set = set(tuple(p) for p in st.session_state.path[idx:idx+6])

    grid_display = render_grid(st.session_state.grid, st.session_state.bot, path_set)
    st.code(grid_display, language=None)

    st.caption("🤖 Bot &nbsp;&nbsp; 🌾 Crop &nbsp;&nbsp; 🪨 Obstacle &nbsp;&nbsp; 🟩 Explored &nbsp;&nbsp; 🟦 Planned path")

with panel_col:
    st.markdown("#### 📡 Sensor Array")
    sensors = get_sensors(st.session_state.grid, st.session_state.bot)
    sc1, sc2 = st.columns(2)
    items = list(sensors.items())
    for i, (label, blocked) in enumerate(items):
        col = sc1 if i % 2 == 0 else sc2
        with col:
            if blocked:
                st.error(f"{label}\n**BLOCKED**")
            else:
                st.success(f"{label}\n**CLEAR**")

    st.markdown("#### 🛰 Telemetry")
    bot = st.session_state.bot
    path_remaining = max(0, len(st.session_state.path) - st.session_state.path_idx)
    st.markdown(f"""
| Parameter | Value |
|---|---|
| Position | `{bot}` |
| Path remaining | `{path_remaining} steps` |
| Algorithm | `A* Search` |
| Update rate | `~2 Hz` |
""")

    st.markdown("#### 🖥 System Log")
    log_text = "\n".join(st.session_state.log)
    st.code(log_text, language=None)

    st.info("**Hardware equivalent:** This simulation mirrors an Arduino/Raspberry Pi Agri-Bot — ultrasonic sensors → GPIO pins → motor driver → wheel control. The A\\* logic here runs as C++ on Arduino or Python on Raspberry Pi.")

# Auto-step
if st.session_state.get("running") and st.session_state.get("mission") == "running":
    step_bot()
    time.sleep(0.4)
    st.rerun()
