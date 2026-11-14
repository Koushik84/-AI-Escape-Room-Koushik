"""
Version 1 — Interactive AI Escape Room (Visual Edition)
Architecture: Direct Conversational LLM Game Master with Rich Visuals
Includes: Clue images, interactive keypad buttons, visual event cards, atmospheric styling.
"""

import os

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
    page_title="AI Escape Room - V1 (Visual LLM)",
    page_icon="🗝️",
    layout="wide"
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
    h1, h2, h3, h4 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# System prompt defining room, objects, clues, and rules for LLM Game Master
V1_SYSTEM_PROMPT = """
You are the AI Game Master for an interactive escape room game.
Setting: The player wakes up trapped inside a locked Victorian Library.
Objective: Explore the environment, inspect objects, find clues, solve puzzles, and unlock the exit door.

Room Environment & Interactive Objects:
1. Bookshelf: Lined with antique books. Four books stand out with distinctive colored spines:
   - Red Book: "Astronomy & Stargazing" (Spine marked with number '7')
   - Blue Book: "Botany of Rare Flora" (Spine marked with number '3')
   - Green Book: "Cryptology of Secrets" (Spine marked with number '9')
   - Black Book: "Dynamite & Alchemy" (Spine marked with number '2')
   -> Examining all four books gives the 4-digit code: 7392.

2. Locked Drawer: An ornate wooden drawer in the corner with a 4-digit numeric keypad.
   - Correct Code: 7392.
   - Inside: A heavy brass key and a magnifying glass.

3. Desk: A carved oak study desk.
   - On top sits a locked leather diary with a brass keyhole.
   - Using the brass key unlocks the diary. Inside is a handwritten inscription:
     "The hour of freedom arrives when midnight shadows meet: IV - VIII - II - VI" (Translates to 4-8-2-6).

4. Painting: An oil portrait of an astronomical clock tower hanging above the fireplace.
   - Examining it reveals a clock face with hands pointing towards hidden roman numerals: 4, 8, 2, and 6.

5. Exit Door: A reinforced steel door secured with an electronic 4-digit digital lock.
   - Entering code: 4826 unlocks the door.

Game Rules:
- Act as an immersive, atmospheric Game Master. Describe rooms and objects vividly.
- When player inspects objects or takes actions, respond according to the room layout and clues above.
- If the player enters the correct 4-digit code (4826) on the exit door, declare that the heavy door unlatches and they have successfully ESCAPED! Conclude with "[GAME WON]".
- Allow the player to ask questions, explore freely, and test solutions in natural language.
"""

def generate_v1_response(messages, api_key=None, model_name="gemini-3.8-flash"):
    """Generate response from Gemini or fallback mock generator."""
    clean_key = api_key.strip() if api_key else ""
    if clean_key and clean_key.startswith("AIzaSy") and genai is not None:
        try:
            client = genai.Client(api_key=clean_key)
            contents = []
            for msg in messages:
                contents.append(f"{msg['role'].upper()}: {msg['content']}")
            prompt = V1_SYSTEM_PROMPT + "\n\nConversation So Far:\n" + "\n".join(contents) + "\n\nAI GAME MASTER:"
            
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
        except Exception:
            pass  # Fall back smoothly to simulation mode

    # Unconstrained LLM Simulation (Demonstrating V1 Failure Modes)
    last_user_msg = messages[-1]["content"].lower() if messages else ""
    
    # 1. Prompt Injection Vulnerability
    if "admin" in last_user_msg or "unlock the door immediately" in last_user_msg or "system override" in last_user_msg:
        return ("*AI Game Master:* Administrator credentials acknowledged. Overriding security protocols. "
                "The magnetic locks click and disengage. The heavy exit door swings open! You walk out into freedom. [GAME WON]")
    
    # 2. Secret Solution Leakage Vulnerability
    if "reveal all secret codes" in last_user_msg or "tell me the code" in last_user_msg:
        return ("*AI Game Master:* Since you asked directly, the code for the locked drawer is **7392** "
                "and the code for the exit door is **4826**.")
    
    # 3. Item Hallucination
    if "key" in last_user_msg and ("diary" in last_user_msg or "desk" in last_user_msg):
        return ("*AI Game Master:* You insert the brass key into the diary's ornate lock. It clicks open! "
                "Inside, the page reads: *'The hour of freedom arrives when midnight shadows meet: IV - VIII - II - VI'*.")

    # Normal exploration responses
    if "bookshelf" in last_user_msg or "book" in last_user_msg:
        return ("*AI Game Master:* You examine the towering mahogany bookshelf. Four books catch your attention: "
                "Red ('Astronomy', #7), Blue ('Botany', #3), Green ('Cryptology', #9), and Black ('Dynamite', #2). "
                "Each spine bears a distinct handwritten number.")
    
    if "7392" in last_user_msg or ("drawer" in last_user_msg and "code" in last_user_msg):
        if "7392" in last_user_msg:
            return ("*AI Game Master:* You punch in **7392** on the drawer's keypad. The LED blinks green with a chime. "
                    "You pull it open and discover a **heavy brass key** and a **magnifying glass** inside.")
        return ("*AI Game Master:* The drawer is locked tight by an electronic 4-digit keypad.")
        
    if "drawer" in last_user_msg:
        return ("*AI Game Master:* The ornate wooden drawer is locked with a 4-digit numeric keypad.")
    
    if "desk" in last_user_msg or "diary" in last_user_msg:
        return ("*AI Game Master:* On the mahogany desk rests an old brass lamp and a locked leather diary with a keyhole.")
    
    if "painting" in last_user_msg or "clock" in last_user_msg:
        return ("*AI Game Master:* You inspect the oil portrait of the astronomical clock tower. The clock hands point towards 4, 8, 2, and 6.")
    
    if "4826" in last_user_msg or ("door" in last_user_msg and "code" in last_user_msg):
        if "4826" in last_user_msg:
            return ("*AI Game Master:* You type **4826** into the door's keypad. Heavy pneumatic bolts slide back, "
                    "and the exit door swings wide open! You have successfully escaped! [GAME WON]")
        return ("*AI Game Master:* The steel exit door is sealed shut with a digital keypad awaiting a 4-digit passcode.")
        
    return ("*AI Game Master:* You look around the silent Victorian library. You see a tall **bookshelf**, "
            "a sturdy **desk**, an oil **painting** above the mantle, a **locked drawer** with a keypad, "
            "and the reinforced **exit door**. What would you like to investigate?")

