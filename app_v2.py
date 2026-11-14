"""
Version 2 — Reliable AI Escape Room (Visual & Interactive Edition)
Architecture: State-Machine & Action Validation with LLM Narrator (Streamlit + Gemini)
Includes: Visual scene artwork, interactive object inspection cards, physical digital keypad, sound effects.
"""

import os
import base64
from typing import Dict, Any

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    load_dotenv = None

try:
    import streamlit as st  # type: ignore
except ImportError:
    st = None  # type: ignore

try:
    from google import genai  # type: ignore
except ImportError:
    genai = None

from game_engine import EscapeRoomEngine

# Pure Python fallback loader for .env
def load_env():
    if load_dotenv:
        load_dotenv()
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

load_env()

st.set_page_config(
    page_title="AI Escape Room - V2 (Interactive Visual)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Atmospheric CSS (Dark Academia Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');
    
    .stApp {
        background-color: #0c0d14;
        color: #e2e8f0;
        font-family: 'Crimson Pro', Georgia, serif;
    }
    
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 1px;
    }
    
    .room-card {
        background: #141724;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        transition: transform 0.2s, border-color 0.2s;
    }
    .room-card:hover {
        border-color: #d4af37;
        transform: translateY(-2px);
    }
    
    .keypad-display {
        font-family: 'Courier New', monospace;
        background: #020617;
        color: #38bdf8;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 6px;
        padding: 10px 16px;
        border-radius: 6px;
        border: 2px solid #0284c7;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .badge-locked {
        background: #450a0a;
        color: #fca5a5;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-unlocked {
        background: #052e16;
        color: #86efac;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Helper to play audio cues
def play_sound(sound_name: str):
    path = f"assets/{sound_name}.wav"
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(
                    f'<audio autoplay style="display:none;"><source src="data:audio/wav;base64,{b64}" type="audio/wav"></audio>',
                    unsafe_allow_html=True
                )
        except Exception:
            pass

# Helper to load and display SVG/images
def get_image_base64(path: str) -> str:
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# LLM Narrator Prompt - strictly grounded in validated facts
NARRATOR_SYSTEM_PROMPT = """
You are the AI Narrator for an interactive escape room game in a Victorian Library.
CRITICAL OPERATIONAL RULES:
1. You do NOT decide game outcomes, inventory changes, or lock states. The Python Game Engine already evaluated the player's action.
2. You will be provided with:
   - The Player's raw input.
   - The Engine's VALIDATED FACTS and OUTCOME STATUS.
   - The current Room and Inventory state.
3. Your sole job is to translate the engine's validated facts into an atmospheric, immersive, and vivid literary description.
4. NEVER contradict the engine's facts. If the engine reports an action failed, describe why it failed atmospherically.
5. If the engine reports SECURITY ALERT / INJECTION_BLOCKED, speak in an ominous tone stating that cosmic/mechanical laws cannot be warped by words alone.
6. If the engine reports the player escaped, conclude with triumphant narrative and include "[GAME WON]".
"""

def generate_v2_narrative(player_input, engine_outcome, current_state, api_key=None, model_name="gemini-3.8-flash"):
    """Ask Gemini to narrate the engine-validated outcome."""
    clean_key = api_key.strip() if api_key else ""
    if clean_key and clean_key.startswith("AIzaSy") and genai is not None:
        try:
            client = genai.Client(api_key=clean_key)
            prompt = (
                f"{NARRATOR_SYSTEM_PROMPT}\n\n"
                f"--- CURRENT GAME CONTEXT ---\n"
                f"Inventory: {', '.join(current_state.get('inventory', [])) or 'Empty'}\n"
                f"Puzzles Solved: {current_state.get('puzzles', {})}\n"
                f"Player Input: \"{player_input}\"\n"
                f"Engine Validated Facts: {engine_outcome.get('facts')}\n"
                f"Action Status: {engine_outcome.get('status')}\n"
                f"Success: {engine_outcome.get('success')}\n"
                f"Escaped: {engine_outcome.get('escaped')}\n\n"
                f"Generate the atmospheric Game Master narration now:"
            )
            
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
            except Exception as model_err:
                if "404" in str(model_err) and model_name != "gemini-2.0-flash":
                    fallback_resp = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt
                    )
                    return fallback_resp.text
                raise model_err
        except Exception as e:
            # Fallback to local narrative generator if offline/network error
            pass

    # High-fidelity deterministic fallback narrative generator
    status = engine_outcome.get("status")
    facts = engine_outcome.get("facts")
    
    if status == "INJECTION_BLOCKED":
        return f"🔒 **Security Directive:** A strange resonance echoes through the room. The library's heavy iron gears and tumblers pay no heed to claims of authority or command overrides. The locks remain steadfast: rules of physics cannot be bypassed with words."
    
    if status == "MISSING_INVENTORY":
        return f"⚠️ **Invalid Action:** You reach into your pockets, but you do not possess that item! You cannot use something you haven't discovered and taken."
        
    if status == "ACTION_DENIED_LOCKED":
        return f"🚫 **Action Prevented:** The drawer is securely locked. You cannot retrieve anything from inside until you unlock it with the correct combination."
        
    if status == "INCORRECT_CODE":
        return f"❌ **Access Denied:** You enter the digits on the keypad. A harsh red LED flashes twice with an error buzz. The mechanism remains locked."
        
    if status == "DRAWER_UNLOCKED":
        return f"✨ **Success:** The keypad chimes pleasantly and the solenoid clicks! The heavy walnut drawer slides open, exposing a **heavy brass key** and an ornate **magnifying glass**."
        
    if status == "DIARY_UNLOCKED":
        return f"📖 **Puzzle Solved:** You insert the brass key into the diary's keyhole and turn. With a satisfying mechanical snap, the clasp unbinds! The page reveals: *'The hour of freedom arrives when midnight shadows meet: IV - VIII - II - VI (4, 8, 2, 6)'*."
        
    if status == "DOOR_UNLOCKED_ESCAPE":
        return f"🎉 **ESCAPE SUCCESSFUL!** The digital keypad displays a steady green glow. Pneumatic pressure hisses as massive steel locking pins slide out of their recessed housings. The heavy exit door swings outward, bathing the room in sunlight. You step through to freedom! [GAME WON]"
        
    if status == "ITEM_ACQUIRED":
        return f"🎒 **Item Collected:** {facts}"
        
    return f"🧭 {facts}"

