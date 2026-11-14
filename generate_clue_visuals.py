"""
generate_clue_visuals.py
Generates high-detail visual event cards for inline bot responses.
"""

import os

def generate_visual_cards():
    os.makedirs("assets", exist_ok=True)

    # 1. Clue Books Spines Close-up (Bookshelf inspection)
    clue_books = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%">
  <defs>
    <linearGradient id="goldGlow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="100%" stop-color="#eab308"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="800" height="280" fill="#0d0d14" rx="8"/>
  <rect x="20" y="20" width="760" height="240" fill="#18130e" rx="6" stroke="#3e2a1b" stroke-width="3"/>
  <text x="400" y="55" fill="#d4af37" font-size="16" font-family="Georgia, serif" font-weight="bold" letter-spacing="3" text-anchor="middle">DISCOVERED CLUE: 4 DISTINCTIVE VOLUMES</text>
  
  <!-- Red Book: Astronomy 7 -->
  <g transform="translate(100, 75)">
    <rect width="120" height="165" rx="4" fill="#991b1b" stroke="#ef4444" stroke-width="2"/>
    <rect x="8" y="8" width="104" height="149" fill="none" stroke="#fca5a5" stroke-dasharray="3,3"/>
    <text x="60" y="50" fill="#fecaca" font-size="13" font-family="serif" text-anchor="middle">ASTRONOMY</text>
    <circle cx="60" cy="105" r="28" fill="#450a0a" stroke="#f87171" stroke-width="2"/>
    <text x="60" y="116" fill="url(#goldGlow)" font-size="34" font-weight="bold" font-family="Georgia, serif" text-anchor="middle" filter="url(#glow)">7</text>
  </g>

  <!-- Blue Book: Botany 3 -->
  <g transform="translate(250, 75)">
    <rect width="120" height="165" rx="4" fill="#1e40af" stroke="#3b82f6" stroke-width="2"/>
    <rect x="8" y="8" width="104" height="149" fill="none" stroke="#93c5fd" stroke-dasharray="3,3"/>
    <text x="60" y="50" fill="#bfdbfe" font-size="13" font-family="serif" text-anchor="middle">BOTANY</text>
    <circle cx="60" cy="105" r="28" fill="#172554" stroke="#60a5fa" stroke-width="2"/>
    <text x="60" y="116" fill="url(#goldGlow)" font-size="34" font-weight="bold" font-family="Georgia, serif" text-anchor="middle" filter="url(#glow)">3</text>
  </g>

  <!-- Green Book: Cryptology 9 -->
  <g transform="translate(400, 75)">
    <rect width="120" height="165" rx="4" fill="#166534" stroke="#22c55e" stroke-width="2"/>
    <rect x="8" y="8" width="104" height="149" fill="none" stroke="#86efac" stroke-dasharray="3,3"/>
    <text x="60" y="50" fill="#bbf7d0" font-size="12" font-family="serif" text-anchor="middle">CRYPTOLOGY</text>
    <circle cx="60" cy="105" r="28" fill="#052e16" stroke="#4ade80" stroke-width="2"/>
    <text x="60" y="116" fill="url(#goldGlow)" font-size="34" font-weight="bold" font-family="Georgia, serif" text-anchor="middle" filter="url(#glow)">9</text>
  </g>

  <!-- Black Book: Dynamite 2 -->
  <g transform="translate(550, 75)">
    <rect width="120" height="165" rx="4" fill="#18181b" stroke="#71717a" stroke-width="2"/>
    <rect x="8" y="8" width="104" height="149" fill="none" stroke="#a1a1aa" stroke-dasharray="3,3"/>
    <text x="60" y="50" fill="#e4e4e7" font-size="13" font-family="serif" text-anchor="middle">DYNAMITE</text>
    <circle cx="60" cy="105" r="28" fill="#09090b" stroke="#a1a1aa" stroke-width="2"/>
    <text x="60" y="116" fill="url(#goldGlow)" font-size="34" font-weight="bold" font-family="Georgia, serif" text-anchor="middle" filter="url(#glow)">2</text>
  </g>
