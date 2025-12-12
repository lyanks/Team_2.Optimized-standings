import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math
import pandas as pd
import os

# ==========================================
# CUSTOM CSS & CONFIG (STYLING)
# ==========================================
st.set_page_config(
    page_title="Tournament PageRank",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #4CAF50; }
    .stButton>button {
        width: 100%; border-radius: 10px; background-color: #262730;
        color: white; border: 1px solid #4a4a4a; transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #4CAF50; color: white; border-color: #4CAF50;
    }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOGIC (PAGERANK & LAYOUT)
# ==========================================

@st.cache_data 
def calculate_pagerank(matches_data, teams_tuple, damping=0.85, epsilon=1e-8):
    """
    Розраховує PageRank (while loop convergence).
    Адаптовано під вхідний формат списку кортежів (Winner, Loser).
    """
    teams = list(teams_tuple)
    n = len(teams)
    if n == 0: return {}

    # --- ПІДГОТОВКА ДАНИХ (Адаптація під твій код) ---
    # Перетворюємо список [(Winner, Loser)] -> {Loser: {Winners...}}
    matches_dict = {}
    for w, l in matches_data:
        if l not in matches_dict:
            matches_dict[l] = set()
        matches_dict[l].add(w)
    
    # --- ТВІЙ АЛГОРИТМ ---
    teams_list = list(teams)
    team_idx = {t: i for i, t in enumerate(teams_list)}

    # Ініціалізація рівномірно
    scores = np.ones(n) / n

    # Рахуємо out_degree (скільки разів команда програла)
    out_degree = {t: 0 for t in teams}
    for loser, winners in matches_dict.items():
        out_degree[loser] = len(winners)

    # PageRank ітерації
    while True:
        new_scores = np.ones(n) * (1 - damping) / n

        for loser, winners in matches_dict.items():
            if out_degree[loser] > 0:
                loser_idx = team_idx[loser]
                contribution = damping * scores[loser_idx] / out_degree[loser]

                for winner in winners:
                    winner_idx = team_idx[winner]
                    new_scores[winner_idx] += contribution

        # Для команд без поразок (dangling nodes) - розподіляємо рівномірно
        dangling_sum = 0
        for t in teams:
            # Якщо команда нікому не програла, вона "dangling" в контексті loser->winner графа
            if t not in matches_dict or len(matches_dict.get(t, set())) == 0:
                dangling_sum += scores[team_idx[t]]

        new_scores += damping * dangling_sum / n

        delta = np.sum(np.abs(new_scores - scores))
        scores = new_scores

        if delta < epsilon:
            break

    # Нормалізуємо (про всяк випадок)
    scores = scores / scores.sum()

    return {teams_list[i]: scores[i] for i in range(n)}

@st.cache_data
def get_layout(scores, radii):
    sorted_teams = sorted(scores.keys(), key=lambda t: scores[t], reverse=True)
    n = len(sorted_teams)
    if n == 0: return {}
    
    max_r = max(radii.values()) if radii else 30
    R = max(100, n * max_r * 0.7)
    
    pos = {}
    for i, team in enumerate(sorted_teams):
        theta = 2 * math.pi * i / n - math.pi / 2
        pos[team] = np.array([R * math.cos(theta), R * math.sin(theta)])
        
    return pos

# ==========================================
# PLOTLY GRAPH
# ==========================================

def create_stylish_graph(scores, matches, pos, radii):
    fig = go.Figure()
    
    # Edges
    edge_x, edge_y = [], []
    for w, l in matches:
        if w in pos and l in pos:
            p1, p2 = pos[w], pos[l]
            edge_x.extend([p1[0], p2[0], None])
            edge_y.extend([p1[1], p2[1], None])
            
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(color='#444', width=1),
        hoverinfo='none',
        opacity=0.5
    ))
    
    # Nodes
    node_x, node_y, node_text, node_size, node_color = [], [], [], [], []
    
    for team, score in scores.items():
        p = pos[team]
        node_x.append(p[0])
        node_y.append(p[1])
        node_text.append(f"<b>{team}</b><br>Score: {score:.4f}")
        node_size.append(radii[team] * 2.2)
        node_color.append(score)

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(
            size=node_size,
            color=node_color,
            colorscale='Viridis',
            showscale=False,
            line=dict(color='white', width=1.5)
        ),
        text=list(scores.keys()),
        textposition="middle center",
        textfont=dict(size=12, color='white', family="Arial"),
        hovertext=node_text,
        hoverinfo='text'
    ))

    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False),
        height=650,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        dragmode='pan'
    )
    return fig

# ==========================================
# MAIN APP & DATA LOADING
# ==========================================