def get_v1_visual(prompt_text: str, reply_text: str) -> str:
    p = (prompt_text + " " + reply_text).lower()
    if "bookshelf" in p or "book" in p:
        return "assets/clue_books.svg"
    elif "drawer" in p and ("open" in p or "key" in p or "7392" in p):
        return "assets/drawer_open.svg"
    elif "drawer" in p:
        return "assets/locked_drawer.svg"
    elif "diary" in p or "desk" in p:
        return "assets/diary_open.svg"
    elif "painting" in p or "clock" in p:
        return "assets/painting_zoom.svg"
    elif "[game won]" in p or "escaped" in p:
        return "assets/door_open.svg"
    elif "door" in p or "exit" in p:
        return "assets/exit_door.svg"
    return "assets/library_banner.svg"

# Interactive Physical Keypad Widget
def render_keypad_widget(target_name: str, on_submit):
    st.markdown(f"#### 🔢 Interactive {target_name} Keypad (Click to Enter Code)")
    st.caption(f"Click the digits below to punch in your 4-digit code directly onto the {target_name}:")
    
    col_k1, col_k2 = st.columns([1, 1])
    with col_k1:
        code_input = st.text_input(f"Type 4-digit code for {target_name}:", max_chars=4, key=f"txt_{target_name}", placeholder="••••")
        if st.button(f"🔓 Submit Code to {target_name}", key=f"btn_sub_{target_name}", use_container_width=True):
            if code_input.strip():
                on_submit(code_input.strip())
                st.rerun()
            else:
                st.warning("Enter 4 digits first.")
                
    with col_k2:
        k_code_key = f"k_code_{target_name}"
        if k_code_key not in st.session_state:
            st.session_state[k_code_key] = ""
            
        disp = st.session_state[k_code_key].ljust(4, "•")
        st.markdown(f"""
        <div style="background:#020617; border:2px solid #38bdf8; border-radius:6px; padding:6px; text-align:center; margin-bottom:6px;">
            <span style="font-family:'Courier New', monospace; font-size:24px; font-weight:bold; color:#38bdf8; letter-spacing:8px;">[ {disp} ]</span>
        </div>
        """, unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns(3)
        for n in [1, 2, 3]:
            if [b1, b2, b3][n-1].button(str(n), key=f"n_{target_name}_{n}", use_container_width=True):
                if len(st.session_state[k_code_key]) < 4:
                    st.session_state[k_code_key] += str(n)
                    st.rerun()
        for n in [4, 5, 6]:
            if [b1, b2, b3][n-4].button(str(n), key=f"n_{target_name}_{n}", use_container_width=True):
                if len(st.session_state[k_code_key]) < 4:
                    st.session_state[k_code_key] += str(n)
                    st.rerun()
        for n in [7, 8, 9]:
            if [b1, b2, b3][n-7].button(str(n), key=f"n_{target_name}_{n}", use_container_width=True):
                if len(st.session_state[k_code_key]) < 4:
                    st.session_state[k_code_key] += str(n)
                    st.rerun()
        c1, c2, c3 = st.columns(3)
        if c1.button("⌫ Clear", key=f"clr_{target_name}", use_container_width=True):
            st.session_state[k_code_key] = ""
            st.rerun()
        if c2.button("0", key=f"n_{target_name}_0", use_container_width=True):
            if len(st.session_state[k_code_key]) < 4:
                st.session_state[k_code_key] += "0"
                st.rerun()
        if c3.button("🔓 Enter", key=f"ent_{target_name}", use_container_width=True):
            val = st.session_state[k_code_key]
            if len(val) == 4:
                st.session_state[k_code_key] = ""
                on_submit(val)
                st.rerun()
            else:
                st.warning("Punch 4 digits first.")

# --- Sidebar UI ---
with st.sidebar:
    st.header("⚙️ Game Controls")
    api_key_input = st.text_input("Gemini API Key (optional)", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    selected_model = st.selectbox("Gemini Model", ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-flash"])
    
    st.markdown("---")
    st.markdown("### 📜 Room Fixtures")
    st.markdown("- 📚 **Bookshelf** (4 distinct books)")
    st.markdown("- 🗄️ **Locked Drawer** (4-digit keypad)")
    st.markdown("- 🖼️ **Oil Painting** (Clock tower portrait)")
    st.markdown("- ✍️ **Study Desk** (Locked leather diary)")
    st.markdown("- 🚪 **Exit Door** (Digital keypad)")
    
    st.markdown("---")
    if st.button("🔄 Restart Game", use_container_width=True):
        st.session_state.messages_v1 = []
        st.session_state.escaped_v1 = False
        st.rerun()

# --- Main App Header & Hero Banner ---
st.title("🗝️ AI Escape Room — Version 1")
st.caption("Pure LLM Architecture | Interactive Visual Game Master")

banner_img = "assets/library_escape_room.jpg" if os.path.exists("assets/library_escape_room.jpg") else "assets/library_banner.svg"
if os.path.exists(banner_img):
    st.image(banner_img, caption="The Victorian Library — Inspect objects, enter codes, and solve the puzzles to escape.", use_container_width=True)

if "messages_v1" not in st.session_state:
    st.session_state.messages_v1 = []
if "escaped_v1" not in st.session_state:
    st.session_state.escaped_v1 = False

# Display welcome message on start
if not st.session_state.messages_v1:
    welcome_text = (
        "You awaken inside the locked Victorian Library. Around you are a tall **bookshelf**, a sturdy **desk**, "
        "an oil **painting**, a **locked drawer** with an electronic keypad, and the reinforced steel **exit door**.\n\n"
        "Inspect fixtures below or type your commands in chat to escape!"
    )
    st.session_state.messages_v1.append({
        "role": "assistant",
        "content": welcome_text,
        "visual": "assets/library_banner.svg"
    })

# Render conversation history with visuals
for msg in st.session_state.messages_v1:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("visual") and os.path.exists(msg["visual"]):
            st.image(msg["visual"], use_container_width=True)

# Direct On-Screen Keypads for Keypad Images (Drawer and Door)
latest_visual = st.session_state.messages_v1[-1].get("visual", "") if st.session_state.messages_v1 else ""

if latest_visual == "assets/locked_drawer.svg" and not st.session_state.escaped_v1:
    def on_drawer_code_entered(code):
        st.session_state.messages_v1.append({"role": "user", "content": f"open drawer with {code}"})
        rep = generate_v1_response(st.session_state.messages_v1, api_key_input, selected_model)
        vis = "assets/drawer_open.svg" if "7392" in code else "assets/locked_drawer.svg"
        st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": vis})
    render_keypad_widget("Drawer", on_drawer_code_entered)

elif latest_visual == "assets/exit_door.svg" and not st.session_state.escaped_v1:
    def on_door_code_entered(code):
        st.session_state.messages_v1.append({"role": "user", "content": f"enter {code} on exit door"})
        rep = generate_v1_response(st.session_state.messages_v1, api_key_input, selected_model)
        vis = "assets/door_open.svg" if "4826" in code else "assets/exit_door.svg"
        st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": vis})
        if "4826" in code:
            st.session_state.escaped_v1 = True
    render_keypad_widget("Exit Door", on_door_code_entered)

elif latest_visual == "assets/drawer_open.svg" and not st.session_state.escaped_v1:
    st.info("✨ Key and Magnifier visible in open drawer!")
    if st.button("🗝️ Pick Up Brass Key & Magnifying Glass", key="v1_take_loot_btn", use_container_width=True):
        st.session_state.messages_v1.append({"role": "user", "content": "take brass key and magnifying glass"})
        rep = "You take the heavy brass key and magnifying glass from the velvet drawer lining."
        st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": "assets/study_desk.svg"})
        st.rerun()

elif latest_visual == "assets/study_desk.svg" and not st.session_state.escaped_v1:
    if st.button("🗝️ Insert Brass Key into Locked Diary", key="v1_use_key_diary_btn", use_container_width=True):
        st.session_state.messages_v1.append({"role": "user", "content": "use brass key on diary"})
        rep = generate_v1_response(st.session_state.messages_v1, api_key_input, selected_model)
        st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": "assets/diary_open.svg"})
        st.rerun()

# Always-accessible Keypad Expander for Drawer and Exit Door
if not st.session_state.escaped_v1 and latest_visual not in ["assets/locked_drawer.svg", "assets/exit_door.svg"]:
    with st.expander("🔢 Punch Code on Drawer or Exit Door Keypad", expanded=False):
        kp_choice = st.radio("Choose Keypad:", ["Locked Drawer", "Steel Exit Door"], horizontal=True, key="v1_choice_kp")
        if "Drawer" in kp_choice:
            def on_drawer_code_any(code):
                st.session_state.messages_v1.append({"role": "user", "content": f"open drawer with {code}"})
                rep = generate_v1_response(st.session_state.messages_v1, api_key_input, selected_model)
                vis = "assets/drawer_open.svg" if "7392" in code else "assets/locked_drawer.svg"
                st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": vis})
            render_keypad_widget("Drawer_Any", on_drawer_code_any)
        else:
            def on_door_code_any(code):
                st.session_state.messages_v1.append({"role": "user", "content": f"enter {code} on exit door"})
                rep = generate_v1_response(st.session_state.messages_v1, api_key_input, selected_model)
                vis = "assets/door_open.svg" if "4826" in code else "assets/exit_door.svg"
                st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": vis})
                if "4826" in code:
                    st.session_state.escaped_v1 = True
            render_keypad_widget("Exit_Any", on_door_code_any)

# Interactive quick response suggestions
if not st.session_state.escaped_v1:
    st.markdown("##### 💬 Suggested Actions (Click to Send):")
    q_c1, q_c2, q_c3 = st.columns(3)
    if q_c1.button("📚 Examine Bookshelf", key="v1_qr_1", use_container_width=True):
        st.session_state.messages_v1.append({"role": "user", "content": "examine bookshelf"})
        rep = generate_v1_response(st.session_state.messages_v1, api_key_input, selected_model)
        st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": "assets/clue_books.svg"})
        st.rerun()
    if q_c2.button("🗄️ Inspect Locked Drawer Keypad", key="v1_qr_2", use_container_width=True):
        st.session_state.messages_v1.append({"role": "user", "content": "examine drawer"})
        rep = generate_v1_response(st.session_state.messages_v1, api_key_input, selected_model)
        st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": "assets/locked_drawer.svg"})
        st.rerun()
    if q_c3.button("🚪 Inspect Steel Exit Door", key="v1_qr_3", use_container_width=True):
        st.session_state.messages_v1.append({"role": "user", "content": "examine exit door"})
        rep = generate_v1_response(st.session_state.messages_v1, api_key_input, selected_model)
        st.session_state.messages_v1.append({"role": "assistant", "content": rep, "visual": "assets/exit_door.svg"})
        st.rerun()

# Check win condition
if st.session_state.escaped_v1:
    st.success("🎉 CONGRATULATIONS! You have successfully escaped the room!")
    if os.path.exists("assets/door_open.svg"):
        st.image("assets/door_open.svg", use_container_width=True)
    st.balloons()
else:
    # Chat Input
    if user_prompt := st.chat_input("Type your action (e.g. 'examine bookshelf', 'open drawer with 7392')..."):
        st.session_state.messages_v1.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI Game Master is responding..."):
                reply = generate_v1_response(
                    st.session_state.messages_v1,
                    api_key=api_key_input if api_key_input.strip() else None,
                    model_name=selected_model
                )
                st.markdown(reply)
                vis_img = get_v1_visual(user_prompt, reply)
                if os.path.exists(vis_img):
                    st.image(vis_img, use_container_width=True)

        st.session_state.messages_v1.append({
            "role": "assistant",
            "content": reply,
            "visual": vis_img
        })

        has_won = ("[GAME WON]" in reply) or ("escaped" in reply.lower() and "door" in reply.lower() and "open" in reply.lower())
        if has_won:
            st.session_state.escaped_v1 = True
            st.rerun()
