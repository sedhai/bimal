import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Manab's Gaming Quest", page_icon="🎮", layout="centered")

# --- INITIALIZE SESSION STATE ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# --- THE 50-PAGE GAME UNIVERSE (With Theme Types) ---
GAME_DATA = {
    1: {"title": "The Spawn Point", "text": "Welcome to Manab's Universe! Fill out your stats, then choose your path.", "type": "normal", "choices": {"🚀 PLAY OBBY (Action)": 2, "🏗️ PLAY TYCOON (Strategy)": 20, "🔦 PLAY HORROR (Scary)": 35}},
    
    # --- OBBY PATH ---
    2: {"title": "Level 2: The Obby", "text": "You spawn on a green block. A massive lava pit is in front of you.", "type": "normal", "choices": {"Take narrow bridge": 3, "Jump to platform": 4}},
    3: {"title": "💀 OOF!", "text": "The bridge was a troll! You fell into the lava.", "type": "death", "choices": {"RESPAWN": 1}},
    4: {"title": "Level 3: Lasers", "text": "Perfect jump! Now you face spinning lasers.", "type": "normal", "choices": {"Run fast!": 5, "Wait and time it": 6}},
    5: {"title": "💀 OOF!", "text": "You got zapped. Patience is a virtue, noob.", "type": "death", "choices": {"RESPAWN": 1}},
    6: {"title": "Level 4: Checkpoint", "text": "Checkpoint! A locked door blocks your path.", "type": "normal", "choices": {"Search for key": 7, "Glitch through wall": 8}},
    7: {"title": "Level 5: Key Room", "text": "You found a glowing key guarded by a sleeping Noob.", "type": "normal", "choices": {"Sneak past": 9, "Attack the Noob": 10}},
    8: {"title": "💀 Anti-Cheat!", "text": "Manab's anti-cheat caught you glitching. BANNED.", "type": "death", "choices": {"RESPAWN": 1}},
    9: {"title": "Level 6: Dark Cave", "text": "You unlocked the door. You enter a dark cave.", "type": "normal", "choices": {"Left Tunnel": 11, "Right Tunnel": 12}},
    10: {"title": "💀 OOF!", "text": "The Noob woke up and hit you with a ban hammer.", "type": "death", "choices": {"RESPAWN": 1}},
    11: {"title": "Level 7: Jetpack", "text": "The left tunnel is safe! You find a jetpack.", "type": "normal", "choices": {"Equip Jetpack": 13, "Leave it": 14}},
    12: {"title": "💀 Cave In!", "text": "The right tunnel collapsed!", "type": "death", "choices": {"RESPAWN": 1}},
    13: {"title": "🔥 BOSS ROOM", "text": "You fly up. The Mega-Bacon-Hair Boss appears!", "type": "epic", "choices": {"Shoot laser": 15, "Fly around him": 16}},
    14: {"title": "💀 The Floor is Lava", "text": "You should have taken the jetpack.", "type": "death", "choices": {"RESPAWN": 1}},
    15: {"title": "🔥 BOSS PHASE 2", "text": "Direct hit! The boss shrinks and begs for mercy.", "type": "epic", "choices": {"Spare him": 17, "Oof him": 18}},
    16: {"title": "💀 Out of fuel", "text": "Your jetpack ran out of gas. You fell.", "type": "death", "choices": {"RESPAWN": 1}},
    17: {"title": "🏆 OBBY VICTORY!", "text": "You showed mercy! You are an Obby Master.", "type": "win", "choices": {"Main Hub": 1, "🌟 UNLOCK SECRET": 50}},
    18: {"title": "💀 Karma!", "text": "He used a reverse Uno card on you.", "type": "death", "choices": {"RESPAWN": 1}},
    19: {"title": "Secret Room", "text": "You found Manab's stash of Robux.", "type": "win", "choices": {"Take some": 1}},
    
    # --- TYCOON PATH ---
    20: {"title": "Level 2: Tycoon Start", "text": "You claim a blank Tycoon base. You have $10.", "type": "normal", "choices": {"Buy a Dropper": 21, "Buy Walls": 22}},
    21: {"title": "Level 3: Cash Flow", "text": "The dropper makes $1 a sec. You get $50.", "type": "normal", "choices": {"Buy Upgrade": 23, "Buy Sword": 24}},
    22: {"title": "💀 Raided!", "text": "You bought walls but had no money. A player broke in.", "type": "death", "choices": {"RESPAWN": 1}},
    23: {"title": "Level 4: Empire", "text": "Your tycoon is huge! Making $1000 a sec.", "type": "normal", "choices": {"Build Mega Laser": 25, "Build Forcefield": 26}},
    24: {"title": "Level 5: Warrior", "text": "You bought a sword and went outside.", "type": "normal", "choices": {"Attack Pro": 27, "Attack Noob": 28}},
    25: {"title": "🔥 MEGA LASER", "text": "You blasted the server. You are the Tycoon King!", "type": "epic", "choices": {"Claim Victory": 29}},
    26: {"title": "Level 6: The Turtle", "text": "You sit in your base forever. Boring.", "type": "normal", "choices": {"Go outside": 24}},
    27: {"title": "💀 OOF!", "text": "The Pro had admin commands. Destroyed.", "type": "death", "choices": {"RESPAWN": 1}},
    28: {"title": "Level 6: Victory?", "text": "You beat the noob, but his big brother joined.", "type": "epic", "choices": {"Run away": 1, "Fight him": 27}},
    29: {"title": "🏆 TYCOON VICTORY", "text": "You are the richest player on the server!", "type": "win", "choices": {"Main Hub": 1, "🌟 UNLOCK SECRET": 50}},
    30: {"title": "Bank", "text": "Money stored.", "type": "normal", "choices": {"Withdraw": 20}},
    31: {"title": "Shop", "text": "Buy hats.", "type": "normal", "choices": {"Back": 20}},
    32: {"title": "💀 Glitch", "text": "Fell through map.", "type": "death", "choices": {"RESPAWN": 1}},
    33: {"title": "💀 AFK", "text": "Disconnected for being AFK.", "type": "death", "choices": {"RECONNECT": 1}},
    34: {"title": "Admin Room", "text": "Secret area.", "type": "epic", "choices": {"Leave": 1}},

    # --- HORROR PATH ---
    35: {"title": "Level 2: Horror Maze", "text": "It's pitch black. You hear a weird noise.", "type": "normal", "choices": {"Turn on flashlight": 36, "Walk in dark": 37}},
    36: {"title": "Level 3: The Doors", "text": "Two doors. Door 1 has blood. Door 2 smells like pizza.", "type": "normal", "choices": {"Enter Door 1": 38, "Enter Door 2": 39}},
    37: {"title": "💀 Jump Scare!", "text": "Monster got you. OOF.", "type": "death", "choices": {"RESPAWN": 1}},
    38: {"title": "Level 4: Safe Room!", "text": "Reverse psychology! Door 1 was safe. Found a medkit.", "type": "normal", "choices": {"Heal up": 40, "Save for later": 41}},
    39: {"title": "💀 Pizza Trap", "text": "Pizza was a lie. You were eaten.", "type": "death", "choices": {"RESPAWN": 1}},
    40: {"title": "Level 5: Generator", "text": "Generator needs a 4 digit code.", "type": "normal", "choices": {"Enter 1234": 42, "Look for clues": 43}},
    41: {"title": "💀 Infection", "text": "You turned into a zombie.", "type": "death", "choices": {"RESPAWN": 1}},
    42: {"title": "💀 Wrong Code", "text": "Alarm sounds. Monsters find you.", "type": "death", "choices": {"RESPAWN": 1}},
    43: {"title": "Level 6: The Clue", "text": "Note says: 'Manab's favorite number'. It's 7777!", "type": "normal", "choices": {"Enter 7777": 44}},
    44: {"title": "Level 7: Power On!", "text": "Lights on! A secret elevator opens.", "type": "normal", "choices": {"Get in": 45}},
    45: {"title": "🔥 FINAL CHASE", "text": "Elevator breaks. A monster is chasing you!", "type": "epic", "choices": {"Slide under wall": 46, "Jump over it": 47}},
    46: {"title": "Level 8: Escaped!", "text": "You slid to safety and locked the doors.", "type": "normal", "choices": {"Open Reward": 48}},
    47: {"title": "💀 Tripped!", "text": "Didn't jump high enough.", "type": "death", "choices": {"RESPAWN": 1}},
    48: {"title": "🏆 HORROR VICTORY!", "text": "You survived Manab's haunted maze.", "type": "win", "choices": {"Main Hub": 1, "🌟 UNLOCK SECRET": 50}},
    49: {"title": "The Void", "text": "Lost forever.", "type": "death", "choices": {"Wake up": 1}},

    # --- FINAL BOSS ---
    50: {"title": "👑 MANAB'S INNER CIRCLE", "text": "YOU FOUND THE SECRET 50TH PAGE! You have completed all paths. You are officially an elite gamer.", "type": "epic", "choices": {"Restart Game": 1}}
}

