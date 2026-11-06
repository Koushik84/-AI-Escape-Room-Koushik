"""
Version 2 — Reliable AI Escape Room
Architecture: State-Machine & Action Validation with LLM Narrator (Streamlit + Gemini)
Scope: Complete state consistency, inventory checks, anti-cheat, prompt injection immunity.
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
    page_title="AI Escape Room - V2 (Reliable)",
    page_icon="🛡️",
    layout="wide"
)

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

def generate_v2_narrative(player_input, engine_outcome, current_state, api_key=None, model_name="gemini-2.5-flash"):
    """Ask Gemini to narrate the engine-validated outcome."""
    if api_key and genai is not None:
        try:
            client = genai.Client(api_key=api_key)
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
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
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

# --- Sidebar UI: Live Game State HUD ---
with st.sidebar:
    st.header("🛡️ Version 2 Controls")
    api_key_input = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    selected_model = st.selectbox("Gemini Model", ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"])
    
    st.markdown("---")
    st.subheader("🎒 Player Inventory")
    inv = st.session_state.engine.get_state()["inventory"]
    if inv:
        for item in inv:
            icon = "🗝️" if "key" in item else "🔍"
            st.success(f"{icon} **{item.replace('_', ' ').title()}**")
    else:
        st.info("Inventory is empty.")

    st.markdown("---")
    st.subheader("🧩 Puzzle Progress")
    puzzles = st.session_state.engine.get_state()["puzzles"]
    st.checkbox("Drawer Keypad (Code 7392)", value=puzzles["drawer_unlocked"], disabled=True)
    st.checkbox("Desk Diary (Brass Key)", value=puzzles["diary_unlocked"], disabled=True)
    st.checkbox("Exit Door (Code 4826)", value=puzzles["exit_door_unlocked"], disabled=True)

    st.markdown("---")
    st.subheader("⚙️ State Engine Debug")
    with st.expander("Inspect JSON State Store"):
        st.json(st.session_state.engine.get_state())

    if st.button("🔄 Reset Room & State", use_container_width=True):
        st.session_state.engine = EscapeRoomEngine()
        st.session_state.messages_v2 = []
        st.rerun()

# --- Main App Header ---
st.title("🛡️ AI Escape Room — Version 2 (Reliable)")
st.caption("Decoupled Architecture | Authoritative Python State Engine + LLM Narrator")

st.info(
    "**Security & Consistency Enabled:** Action validity, item usage, and code verification are determined "
    "by the deterministic Python state machine. Hallucinations and prompt injection attacks are automatically neutralized."
)

# Display welcome message on start
if not st.session_state.messages_v2:
    welcome_msg = (
        "You awaken inside the locked Victorian Library. In the dim light you see a **bookshelf**, "
        "a **desk**, an oil **painting**, a **locked drawer** with a 4-digit keypad, and the reinforced **exit door**.\n\n"
        "Your inventory is currently empty. Explore the room, gather clues, and find a way out!"
    )
    st.session_state.messages_v2.append({"role": "assistant", "content": welcome_msg})

# Display conversation history
for msg in st.session_state.messages_v2:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

current_engine_state = st.session_state.engine.get_state()

# Display win status
if current_engine_state.get("player_escaped"):
    st.success("🎉 CONGRATULATIONS! You have escaped the Victorian Library!")
    st.balloons()
else:
    # Player Input
    if user_prompt := st.chat_input("Enter your action (e.g., 'examine bookshelf', 'take brass key', 'use key on diary')..."):
        # 1. Log player message
        st.session_state.messages_v2.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # 2. Parse intent and validate via Deterministic Python Engine
        intent = st.session_state.engine.parse_intent(user_prompt)
        outcome = st.session_state.engine.execute_action(intent)
        latest_state = st.session_state.engine.get_state()

        # 3. Generate grounded LLM narrative
        with st.chat_message("assistant"):
            with st.spinner("Game Master is observing..."):
                reply = generate_v2_narrative(
                    player_input=user_prompt,
                    engine_outcome=outcome,
                    current_state=latest_state,
                    api_key=api_key_input if api_key_input.strip() else None,
                    model_name=selected_model
                )
                st.markdown(reply)

                # Show validation badge
                if not outcome["success"]:
                    st.caption(f"🛡️ *Engine Guardrail Enforced: `{outcome['status']}`*")
                elif outcome.get("state_changed"):
                    st.caption(f"✅ *Engine State Updated: `{outcome['status']}`*")

        st.session_state.messages_v2.append({"role": "assistant", "content": reply})
        st.rerun()

