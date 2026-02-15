import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bimal's Sonic Quest", page_icon="🦔", layout="centered")

# --- INITIALIZE SESSION STATE ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'ring_clicks' not in st.session_state:
    st.session_state.ring_clicks = 0

# --- THE BIMAL GAME UNIVERSE (Sonic Theme) ---
GAME_DATA = {
    1: {"title": "The Ring Portal", "text": "Welcome to Bimal's Universe! Gotta go fast! Fill out your stats to spin dash into the game.", "type": "normal", "choices": {"🌴 GREEN HILL ZONE": 2, "🎰 CASINO NIGHT": 20, "⚙️ DEATH EGG": 35}},
    
    # Easter Eggs
    99: {"title": "💎 MASTER EMERALD SHRINE", "text": "ACCESS GRANTED. You found the secret dev room. You possess all 7 Chaos Emeralds. You are Super Bimal.", "type": "epic", "choices": {"Return to Reality": 1}},
    404: {"title": "ZONE ERROR 404", "text": "You broke the matrix. You are now stuck in the Special Stage void.", "type": "glitch", "choices": {"Try to Escape": 1, "Fall deeper": 404}},

    # --- GREEN HILL PATH ---
    2: {"title": "Zone 1: Green Hill", "text": "You dash into Green Hill Zone! A Moto Bug is rolling towards you!", "type": "normal", "choices": {"Spin Dash it!": 4, "Jump over it": 3}},
    3: {"title": "💥 DROPPED YOUR RINGS!", "text": "You hit a flying Buzz Bomber! You lost all your rings.", "type": "death", "choices": {"RETRY ZONE": 1}},
    4: {"title": "Zone 2: The Loop", "text": "Nice Spin Dash! You are running towards a giant loop-de-loop.", "type": "normal", "choices": {"Hold Forward (Speed!)": 6, "Hit the brakes": 5}},
    5: {"title": "💥 NOT FAST ENOUGH!", "text": "You didn't have enough momentum! You fell upside down.", "type": "death", "choices": {"RETRY ZONE": 1}},
    6: {"title": "Zone 3: Star Post", "text": "Checkpoint! A red spring and a yellow spring are ahead.", "type": "normal", "choices": {"Hit Red Spring": 7, "Hit Yellow Spring": 8}},
    7: {"title": "Zone 4: High Route", "text": "The red spring launched you to the clouds! You found a giant ring.", "type": "normal", "choices": {"Jump into the Giant Ring": 9, "Ignore it and run": 10}},
    8: {"title": "💥 SPIKES!", "text": "The yellow spring didn't shoot you high enough. Spikes!", "type": "death", "choices": {"RETRY ZONE": 1}},
    9: {"title": "Zone 5: Special Stage", "text": "You are in a 3D maze! You need to grab the blue spheres.", "type": "normal", "choices": {"Turn Left": 11, "Turn Right": 12}},
    10: {"title": "💥 CRUSHED!", "text": "You ignored the ring and ran right into a wall trap.", "type": "death", "choices": {"RETRY ZONE": 1}},
    11: {"title": "Zone 6: Blue Sphere", "text": "Perfect turn! You grab the last sphere and unlock a Chaos Emerald!", "type": "epic", "choices": {"Return to Level": 13, "Stay in maze": 14}},
    12: {"title": "💥 RED SPHERE!", "text": "You touched a red sphere! You were kicked out.", "type": "death", "choices": {"RETRY ZONE": 1}},
    13: {"title": "🔥 BOSS: EGG MOBILE", "text": "Dr. Eggman swings a giant wrecking ball at you!", "type": "epic", "choices": {"Jump on his head": 15, "Wait for the swing": 16}},
    14: {"title": "💥 LOST IN TIME", "text": "You stayed in the maze too long. Time Over.", "type": "death", "choices": {"RETRY ZONE": 1}},
    15: {"title": "🔥 BOSS PHASE 2", "text": "Direct hit! Eggman shoots a laser!", "type": "epic", "choices": {"Dodge Left": 17, "Dodge Right": 18}},
    16: {"title": "💥 FLATTENED", "text": "You got squashed by the wrecking ball.", "type": "death", "choices": {"RETRY ZONE": 1}},
    17: {"title": "🏆 ZONE CLEARED!", "text": "You defeated Eggman and saved the animals!", "type": "win", "choices": {"Return to Menu": 1, "🌟 UNLOCK SUPER ENDING": 50}},
    18: {"title": "💥 ZAPPED!", "text": "You dodged right into the laser beam.", "type": "death", "choices": {"RETRY ZONE": 1}},
    
    # --- CASINO NIGHT PATH ---
    20: {"title": "Zone 1: Casino Night", "text": "Neon lights everywhere! You drop into a giant pinball machine.", "type": "normal", "choices": {"Hit the flipper": 21, "Fall down middle": 22}},
    21: {"title": "Zone 2: Slot Machine [MINI-GAME]", "text": "You are stuck in the slot machine! Spam click the lever to build momentum.", "type": "normal", "choices": {}}, # Choices handled by mini-game logic
    22: {"title": "💥 GUTTERBALL!", "text": "You fell down the pinball drain.", "type": "death", "choices": {"RETRY ZONE": 1}},
    23: {"title": "Zone 3: JACKPOT!", "text": "Three Bimal icons! You just won 1,000 rings!", "type": "epic", "choices": {"Go to the Vault": 25, "Gamble it all": 26}},
    25: {"title": "🔥 THE VAULT [MINI-GAME]", "text": "Shadow is guarding the Vault. Enter the 4-digit PIN to bypass him. (Hint: The year Sonic was created!)", "type": "epic", "choices": {"Run away": 28}}, # PIN handled by logic
    26: {"title": "💥 BANKRUPT!", "text": "You gambled it all and lost everything.", "type": "death", "choices": {"RETRY ZONE": 1}},
    28: {"title": "Zone 5: The Exit", "text": "You ran away and found the Casino exit.", "type": "win", "choices": {"Leave Casino": 1}},
    29: {"title": "🏆 VAULT UNLOCKED", "text": "You correctly guessed the PIN! You are the true Casino champion.", "type": "win", "choices": {"Return to Menu": 1, "🌟 UNLOCK SUPER ENDING": 50}},

    # --- DEATH EGG PATH ---
    35: {"title": "Zone 1: Death Egg", "text": "You board Eggman's space station. The gravity feels weird.", "type": "normal", "choices": {"Run on the ceiling": 36, "Run on the floor": 37}},
    36: {"title": "Zone 2: Laser Grid", "text": "Ceiling route was smart! Now you face a grid of moving lasers.", "type": "normal", "choices": {"Slide under": 38, "Jump over": 39}},
    37: {"title": "💥 TRAP DOOR!", "text": "The floor opened up and dropped you into space.", "type": "death", "choices": {"RETRY ZONE": 1}},
    38: {"title": "Zone 3: Metal Sonic", "text": "You slid under! Suddenly, Metal Sonic drops from the ceiling.", "type": "epic", "choices": {"Race Him": 40, "Punch Him": 41}},
    39: {"title": "💥 ZAPPED!", "text": "You jumped, but hit an invisible laser.", "type": "death", "choices": {"RETRY ZONE": 1}},
    40: {"title": "Zone 4: The Race", "text": "You are racing Metal Sonic down a collapsing hallway!", "type": "normal", "choices": {"Use Boost": 43, "Save Boost": 42}},
    41: {"title": "💥 SHIELDS UP", "text": "You punched his electric shield and lost all your rings.", "type": "death", "choices": {"RETRY ZONE": 1}},
    42: {"title": "💥 TOO SLOW", "text": "Metal Sonic beat you to the door and locked you out.", "type": "death", "choices": {"RETRY ZONE": 1}},
    43: {"title": "Zone 5: Giant Mech", "text": "You beat Metal! But now Eggman jumps into the giant Death Egg Robot.", "type": "epic", "choices": {"Target the jetpack": 44}},
    44: {"title": "🔥 FINAL HIT", "text": "The jetpack explodes! The robot is falling apart.", "type": "epic", "choices": {"Hit the cockpit": 46, "Run away": 47}},
    46: {"title": "Zone 6: Escape!", "text": "You destroyed it! The Death Egg is exploding, run to the escape pod!", "type": "normal", "choices": {"Get in Pod": 48}},
    47: {"title": "💥 TRIPPED", "text": "You tripped on scrap metal.", "type": "death", "choices": {"RETRY ZONE": 1}},
    48: {"title": "🏆 SAVED THE WORLD!", "text": "You escaped the Death Egg just in time. Bimal is proud.", "type": "win", "choices": {"Return to Menu": 1, "🌟 UNLOCK SUPER ENDING": 50}},
    
    # --- ENDING ---
    50: {"title": "👑 SUPER BIMAL UNLOCKED", "text": "YOU COLLECTED ALL 7 CHAOS EMERALDS! You have unlocked the ultimate Super Bimal ending.", "type": "epic", "choices": {"Play Again": 1}}
}