# --- GET CURRENT PAGE DATA ---
current_page_num = st.session_state.current_page
page_data = GAME_DATA[current_page_num]
page_type = page_data["type"]

# --- DYNAMIC THEME ENGINE ---
# We change the colors based on the page 'type' (normal, death, win, epic)
if page_type == "death":
    bg_color, accent_color, badge_text = "#3d0000", "#ff0000", "GAME OVER"
    grid_color = "rgba(255, 0, 0, .1)"
elif page_type == "win":
    bg_color, accent_color, badge_text = "#002b11", "#00ff00", "VICTORY!"
    grid_color = "rgba(0, 255, 0, .05)"
elif page_type == "epic":
    bg_color, accent_color, badge_text = "#2b003a", "#FFE600", "BOSS LEVEL"
    grid_color = "rgba(255, 215, 0, .1)"
else:
    bg_color, accent_color, badge_text = "#111111", "#00B06F", f"LEVEL {current_page_num}"
    grid_color = "rgba(255, 255, 255, .05)"

# --- INJECT CUSTOM CSS ---
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Roboto:wght@400;900&display=swap');
        
        /* Main Background */
        .stApp {{
            background-color: {bg_color};
            background-image: linear-gradient(0deg, transparent 24%, {grid_color} 25%, {grid_color} 26%, transparent 27%, transparent 74%, {grid_color} 75%, {grid_color} 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, {grid_color} 25%, {grid_color} 26%, transparent 27%, transparent 74%, {grid_color} 75%, {grid_color} 76%, transparent 77%, transparent);
            background-size: 50px 50px;
            color: white;
            font-family: 'Roboto', sans-serif;
            transition: all 0.5s ease;
        }}
        
        /* Hide Default Streamlit Header */
        header {{visibility: hidden;}}
        
        /* Main Title */
        h1 {{
            font-family: 'Press Start 2P', cursive;
            text-align: center;
            color: #FFE600;
            text-shadow: 4px 4px #DE3632;
            padding-bottom: 20px;
        }}
        
        /* The Game Card */
        .game-card {{
            background: #2a2d33;
            border: 3px solid {accent_color};
            border-bottom: 8px solid {accent_color};
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            position: relative;
        }}
        
        /* The Level Badge */
        .level-badge {{
            background-color: {accent_color};
            color: {"black" if page_type == "epic" else "white"};
            font-family: 'Press Start 2P', cursive;
            font-size: 12px;
            padding: 10px;
            position: absolute;
            top: -15px;
            left: 20px;
            border: 2px solid #000;
            transform: rotate(-2deg);
        }}
        
        /* Story Text inside Card */
        .story-text {{
            font-size: 18px;
            line-height: 1.6;
            margin-top: 20px;
            margin-bottom: 20px;
            color: #ddd;
        }}
        
        /* Button Styling */
        .stButton>button {{
            width: 100%;
            background: linear-gradient(45deg, #DE3632, #FF5733);
            font-family: 'Press Start 2P', cursive !important;
            font-size: 12px;
            color: white;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 6px 0 #8b0000;
            transition: all 0.1s;
        }}
        .stButton>button:active {{
            transform: translateY(6px);
            box-shadow: none;
        }}
        .stButton>button:hover {{
            border-color: #FFE600;
            color: #FFE600;
        }}
    </style>
""", unsafe_allow_html=True)

# --- RENDER THE GAME UI ---
st.markdown("<h1>MANAB'S<br>GAMING QUEST</h1>", unsafe_allow_html=True)

# Create the HTML Card Shell
st.markdown(f"""
    <div class="game-card">
        <div class="level-badge">{badge_text}</div>
        <h2 style="color:{accent_color}; font-family:'Roboto'; font-weight:900; font-style:italic;">{page_data["title"]}</h2>
        <div class="story-text">{page_data["text"]}</div>
    </div>
""", unsafe_allow_html=True)

# --- SPECIAL FOR LEVEL 1: THE FORM ---
# Streamlit allows us to build real interactive forms right inside the Python code
if current_page_num == 1:
    with st.container():
        st.markdown("<h4 style='color:#00B06F;'>Enter Player Stats:</h4>", unsafe_allow_html=True)
        player_name = st.text_input("Real Name / Spy Code Name:")
        roblox_user = st.text_input("Roblox Username:")
        avatar_style = st.selectbox("Avatar Style:", ["Bacon Hair", "Blocky", "Tryhard (Emo)"])
        st.write("---")

# --- RENDER CHOICES (BUTTONS) ---
# We loop through the dictionary choices and create a Streamlit button for each one
cols = st.columns(len(page_data["choices"])) # Puts buttons side-by-side
for i, (choice_text, target_page) in enumerate(page_data["choices"].items()):
    with cols[i]:
        # When a button is clicked, change the state and rerun the script!
        if st.button(choice_text, key=f"btn_{current_page_num}_{i}"):
            st.session_state.current_page = target_page
            st.rerun()

# --- PROGRESS BAR ---
st.markdown("<br><br>", unsafe_allow_html=True)
progress_val = min(current_page_num / 50.0, 1.0)
st.progress(progress_val, text=f"QUEST PROGRESS: PAGE {current_page_num}/50")