import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="The Manab x Bimal Multiverse", page_icon="🌌", layout="centered")

# --- INITIALIZE SESSION STATE (MEMORY) ---
# This is how the game remembers the player's name and login status!
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""

# --- THE UNIFIED MULTIVERSE GAME DATA ---
GAME_DATA = {
    # --- HUB WORLD ---
    1: {"title": "The Multiverse Hub", "text": "The universes have collided! Choose your destiny.", "type": "hub", 
        "choices": {"🟥 PLAY MANAB'S OBBY": 2, "🟦 PLAY BIMAL'S SONIC ZONE": 20, "🟪 PLAY CO-OP CROSSOVER": 100}},

    # --- MANAB'S PATH (ROBLOX) ---
    2: {"title": "Manab's Obby", "text": "You spawn on a green block. A massive lava pit is in front of you.", "type": "manab", "choices": {"Take narrow bridge": 3, "Jump to platform": 4}},
    3: {"title": "💀 OOF!", "text": "The bridge was a troll! You fell into the lava.", "type": "death", "choices": {"RESPAWN AT HUB": 1}},
    4: {"title": "Boss: Mega Noob", "text": "A giant Noob blocks your path!", "type": "epic", "choices": {"Use Ban Hammer": 5}},
    5: {"title": "🏆 OBBY VICTORY!", "text": "You banned the Noob! Manab is proud.", "type": "win", "choices": {"Return to Hub": 1}},

    # --- BIMAL'S PATH (SONIC) ---
    20: {"title": "Green Hill Zone", "text": "You dash into Green Hill! A Moto Bug rolls towards you.", "type": "bimal", "choices": {"Spin Dash": 22, "Jump over it": 21}},
    21: {"title": "💥 DROPPED YOUR RINGS!", "text": "You hit a flying Buzz Bomber!", "type": "death", "choices": {"RESPAWN AT HUB": 1}},
    22: {"title": "Boss: Eggman", "text": "Dr. Eggman swings a wrecking ball!", "type": "epic", "choices": {"Target his jetpack": 23}},
    23: {"title": "🏆 ZONE CLEARED!", "text": "Eggman retreats! Bimal says you're way past cool.", "type": "win", "choices": {"Return to Hub": 1}},

    # --- THE BRAND NEW MULTIVERSE CO-OP PATH ---
    100: {"title": "🌌 The Glitched Portal", "text": "A massive portal rips open the sky. Sonic and a Roblox Noob fall out together! They need your help.", "type": "crossover", "choices": {"Help Them": 101, "Run Away": 102}},
    102: {"title": "💀 THE SERVER CRASHED", "text": "You abandoned them, and the multiverse collapsed into a 404 error.", "type": "death", "choices": {"RESPAWN AT HUB": 1}},
    101: {"title": "🌌 The Amalgamation", "text": "Dr. Eggman appears, but he's wearing a Bacon Hair wig and holding a Roblox Rocket Launcher! 'I will conquer ALL servers!' he yells.", "type": "epic", "choices": {"Use Sonic's Speed": 103, "Use Roblox Building Tools": 104}},
    103: {"title": "💨 Chaos Spin Dash!", "text": "You grab a Chaos Emerald and spin dash through Eggman's rocket, shattering his Egg Mobile into Roblox blocks!", "type": "epic", "choices": {"Finish Him": 105}},
    104: {"title": "🧱 Mega Wall Build!", "text": "You rapidly build a Roblox Tycoon mega-wall. Eggman crashes into it and gets an instant 'OOF'!", "type": "epic", "choices": {"Finish Him": 105}},
    105: {"title": "🏆 SAVED THE MULTIVERSE", "text": "Manab and Bimal high-five! You have officially saved both games. You are the Ultimate Gamer.", "type": "win", "choices": {"Play Again": 1}}
}

# --- GET CURRENT PAGE DATA ---
current_page_num = st.session_state.current_page
page_data = GAME_DATA[current_page_num]
page_type = page_data["type"]

# --- THEME ENGINE ---
if page_type == "death":
    bg_color, accent_color, badge_text = "#3d0000", "#ff0000", "GAME OVER"
    grid_color = "rgba(255, 0, 0, .1)"
elif page_type == "win":
    bg_color, accent_color, badge_text = "#002b11", "#00ffaa", "VICTORY!"
    grid_color = "rgba(0, 255, 100, .1)"
    st.balloons()
elif page_type == "epic":
    bg_color, accent_color, badge_text = "#332200", "#FFD700", "BOSS BATTLE"
    grid_color = "rgba(255, 215, 0, .1)"
elif page_type == "manab":
    bg_color, accent_color, badge_text = "#111111", "#DE3632", "ROBLOX ZONE"
    grid_color = "rgba(222, 54, 50, .1)"