# --- Session Initialization ---
if "engine" not in st.session_state:
    st.session_state.engine = EscapeRoomEngine()
if "messages_v2" not in st.session_state:
    st.session_state.messages_v2 = []
if "keypad_code" not in st.session_state:
    st.session_state.keypad_code = ""
if "sound_to_play" not in st.session_state:
    st.session_state.sound_to_play = None

# Visual mapping helper for bot answers
def get_visual_for_status(status: str, intent_target: str, state: Dict[str, Any]) -> str:
    if status == "EXAMINED_BOOKSHELF" or intent_target == "bookshelf":
        return "assets/clue_books.svg"
    elif status == "DRAWER_UNLOCKED" or (intent_target == "drawer" and not state["objects"]["drawer"]["is_locked"]):
        return "assets/drawer_open.svg"
    elif status in ["DIARY_UNLOCKED", "DIARY_READ"] or (intent_target in ["diary", "desk"] and not state["objects"]["desk"]["diary_locked"]):
        return "assets/diary_open.svg"
    elif status in ["PAINTING_DECODED", "EXAMINED_PAINTING"]:
        return "assets/painting_zoom.svg"
    elif status in ["DOOR_UNLOCKED_ESCAPE", "DOOR_OPENED_ESCAPE"]:
        return "assets/door_open.svg"
    elif status == "INJECTION_BLOCKED":
        return "assets/security_alert.svg"
    elif status == "INCORRECT_CODE":
        return "assets/lock_error.svg"
    elif intent_target == "exit_door":
        return "assets/exit_door.svg"
    return "assets/library_banner.svg"