# --- GET CURRENT PAGE DATA ---
current_page_num = st.session_state.current_page
page_data = GAME_DATA[current_page_num]
page_type = page_data["type"]

# Streamlit Native Animation on Win
if page_type == "win":
    st.balloons()
elif current_page_num == 50:
    st.snow() # Chaos Emerald Magic

# --- DYNAMIC THEME ENGINE (SONIC THEME) ---
if page_type == "death":
    bg_color, accent_color, badge_text = "#3d0000", "#e30022", "GAME OVER"
    grid_color = "rgba(255, 0, 0, .15)"
    card_animation = "animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;"
elif page_type == "win":
    bg_color, accent_color, badge_text = "#002b11", "#00ffaa", "ZONE CLEARED"
    grid_color = "rgba(0, 255, 100, .15)"
    card_animation = "animation: float 3s ease-in-out infinite;"
elif page_type == "epic":
    bg_color, accent_color, badge_text = "#332200", "#FFD700", "BOSS BATTLE"
    grid_color = "rgba(255, 215, 0, .15)"
    card_animation = "animation: float 2s ease-in-out infinite, epicPulse 2s infinite;"
elif page_type == "glitch":
    bg_color, accent_color, badge_text = "#00ff00", "#000000", "ERR 404"
    grid_color = "rgba(0, 255, 0, 0)"
    card_animation = ""