elif page_type == "bimal":
    bg_color, accent_color, badge_text = "#001533", "#0033cc", "SONIC ZONE"
    grid_color = "rgba(0, 102, 255, .15)"
elif page_type == "crossover":
    bg_color, accent_color, badge_text = "#1f0033", "#ff00ff", "MULTIVERSE"
    grid_color = "rgba(255, 0, 255, .15)"
else: # Hub
    bg_color, accent_color, badge_text = "#1a1a1a", "#00B06F", "MAIN MENU"
    grid_color = "rgba(255, 255, 255, .05)"

# --- CUSTOM CSS ---
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Roboto:wght@400;900&display=swap');
        
        .stApp {{
            background-color: {bg_color};
            background-image: linear-gradient(0deg, transparent 24%, {grid_color} 25%, {grid_color} 26%, transparent 27%, transparent 74%, {grid_color} 75%, {grid_color} 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, {grid_color} 25%, {grid_color} 26%, transparent 27%, transparent 74%, {grid_color} 75%, {grid_color} 76%, transparent 77%, transparent);
            background-size: 50px 50px;
            color: white;
            font-family: 'Roboto', sans-serif;
            transition: all 0.5s ease;
        }}
        header {{visibility: hidden;}}
        h1 {{ font-family: 'Press Start 2P', cursive; text-align: center; color: #FFF; text-shadow: 4px 4px {accent_color}; padding-bottom: 20px; }}
        .game-card {{ background: #1a1c23; border: 3px solid {accent_color}; border-bottom: 8px solid {accent_color}; border-radius: 15px; padding: 30px; margin-bottom: 30px; position: relative; }}
        .level-badge {{ background-color: {accent_color}; color: {"black" if page_type in ["epic", "crossover"] else "white"}; font-family: 'Press Start 2P', cursive; font-size: 12px; padding: 10px; position: absolute; top: -15px; left: 20px; border: 2px solid #000; transform: rotate(-2deg); }}
        .story-text {{ font-size: 18px; line-height: 1.6; margin-top: 20px; margin-bottom: 20px; color: #ddd; }}
        
        .stButton>button {{ width: 100%; background: linear-gradient(45deg, #222, #444); font-family: 'Press Start 2P', cursive !important; font-size: 12px; color: white; border: 2px solid {accent_color}; border-radius: 10px; padding: 15px; transition: all 0.2s; }}
        .stButton>button:hover {{ border-color: #fff; transform: scale(1.03); }}
    </style>
""", unsafe_allow_html=True)

# --- RENDER HEADER & CARD ---
st.markdown("<h1>THE MULTIVERSE</h1>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="game-card">
        <div class="level-badge">{badge_text}</div>
        <h2 style="color:{accent_color}; font-family:'Roboto'; font-weight:900; font-style:italic;">{page_data["title"]}</h2>
        <div class="story-text">{page_data["text"]}</div>
    </div>
""", unsafe_allow_html=True)

# --- SECURITY LOGIN LOGIC (ONLY ON PAGE 1) ---
if current_page_num == 1:
    # If they haven't logged in yet, show the form
    if not st.session_state.is_authenticated:
        with st.container():
            st.markdown("<h4 style='color:#FFD700;'>Player Registration:</h4>", unsafe_allow_html=True)
            
            input_name = st.text_input("Gamer Tag:")
            friend_check = st.checkbox("🤝 I confirm I am awesome friends with Manab & Bimal!")
            
            if st.button("ENTER MULTIVERSE", key="login_btn"):
                if input_name.strip() == "":
                    st.error("🛑 HOLD UP! Enter your Gamer Tag first!")
                elif not friend_check:
                    st.error("🚨 SECURITY ALERT: You must tick the friendship box to enter!")
                else:
                    # Save details to Streamlit memory!
                    st.session_state.player_name = input_name
                    st.session_state.is_authenticated = True
                    st.rerun() # Refresh the page to hide the form
    
    # If they are ALREADY logged in, show a welcome message and the game paths
    else:
        st.success(f"🎮 Welcome back to the Multiverse, **{st.session_state.player_name}**!")
        
        # Display the 3 Game Paths
        cols = st.columns(len(page_data["choices"])) 
        for i, (choice_text, target_page) in enumerate(page_data["choices"].items()):
            with cols[i]:
                if st.button(choice_text, key=f"btn_hub_{i}"):
                    st.session_state.current_page = target_page
                    st.rerun()

# --- ALL OTHER GAME PAGES (LEVELS 2+) ---
else:
    if "choices" in page_data and page_data["choices"]:
        cols = st.columns(len(page_data["choices"])) 
        for i, (choice_text, target_page) in enumerate(page_data["choices"].items()):
            with cols[i]:
                if st.button(choice_text, key=f"btn_{current_page_num}_{i}"):
                    st.session_state.current_page = target_page
                    st.rerun()