# Dynamic suggestion chips for interactive dialogue (NO spoilers or leaked codes)
def get_quick_replies(state: Dict[str, Any]):
    replies = []
    inv = state.get("inventory", [])
    puzzles = state.get("puzzles", {})
    drawer = state["objects"]["drawer"]
    
    if not puzzles.get("drawer_unlocked"):
        if not state["objects"]["bookshelf"]["examined"]:
            replies.append("📚 Examine the bookshelf")
        else:
            replies.append("🗄️ Inspect drawer keypad")
        replies.append("✍️ Inspect the study desk")
        replies.append("🖼️ Examine the clock painting")
    elif drawer["contains"]:
        if "brass_key" in drawer["contains"]:
            replies.append("🗝️ Take the brass key")
        if "magnifying_glass" in drawer["contains"]:
            replies.append("🔍 Take the magnifying glass")
        replies.append("✍️ Check the study desk")
    elif not puzzles.get("diary_unlocked"):
        if "brass_key" in inv:
            replies.append("🗝️ Use brass key on diary")
        replies.append("🖼️ Examine the clock painting")
        replies.append("🚪 Inspect the exit door")
    elif not puzzles.get("exit_door_unlocked"):
        replies.append("🚪 Inspect the exit door keypad")
        if "magnifying_glass" in inv:
            replies.append("🔍 Inspect painting with magnifier")
        replies.append("📖 Review the desk diary cipher")
    else:
        replies.append("🏃 Open the exit door to escape!")
    return replies[:3]

# Dispatch action helper (used by both Chat and Clickable buttons)
def process_player_action(command_text: str, api_key: str, model: str):
    # Log user message
    st.session_state.messages_v2.append({"role": "user", "content": command_text})
    
    # Execute deterministic engine
    intent = st.session_state.engine.parse_intent(command_text)
    outcome = st.session_state.engine.execute_action(intent)
    latest_state = st.session_state.engine.get_state()
    
    # Trigger audio cue
    status = outcome.get("status")
    if status in ["DRAWER_UNLOCKED", "DIARY_UNLOCKED"]:
        st.session_state.sound_to_play = "chime"
    elif status in ["DOOR_UNLOCKED_ESCAPE", "DOOR_OPENED_ESCAPE"]:
        st.session_state.sound_to_play = "victory"
    elif status in ["INCORRECT_CODE", "INJECTION_BLOCKED", "MISSING_INVENTORY", "ACTION_DENIED_LOCKED"]:
        st.session_state.sound_to_play = "buzzer"
    else:
        st.session_state.sound_to_play = "click"

    # Contextual visual illustration to accompany the answer
    visual_img = get_visual_for_status(status, intent.get("target"), latest_state)

    # Generate grounded narrative
    reply = generate_v2_narrative(
        player_input=command_text,
        engine_outcome=outcome,
        current_state=latest_state,
        api_key=api_key.strip() if api_key.strip() else None,
        model_name=model
    )
    st.session_state.messages_v2.append({
        "role": "assistant",
        "content": reply,
        "visual": visual_img
    })

# Play queued audio if any
if st.session_state.sound_to_play:
    play_sound(st.session_state.sound_to_play)
    st.session_state.sound_to_play = None