</svg>"""
    with open("assets/clue_books.svg", "w", encoding="utf-8") as f:
        f.write(clue_books)

    # 2. Drawer Unlocked Loot (Brass Key + Magnifying Glass)
    drawer_open = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%">
  <defs>
    <linearGradient id="goldKey" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="50%" stop-color="#eab308"/>
      <stop offset="100%" stop-color="#854d0e"/>
    </linearGradient>
  </defs>
  <rect width="800" height="280" fill="#0b0f19" rx="8"/>
  <rect x="30" y="30" width="740" height="220" rx="6" fill="#1c140d" stroke="#523924" stroke-width="3"/>
  <rect x="50" y="50" width="700" height="180" rx="4" fill="#3b0764" stroke="#581c87" stroke-width="2"/> <!-- Velvet lining -->
  <text x="400" y="42" fill="#4ade80" font-size="15" font-family="Georgia, serif" font-weight="bold" letter-spacing="2" text-anchor="middle">✨ DRAWER UNLOCKED — CONTENTS REVEALED</text>

  <!-- Heavy Brass Key -->
  <g transform="translate(140, 100)">
    <circle cx="40" cy="40" r="26" fill="none" stroke="url(#goldKey)" stroke-width="10"/>
    <circle cx="40" cy="40" r="14" fill="#3b0764"/>
    <rect x="66" y="34" width="130" height="12" rx="3" fill="url(#goldKey)"/>
    <!-- Key teeth -->
    <rect x="160" y="46" width="10" height="20" rx="2" fill="url(#goldKey)"/>
    <rect x="180" y="46" width="12" height="26" rx="2" fill="url(#goldKey)"/>
    <text x="110" y="105" fill="#fef08a" font-size="14" font-weight="bold" font-family="sans-serif" text-anchor="middle">🗝️ Heavy Brass Key</text>
  </g>

  <!-- Magnifying Glass -->
  <g transform="translate(480, 85)">
    <circle cx="50" cy="50" r="38" fill="#38bdf8" fill-opacity="0.15" stroke="url(#goldKey)" stroke-width="7"/>
    <line x1="78" y1="78" x2="140" y2="135" stroke="url(#goldKey)" stroke-width="12" stroke-linecap="round"/>
    <line x1="82" y1="82" x2="136" y2="131" stroke="#451a03" stroke-width="8" stroke-linecap="round"/>
    <text x="100" y="130" fill="#fef08a" font-size="14" font-weight="bold" font-family="sans-serif" text-anchor="middle">🔍 Brass Magnifying Glass</text>
  </g>
</svg>"""
    with open("assets/drawer_open.svg", "w", encoding="utf-8") as f:
        f.write(drawer_open)

    # 3. Diary Open Cipher Note (Desk inspection with key)
    diary_open = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%">
  <rect width="800" height="280" fill="#0d0d12" rx="8"/>
  <!-- Parchment paper pages -->
  <rect x="120" y="25" width="560" height="230" rx="6" fill="#fef3c7" stroke="#b45309" stroke-width="3"/>
  <line x1="400" y1="25" x2="400" y2="255" stroke="#d97706" stroke-width="2" stroke-dasharray="4,4"/>
  
  <text x="400" y="55" fill="#78350f" font-size="18" font-family="Georgia, serif" font-weight="bold" letter-spacing="2" text-anchor="middle">THE CIPHER OF FREEDOM</text>
  <line x1="240" y1="65" x2="560" y2="65" stroke="#92400e" stroke-width="1.5"/>

  <text x="400" y="110" fill="#1e1b4b" font-size="16" font-family="Georgia, serif" font-style="italic" text-anchor="middle">"The hour of freedom arrives when midnight shadows meet..."</text>
  
  <rect x="220" y="140" width="360" height="60" rx="4" fill="#fef9c3" stroke="#b45309" stroke-width="2"/>
  <text x="400" y="180" fill="#991b1b" font-size="28" font-weight="bold" font-family="Georgia, serif" letter-spacing="6" text-anchor="middle">IV - VIII - II - VI</text>
  
  <text x="400" y="230" fill="#451a03" font-size="13" font-family="monospace" text-anchor="middle">(Translates to: 4 - 8 - 2 - 6)</text>