# --- STATE MANAGEMENT UTILS ---
def increment_idx():
    if st.session_state.idx < st.session_state.max_matches:
        st.session_state.idx += 1

def decrement_idx():
    if st.session_state.idx > 1:
        st.session_state.idx -= 1

def start_idx():
    st.session_state.idx = 1

def end_idx():
    st.session_state.idx = st.session_state.max_matches

# --- SIDEBAR & DATA LOADING LOGIC ---
with st.sidebar:
    st.title("🏆 Setup")
    
    # 1. Docker Env Loading
    target_filename = os.getenv("CSV_FILENAME")
    data_folder = "/app/data"
    auto_df = None
    
    if target_filename:
        file_path = os.path.join(data_folder, target_filename)
        if os.path.exists(file_path):
            try:
                auto_df = pd.read_csv(file_path)
                st.success(f"Loaded: {target_filename}")
            except Exception as e:
                st.error(f"Error loading {target_filename}: {e}")
    
    # 2. Manual Upload
    uploaded_file = None
    if auto_df is None:
        uploaded_file = st.file_uploader("Upload Match CSV", type=['csv'])
    
    st.markdown("---")
    st.markdown("**Controls:** Use buttons to replay.")
    st.info("Built with Streamlit & Plotly")

# --- DATA SOURCE DECISION ---
df = None
if auto_df is not None:
    df = auto_df
elif uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")

# --- MAIN CONTENT ---
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("Tournament PageRank Analytics")

if df is not None:
    if len(df.columns) >= 2:
        raw_matches = list(zip(df.iloc[:, 0].astype(str), df.iloc[:, 1].astype(str)))
    else:
        st.error("CSV must have at least 2 columns")
        st.stop()
    
    total_matches = len(raw_matches)
    
    # State Init
    data_hash = hash(tuple(raw_matches))
    if 'last_hash' not in st.session_state or st.session_state.last_hash != data_hash:
        st.session_state.last_hash = data_hash
        st.session_state.idx = 1 
        
    st.session_state.max_matches = total_matches

    # --- CONTROLS ---
    st.markdown("### 🎮 Replay Control")
    st.slider("Match Progress", 1, total_matches, key="idx")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("⏪ Start", on_click=start_idx)
    with c2: st.button("◀ Prev", on_click=decrement_idx)
    with c3: st.button("Next ▶", on_click=increment_idx)
    with c4: st.button("End ⏩", on_click=end_idx)

    # --- CALCULATION ---
    current_step = st.session_state.idx
    current_matches = raw_matches[:current_step]
    
    teams = set()
    for w, l in current_matches:
        teams.add(w); teams.add(l)
    
    # Виклик оновленої функції
    scores = calculate_pagerank(current_matches, tuple(sorted(list(teams))))
    
    # Radii
    vals = list(scores.values())
    radii = {}
    if vals:
        mn, mx = min(vals), max(vals)
        for t, s in scores.items():
            norm = (s - mn)/(mx - mn) if mx > mn else 0.5
            radii[t] = 15 + math.sqrt(norm) * 35
            
    pos = get_layout(scores, radii)

    # --- DASHBOARD ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Matches Played", f"{current_step} / {total_matches}")
    m2.metric("Active Teams", len(teams))
    top_team = max(scores, key=scores.get) if scores else "N/A"
    m3.metric("Current Leader", top_team)

    st.markdown("---")
    
    row_graph, row_table = st.columns([2, 1])
    
    with row_graph:
        st.markdown("#### 🕸️ Interaction Graph")
        fig = create_stylish_graph(scores, current_matches, pos, radii)
        st.plotly_chart(fig, use_container_width=True)
        
    with row_table:
        st.markdown("#### 🏆 Leaderboard")
        if scores:
            df_res = pd.DataFrame(list(scores.items()), columns=["Team", "Score"])
            
            # Points formatting
            multiplier = 10000
            df_res["Score"] = (df_res["Score"] * multiplier).astype(int)
            
            df_res = df_res.sort_values(by="Score", ascending=False).reset_index(drop=True)
            df_res.index += 1
            
            max_score = max(vals) * multiplier if vals else multiplier
            
            st.dataframe(
                df_res,
                use_container_width=True,
                height=600,
                column_config={
                    "Score": st.column_config.ProgressColumn(
                        "Dominance Points",
                        format="%d",
                        min_value=0,
                        max_value=max_score, 
                    ),
                    "Team": st.column_config.TextColumn("Team Name", width="medium")
                }
            )
        else:
            st.info("No data yet.")

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👆 Upload CSV to start (or run via start.py).")