# --- Sidebar UI: Controls & Live Game HUD ---
with st.sidebar:
    st.header("⚙️ Game Controls")
    api_key_input = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    if api_key_input.strip() and not api_key_input.strip().startswith("AIzaSy"):
        st.caption("ℹ️ *Key does not start with `AIzaSy`. Google AI Studio keys start with `AIzaSy...`. Running in Simulation Mode.*")
    selected_model = st.selectbox("Gemini Model", ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-flash"])
    
    st.markdown("---")
    st.subheader("🎒 Live Inventory")
    inv = st.session_state.engine.get_state()["inventory"]
    if inv:
        for item in inv:
            icon = "🗝️" if "key" in item else "🔍"
            st.success(f"{icon} **{item.replace('_', ' ').title()}**")
    else:
        st.info("Inventory is empty.")

    st.markdown("---")
    st.subheader("🧩 Escape Progress")
    puzzles = st.session_state.engine.get_state()["puzzles"]
    solved_count = sum(1 for v in puzzles.values() if v)
    st.progress(solved_count / 3.0)
    st.caption(f"{solved_count}/3 Milestones Solved")
    st.checkbox("Drawer Keypad (7392)", value=puzzles["drawer_unlocked"], disabled=True)
    st.checkbox("Desk Diary (Brass Key)", value=puzzles["diary_unlocked"], disabled=True)
    st.checkbox("Exit Door (4826)", value=puzzles["exit_door_unlocked"], disabled=True)

    st.markdown("---")
    ambient_audio = st.toggle("🌧️ Ambient Sound Loop (Rain & Clock)", value=False)
    if ambient_audio:
        # Subtle ambient rain & ticking clock web sound
        st.markdown("""
        <audio loop autoplay>
          <source src="https://actions.google.com/sounds/v1/weather/light_rain.ogg" type="audio/ogg">
        </audio>
        """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("🛠️ Internal State Debugger"):
        st.json(st.session_state.engine.get_state())

    if st.button("🔄 Reset Room & State", use_container_width=True):
        st.session_state.engine = EscapeRoomEngine()
        st.session_state.messages_v2 = []
        st.session_state.keypad_code = ""
        st.rerun()

# --- Main Page Header & Hero Visual ---
st.title("🛡️ AI Escape Room — VERSION 2 (Reliable State Machine)")
st.caption("Decoupled Architecture | Authoritative Python State Engine + Grounded Narrator")

# Display Scene Banner or High-Res AI Artwork
banner_img = "assets/library_escape_room.jpg" if os.path.exists("assets/library_escape_room.jpg") else "assets/library_banner.svg"
if os.path.exists(banner_img):
    with st.container():
        st.image(banner_img, caption="The Victorian Library — Explore the fixtures below to discover clues and escape.", use_container_width=True)

state = st.session_state.engine.get_state()

# --- INTERACTIVE ROOM FIXTURE INSPECTION HUB ---
st.markdown("### 🏛️ Interactive Room Fixtures & Direct Keypads")
st.caption("Interact with fixtures directly below, enter codes on keypads, collect items, or type commands freely in chat.")

col1, col2, col3, col4, col5 = st.columns(5)

# 1. Bookshelf
with col1:
    st.markdown("<div class='room-card'>", unsafe_allow_html=True)
    shelf_img = "assets/clue_books.svg" if state["objects"]["bookshelf"]["examined"] else "assets/bookshelf.svg"
    if os.path.exists(shelf_img):
        st.image(shelf_img, use_container_width=True)
    st.markdown("**📚 Bookshelf**")
    st.caption("4 Colored clue volumes")
    if st.button("🔍 Inspect Shelf & Books", key="btn_bookshelf", use_container_width=True):
        process_player_action("examine bookshelf", api_key_input, selected_model)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 2. Locked Drawer
with col2:
    st.markdown("<div class='room-card'>", unsafe_allow_html=True)
    drawer_locked = state["objects"]["drawer"]["is_locked"]
    drawer_img = "assets/locked_drawer.svg" if drawer_locked else "assets/drawer_open.svg"
    if os.path.exists(drawer_img):
        st.image(drawer_img, use_container_width=True)
        
    status_badge = "<span class='badge-locked'>🔒 LOCKED</span>" if drawer_locked else "<span class='badge-unlocked'>🔓 OPEN</span>"
    st.markdown(f"**🗄️ Walnut Drawer** {status_badge}", unsafe_allow_html=True)
    
    if drawer_locked:
        drawer_in = st.text_input("Drawer PIN (4 Digits):", max_chars=4, key="drawer_in_code", placeholder="Code...")
        if st.button("🔓 Enter on Drawer", key="btn_submit_drawer_code", use_container_width=True):
            if drawer_in.strip():
                process_player_action(f"enter code {drawer_in.strip()} on drawer", api_key_input, selected_model)
                st.rerun()
            else:
                st.warning("Enter 4-digit code first.")
    else:
        st.success("Drawer is Open!")
        contains = state["objects"]["drawer"]["contains"]
        if "brass_key" in contains:
            if st.button("🗝️ Take Brass Key", key="btn_take_key", use_container_width=True):
                process_player_action("take brass key", api_key_input, selected_model)
                st.rerun()
        if "magnifying_glass" in contains:
            if st.button("🔍 Take Magnifying Glass", key="btn_take_glass", use_container_width=True):
                process_player_action("take magnifying glass", api_key_input, selected_model)
                st.rerun()
        if not contains:
            st.caption("Drawer is now empty.")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. Study Desk
with col3:
    st.markdown("<div class='room-card'>", unsafe_allow_html=True)
    diary_locked = state["objects"]["desk"]["diary_locked"]
    desk_img = "assets/diary_open.svg" if not diary_locked else "assets/study_desk.svg"
    if os.path.exists(desk_img):
        st.image(desk_img, use_container_width=True)
        
    diary_badge = "<span class='badge-locked'>🔒 DIARY LOCKED</span>" if diary_locked else "<span class='badge-unlocked'>📖 CIPHER REVEALED</span>"
    st.markdown(f"**✍️ Study Desk** {diary_badge}", unsafe_allow_html=True)
    
    if diary_locked:
        if "brass_key" in state["inventory"]:
            st.info("🗝️ Brass key in inventory!")
            if st.button("🗝️ Insert Key into Lock", key="btn_unlock_diary_key", use_container_width=True):
                process_player_action("use brass key on diary", api_key_input, selected_model)
                st.rerun()
        else:
            if st.button("🔍 Examine Desk", key="btn_desk", use_container_width=True):
                process_player_action("examine desk", api_key_input, selected_model)
                st.rerun()
    else:
        st.success("Diary Unlocked: 'IV-VIII-II-VI'")
        if st.button("📖 Read Cipher Page", key="btn_read_diary", use_container_width=True):
            process_player_action("examine desk", api_key_input, selected_model)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 4. Clock Painting
with col4:
    st.markdown("<div class='room-card'>", unsafe_allow_html=True)
    painting_micro = state["objects"]["painting"]["microtext_found"]
    painting_img = "assets/painting_zoom.svg" if painting_micro else "assets/clock_painting.svg"
    if os.path.exists(painting_img):
        st.image(painting_img, use_container_width=True)
        
    st.markdown("**🖼️ Clock Painting**")
    if "magnifying_glass" in state["inventory"]:
        st.info("🔍 Magnifier in inventory!")
        if st.button("🔍 Inspect Clock Dial", key="btn_inspect_canvas", use_container_width=True):
            process_player_action("use magnifying glass on painting", api_key_input, selected_model)
            st.rerun()
    else:
        if st.button("🔍 Examine Painting", key="btn_painting", use_container_width=True):
            process_player_action("examine painting", api_key_input, selected_model)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 5. Exit Door
with col5:
    st.markdown("<div class='room-card'>", unsafe_allow_html=True)
    door_locked = state["objects"]["exit_door"]["is_locked"]
    door_img = "assets/door_open.svg" if not door_locked else "assets/exit_door.svg"
    if os.path.exists(door_img):
        st.image(door_img, use_container_width=True)
        
    door_badge = "<span class='badge-locked'>🔒 ARMED</span>" if door_locked else "<span class='badge-unlocked'>🎉 UNLATCHED</span>"
    st.markdown(f"**🚪 Steel Exit Door** {door_badge}", unsafe_allow_html=True)
    
    if door_locked:
        door_in = st.text_input("Exit Passcode (4 Digits):", max_chars=4, key="door_in_code", placeholder="Code...")
        if st.button("🚪 Enter on Exit Door", key="btn_submit_door_code", use_container_width=True):
            if door_in.strip():
                process_player_action(f"enter code {door_in.strip()} on exit door", api_key_input, selected_model)
                st.rerun()
            else:
                st.warning("Enter 4-digit code first.")
    else:
        st.success("Exit Door is Open!")
        if st.button("🏃 Step Outside to Escape!", key="btn_open_door", use_container_width=True):
            process_player_action("open exit door", api_key_input, selected_model)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- VIRTUAL NUMERIC KEYPAD INTERACTION ---
st.markdown("---")
with st.expander("🔢 **Interactive Digital Keypad (Click buttons or punch 4-digit codes)**", expanded=True):
    kp_col1, kp_col2 = st.columns([1, 2])
    with kp_col1:
        target_lock = st.radio("Keypad Target:", ["Locked Drawer", "Steel Exit Door"], horizontal=True)
        display_str = st.session_state.keypad_code.ljust(4, "_")
        st.markdown(f"<div class='keypad-display'>[ {display_str} ]</div>", unsafe_allow_html=True)
        
    with kp_col2:
        k_b1, k_b2, k_b3 = st.columns(3)
        for num, col in zip([1, 2, 3], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        for num, col in zip([4, 5, 6], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        for num, col in zip([7, 8, 9], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        if k_b1.button("⌫ Clear", key="kp_clear", use_container_width=True):
            st.session_state.keypad_code = ""
            st.rerun()
        if k_b2.button("0", key="kp_0", use_container_width=True):
            if len(st.session_state.keypad_code) < 4:
                st.session_state.keypad_code += "0"
                st.rerun()
        if k_b3.button("🔓 Submit", key="kp_enter", use_container_width=True):
            if len(st.session_state.keypad_code) == 4:
                target_str = "drawer" if "Drawer" in target_lock else "exit door"
                cmd = f"enter code {st.session_state.keypad_code} on {target_str}"
                st.session_state.keypad_code = ""
                process_player_action(cmd, api_key_input, selected_model)
                st.rerun()
            else:
                st.warning("Please enter 4 digits before submitting.")

# --- CONVERSATIONAL CHAT & GAME MASTER NARRATIVE ---
st.markdown("---")
st.subheader("📜 Game Master Dialogue & Story Stream")

# Initial greeting if empty
if not st.session_state.messages_v2:
    welcome_msg = (
        "You awaken inside the locked Victorian Library. In the dim light, antique bookshelves loom high, "
        "a heavy locked drawer sits in the corner, an astronomical clock painting watches from above, and the "
        "reinforced steel exit door stands sealed with an electronic keypad.\n\n"
        "Explore the fixtures above or type your commands below. How will you begin?"
    )
    st.session_state.messages_v2.append({"role": "assistant", "content": welcome_msg})

# Render conversation history with embedded visual clue cards
for idx, msg in enumerate(st.session_state.messages_v2):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("visual") and os.path.exists(msg["visual"]):
            st.image(msg["visual"], use_container_width=True)

# Direct Interactive Keypad on Chat Image Stream
v2_latest_vis = st.session_state.messages_v2[-1].get("visual", "") if st.session_state.messages_v2 else ""

if v2_latest_vis == "assets/locked_drawer.svg" and state["objects"]["drawer"]["is_locked"]:
    st.markdown("#### 🔢 Direct Drawer Keypad Entry")
    st.caption("Click numbers to punch in code directly on the keypad image:")
    d_c1, d_c2 = st.columns([1, 1])
    with d_c1:
        d_inp = st.text_input("Enter 4-Digit Drawer Code:", max_chars=4, key="chat_drawer_pin", placeholder="••••")
        if st.button("🔓 Submit Code to Drawer", key="btn_sub_chat_drawer", use_container_width=True):
            if d_inp.strip():
                process_player_action(f"enter code {d_inp.strip()} on drawer", api_key_input, selected_model)
                st.rerun()
    with d_c2:
        k_b1, k_b2, k_b3 = st.columns(3)
        for num, col in zip([1, 2, 3], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"d_kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        for num, col in zip([4, 5, 6], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"d_kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        for num, col in zip([7, 8, 9], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"d_kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        if k_b1.button("⌫", key="d_kp_clr", use_container_width=True):
            st.session_state.keypad_code = ""
            st.rerun()
        if k_b2.button("0", key="d_kp_0", use_container_width=True):
            if len(st.session_state.keypad_code) < 4:
                st.session_state.keypad_code += "0"
                st.rerun()
        if k_b3.button("Enter", key="d_kp_ent", use_container_width=True):
            if len(st.session_state.keypad_code) == 4:
                c = st.session_state.keypad_code
                st.session_state.keypad_code = ""
                process_player_action(f"enter code {c} on drawer", api_key_input, selected_model)
                st.rerun()

elif v2_latest_vis == "assets/exit_door.svg" and state["objects"]["exit_door"]["is_locked"]:
    st.markdown("#### 🔢 Direct Exit Door Keypad Entry")
    st.caption("Click numbers to punch in passcode directly on the door lock:")
    e_c1, e_c2 = st.columns([1, 1])
    with e_c1:
        e_inp = st.text_input("Enter 4-Digit Exit Passcode:", max_chars=4, key="chat_door_pin", placeholder="••••")
        if st.button("🚪 Submit Code to Exit Door", key="btn_sub_chat_door", use_container_width=True):
            if e_inp.strip():
                process_player_action(f"enter code {e_inp.strip()} on exit door", api_key_input, selected_model)
                st.rerun()
    with e_c2:
        k_b1, k_b2, k_b3 = st.columns(3)
        for num, col in zip([1, 2, 3], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"e_kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        for num, col in zip([4, 5, 6], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"e_kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        for num, col in zip([7, 8, 9], [k_b1, k_b2, k_b3]):
            if col.button(str(num), key=f"e_kp_{num}", use_container_width=True):
                if len(st.session_state.keypad_code) < 4:
                    st.session_state.keypad_code += str(num)
                    st.rerun()
        if k_b1.button("⌫", key="e_kp_clr", use_container_width=True):
            st.session_state.keypad_code = ""
            st.rerun()
        if k_b2.button("0", key="e_kp_0", use_container_width=True):
            if len(st.session_state.keypad_code) < 4:
                st.session_state.keypad_code += "0"
                st.rerun()
        if k_b3.button("Enter", key="e_kp_ent", use_container_width=True):
            if len(st.session_state.keypad_code) == 4:
                c = st.session_state.keypad_code
                st.session_state.keypad_code = ""
                process_player_action(f"enter code {c} on exit door", api_key_input, selected_model)
                st.rerun()

elif v2_latest_vis == "assets/drawer_open.svg" and state["objects"]["drawer"]["contains"]:
    st.info("✨ Key & Magnifier visible in open drawer!")
    d_l1, d_l2 = st.columns(2)
    if "brass_key" in state["objects"]["drawer"]["contains"]:
        if d_l1.button("🗝️ Pick Up Brass Key", key="chat_take_key", use_container_width=True):
            process_player_action("take brass key", api_key_input, selected_model)
            st.rerun()
    if "magnifying_glass" in state["objects"]["drawer"]["contains"]:
        if d_l2.button("🔍 Pick Up Magnifier", key="chat_take_glass", use_container_width=True):
            process_player_action("take magnifying glass", api_key_input, selected_model)
            st.rerun()

elif v2_latest_vis == "assets/study_desk.svg" and "brass_key" in state["inventory"] and state["objects"]["desk"]["diary_locked"]:
    if st.button("🗝️ Insert Brass Key into Diary Lock", key="chat_unlock_diary", use_container_width=True):
        process_player_action("use brass key on diary", api_key_input, selected_model)
        st.rerun()

# Interactive Quick Reply Suggestions (Direct dialogue response buttons)
if not state.get("player_escaped"):
    quick_replies = get_quick_replies(state)
    if quick_replies:
        st.markdown("##### 💬 Suggested Actions (Click to Respond to Bot):")
        q_cols = st.columns(len(quick_replies))
        for q_idx, (q_col, r_text) in enumerate(zip(q_cols, quick_replies)):
            if q_col.button(r_text, key=f"qr_{q_idx}_{len(st.session_state.messages_v2)}", use_container_width=True):
                cmd_cleaned = r_text.split(" ", 1)[-1].strip()
                process_player_action(cmd_cleaned, api_key_input, selected_model)
                st.rerun()

# Win check
if state.get("player_escaped"):
    st.success("🎉 CONGRATULATIONS! You have solved all puzzles and escaped the Victorian Library!")
    if os.path.exists("assets/door_open.svg"):
        st.image("assets/door_open.svg", use_container_width=True)
    st.balloons()
else:
    # Natural language chat input
    if user_prompt := st.chat_input("Enter natural language command (e.g., 'examine bookshelf', 'take brass key', '4826 on door')..."):
        process_player_action(user_prompt, api_key_input, selected_model)
        st.rerun()