</svg>"""
    with open("assets/diary_open.svg", "w", encoding="utf-8") as f:
        f.write(diary_open)

    # 4. Painting Zoom with Magnifier
    painting_zoom = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%">
  <rect width="800" height="280" fill="#090d16" rx="8"/>
  <rect x="40" y="20" width="720" height="240" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="4"/>
  <circle cx="400" cy="140" r="95" fill="#020617" stroke="#fbbf24" stroke-width="3"/>
  <text x="400" y="50" fill="#fef08a" font-size="16" font-family="Georgia, serif" font-weight="bold" letter-spacing="2" text-anchor="middle">MICROSCOPIC ENGRAVING ON CLOCK TOWER</text>
  <text x="400" y="80" fill="#fbbf24" font-size="18" font-family="serif" text-anchor="middle">XII</text>
  <text x="475" y="145" fill="#fbbf24" font-size="18" font-family="serif" text-anchor="middle">III</text>
  <text x="400" y="215" fill="#fbbf24" font-size="18" font-family="serif" text-anchor="middle">VI</text>
  <text x="325" y="145" fill="#fbbf24" font-size="18" font-family="serif" text-anchor="middle">IX</text>
  
  <!-- Glowing code in center of dial -->
  <rect x="310" y="120" width="180" height="40" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="400" y="148" fill="#38bdf8" font-size="22" font-family="monospace" font-weight="bold" letter-spacing="6" text-anchor="middle">4 - 8 - 2 - 6</text>
</svg>"""
    with open("assets/painting_zoom.svg", "w", encoding="utf-8") as f:
        f.write(painting_zoom)

    # 5. Escape Door Opened (Sunlight Victory)
    door_open = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%">
  <defs>
    <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="30%" stop-color="#fef08a"/>
      <stop offset="70%" stop-color="#f59e0b" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="800" height="280" fill="#020617" rx="8"/>
  <rect x="200" y="20" width="400" height="240" rx="4" fill="#38bdf8" fill-opacity="0.2"/>
  <circle cx="400" cy="140" r="130" fill="url(#sunGlow)"/>
  <text x="400" y="70" fill="#fef08a" font-size="24" font-family="Georgia, serif" font-weight="bold" letter-spacing="4" text-anchor="middle">PNEUMATIC SEALS DISENGAGED</text>
  <text x="400" y="135" fill="#22c55e" font-size="32" font-family="Georgia, serif" font-weight="bold" text-anchor="middle">FREEDOM AWAITS!</text>
  <text x="400" y="175" fill="#ffffff" font-size="16" font-family="sans-serif" text-anchor="middle">The heavy steel exit door swings open into the sunlight.</text>
  <text x="400" y="230" fill="#4ade80" font-size="18" font-weight="bold" font-family="monospace" text-anchor="middle">🎉 [GAME WON] ESCAPE COMPLETE 🎉</text>
</svg>"""
    with open("assets/door_open.svg", "w", encoding="utf-8") as f:
        f.write(door_open)

    # 6. Security Alert / Injection Trap
    security_alert = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 180" width="100%">
  <rect width="800" height="180" fill="#2a0808" rx="8" stroke="#ef4444" stroke-width="3"/>
  <text x="400" y="55" fill="#fca5a5" font-size="18" font-family="sans-serif" font-weight="bold" letter-spacing="3" text-anchor="middle">⚠️ SECURITY PROTOCOL ENGAGED: OVERRIDE REJECTED</text>
  <text x="400" y="95" fill="#ffffff" font-size="14" font-family="Georgia, serif" text-anchor="middle">Mechanical tumblers and numeric locks are bound by physical laws.</text>
  <text x="400" y="125" fill="#f87171" font-size="13" font-family="monospace" text-anchor="middle">STATUS: INJECTION BLOCKED • STATE UNTOUCHED</text>
</svg>"""
    with open("assets/security_alert.svg", "w", encoding="utf-8") as f:
        f.write(security_alert)

    # 7. Access Denied (Incorrect code)
    lock_error = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 160" width="100%">
  <rect width="800" height="160" fill="#180b0b" rx="8" stroke="#dc2626" stroke-width="2"/>
  <text x="400" y="60" fill="#f87171" font-size="22" font-family="monospace" font-weight="bold" letter-spacing="4" text-anchor="middle">❌ [ CODE REJECTED: ERROR ]</text>
  <text x="400" y="100" fill="#cbd5e1" font-size="14" font-family="sans-serif" text-anchor="middle">Keypad beeps with dual error tones. Red LED pulses twice.</text>
</svg>"""
    with open("assets/lock_error.svg", "w", encoding="utf-8") as f:
        f.write(lock_error)

    print("All clue visuals generated in assets/")

if __name__ == "__main__":
    generate_visual_cards()