else:
    bg_color, accent_color, badge_text = "#001533", "#0033cc", f"ZONE {current_page_num}" if current_page_num > 1 else "MENU"
    grid_color = "rgba(0, 102, 255, .15)"
    card_animation = "animation: float 4s ease-in-out infinite;"

# --- INJECT CUSTOM CSS ---
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Roboto:wght@400;900&display=swap');
        
        @keyframes float {{ 0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} 100% {{ transform: translateY(0px); }} }}
        @keyframes shake {{ 10%, 90% {{ transform: translate3d(-2px, 0, 0); }} 20%, 80% {{ transform: translate3d(4px, 0, 0); }} 30%, 50%, 70% {{ transform: translate3d(-8px, 0, 0); }} 40%, 60% {{ transform: translate3d(8px, 0, 0); }} }}
        @keyframes epicPulse {{ 0% {{ box-shadow: 0 0 10px #FFD700; }} 50% {{ box-shadow: 0 0 30px #FFD700; border-color: #FFD700; }} 100% {{ box-shadow: 0 0 10px #FFD700; }} }}
        @keyframes textFadeIn {{ from {{ opacity: 0; transform: translateY(15px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .stApp {{
            background-color: {bg_color};
            background-image: linear-gradient(0deg, transparent 24%, {grid_color} 25%, {grid_color} 26%, transparent 27%, transparent 74%, {grid_color} 75%, {grid_color} 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, {grid_color} 25%, {grid_color} 26%, transparent 27%, transparent 74%, {grid_color} 75%, {grid_color} 76%, transparent 77%, transparent);
            background-size: 50px 50px;
            color: {"#000" if page_type == "glitch" else "white"};
            font-family: 'Roboto', sans-serif;
            transition: all 0.5s ease;
        }}
        
        header {{visibility: hidden;}}
        
        h1 {{ font-family: 'Press Start 2P', cursive; text-align: center; color: #FFD700; text-shadow: 4px 4px #0033cc; padding-bottom: 20px; }}
        
        .game-card {{
            background: #1a1c23; border: 3px solid {accent_color}; border-bottom: 8px solid {accent_color};
            border-radius: 15px; padding: 30px; margin-bottom: 30px; position: relative; {card_animation}
        }}
        
        .level-badge {{
            background-color: {"#e30022" if page_type != "glitch" else "#000"};
            color: {"black" if page_type == "epic" else "white"};
            font-family: 'Press Start 2P', cursive; font-size: 12px; padding: 10px; position: absolute;
            top: -15px; left: 20px; border: 2px solid #000; transform: rotate(-2deg);
        }}
        
        .story-text {{ font-size: 18px; line-height: 1.6; margin-top: 20px; margin-bottom: 20px; color: #ddd; animation: textFadeIn 0.6s ease-out forwards; }}
        
        .stButton>button {{
            width: 100%; background: linear-gradient(45deg, #0033cc, #0055ff); font-family: 'Press Start 2P', cursive !important;
            font-size: 12px; color: white; border: 2px solid #000; border-radius: 10px; padding: 15px;
            box-shadow: 0 6px 0 #001166; transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .stButton>button:active {{ transform: translateY(6px); box-shadow: none; }}
        .stButton>button:hover {{ border-color: #FFD700; color: #FFD700; transform: scale(1.03); }}
    </style>
""", unsafe_allow_html=True)

# --- RENDER THE GAME UI ---
st.markdown("<h1>BIMAL'S<br>SONIC QUEST</h1>", unsafe_allow_html=True)

# Create the HTML Card Shell
st.markdown(f"""
    <div class="game-card">
        <div class="level-badge">{badge_text}</div>
        <h2 style="color:{accent_color}; font-family:'Roboto'; font-weight:900; font-style:italic; animation: textFadeIn 0.4s ease-out;">{page_data["title"]}</h2>
        <div class="story-text">{page_data["text"]}</div>
    </div>
""", unsafe_allow_html=True)

# --- LEVEL 1: THE SECURITY FORM & CHEATS ---
if current_page_num == 1:
    st.session_state.ring_clicks = 0 # Reset mini-game state
    
    with st.container():
        st.markdown("<h4 style='color:#FFD700; animation: textFadeIn 0.8s ease-out;'>Player Registration:</h4>", unsafe_allow_html=True)
        player_name = st.text_input("Gamer Tag (Type BIMAL for secret):")
        char_style = st.selectbox("Character Style:", ["Sonic (Speed)", "Tails (Flight)", "Knuckles (Power)"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        # Security Bouncer Checkbox
        friend_check = st.checkbox("🦔 I swear I am 'way past cool' and a true friend of Bimal!")
        st.write("---")

    # Choice buttons for Level 1
    cols = st.columns(len(page_data["choices"])) 
    for i, (choice_text, target_page) in enumerate(page_data["choices"].items()):
        with cols[i]:
            if st.button(choice_text, key=f"btn_hub_{i}"):
                # Cheat Code Check!
                if player_name.strip().upper() in ["BIMAL", "SONIC"]:
                    st.session_state.current_page = 99
                    st.rerun()
                # Security Check!
                elif not player_name.strip():
                    st.error("🛑 HOLD UP! You must enter your Gamer Tag before dashing in!")
                elif not friend_check:
                    st.error("🚨 EGGMAN ALERT: You must tick the box confirming you are Bimal's friend to pass!")
                else:
                    st.session_state.current_page = target_page
                    st.rerun()

# --- LEVEL 21: THE SLOT MACHINE CLICKER MINI-GAME ---
elif current_page_num == 21:
    st.markdown(f"<h3 style='text-align:center; color:#FFD700;'>🔄 SPINS: {st.session_state.ring_clicks} / 15</h3>", unsafe_allow_html=True)
    
    if st.session_state.ring_clicks < 15:
        if st.button("🎰 PULL LEVER!"):
            st.session_state.ring_clicks += 1
            st.rerun()
    else:
        st.success("🎰 SLOT MACHINE ACTIVE! 🎰")
        if st.button("🛑 STOP THE WHEELS!", key="stop_wheels"):
            st.session_state.current_page = 23
            st.rerun()

# --- LEVEL 25: THE VAULT PASSWORD MINI-GAME ---
elif current_page_num == 25:
    st.markdown("<h4 style='color:#00aaff;'>Enter 4-Digit PIN:</h4>", unsafe_allow_html=True)
    pin_code = st.text_input("Vault PIN:", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔓 UNLOCK VAULT"):
            if pin_code == "1991":
                st.session_state.current_page = 29
                st.rerun()
            else:
                st.error("❌ WRONG PIN! Shadow caught you!")
                time.sleep(1.5) # Pauses so the player can read the error before dying
                st.session_state.current_page = 26
                st.rerun()
    with col2:
        if st.button("🏃‍♂️ Run away"):
            st.session_state.current_page = 28
            st.rerun()

# --- STANDARD RENDER CHOICES (FOR ALL OTHER LEVELS) ---
else:
    if page_data["choices"]:
        cols = st.columns(len(page_data["choices"])) 
        for i, (choice_text, target_page) in enumerate(page_data["choices"].items()):
            with cols[i]:
                if st.button(choice_text, key=f"btn_{current_page_num}_{i}"):
                    st.session_state.current_page = target_page
                    st.rerun()

# --- PROGRESS BAR (RINGS COLLECTED) ---
st.markdown("<br><br>", unsafe_allow_html=True)
# Cap the progress bar at 1.0 (100%)
progress_val = min(current_page_num / 50.0, 1.0)
st.progress(progress_val, text=f"RINGS COLLECTED: {current_page_num}/50")

# --- EASTER EGG (THE BACKROOMS BADGE) ---
# Because Streamlit buttons have a specific layout, we add a secret invisible button at the bottom for the 404 glitch
st.markdown("<br><br><br>", unsafe_allow_html=True)
if st.button(".", key="secret_glitch_btn"):
    st.session_state.current_page = 404
    st.rerun()
