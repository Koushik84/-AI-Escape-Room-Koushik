"""
generate_svg_scenes.py
Generates rich, atmospheric SVG illustrations for the Victorian Library escape room.
"""

import os

def create_svgs():
    os.makedirs("assets", exist_ok=True)

    # 1. Main Library Banner (Moody Dark Academia)
    banner_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0a14"/>
      <stop offset="50%" stop-color="#141428"/>
      <stop offset="100%" stop-color="#06060c"/>
    </linearGradient>
    <radialGradient id="candleGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffb74d" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#ff9800" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ff9800" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#d4af37"/>
      <stop offset="50%" stop-color="#fff3b0"/>
      <stop offset="100%" stop-color="#aa771c"/>
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="360" fill="url(#bgGrad)"/>

  <!-- Wallpaper damask stripes -->
  <g opacity="0.07">
    <pattern id="stripes" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 0 0 L 20 20 L 0 40 Z" fill="#ffffff"/>
    </pattern>
    <rect width="1200" height="360" fill="url(#stripes)"/>
  </g>

  <!-- Floor boards -->
  <polygon points="0,290 1200,290 1200,360 0,360" fill="#1b120c"/>
  <line x1="0" y1="290" x2="1200" y2="290" stroke="#3d271d" stroke-width="3"/>
  <line x1="300" y1="290" x2="200" y2="360" stroke="#2a1a13" stroke-width="2"/>
  <line x1="600" y1="290" x2="550" y2="360" stroke="#2a1a13" stroke-width="2"/>
  <line x1="900" y1="290" x2="920" y2="360" stroke="#2a1a13" stroke-width="2"/>

  <!-- Left: Bookshelf Silhouette -->
  <rect x="60" y="50" width="180" height="240" rx="4" fill="#1e1610" stroke="#3e2d21" stroke-width="3" filter="url(#shadow)"/>
  <rect x="75" y="70" width="150" height="6" fill="#4a3728"/>
  <rect x="75" y="130" width="150" height="6" fill="#4a3728"/>
  <rect x="75" y="190" width="150" height="6" fill="#4a3728"/>
  <rect x="75" y="250" width="150" height="6" fill="#4a3728"/>

  <!-- Colored Clue Books on shelf -->
  <rect x="85" y="142" width="22" height="48" rx="2" fill="#dc2626"/>
  <text x="96" y="172" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle" font-family="serif">7</text>
  <rect x="110" y="146" width="22" height="44" rx="2" fill="#2563eb"/>
  <text x="121" y="172" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle" font-family="serif">3</text>
  <rect x="135" y="140" width="22" height="50" rx="2" fill="#16a34a"/>
  <text x="146" y="172" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle" font-family="serif">9</text>
  <rect x="160" y="144" width="22" height="46" rx="2" fill="#18181b" stroke="#71717a" stroke-width="1"/>
  <text x="171" y="172" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle" font-family="serif">2</text>

  <!-- Center-Left: Clock Tower Painting -->
  <rect x="340" y="40" width="190" height="150" rx="6" fill="#1c1917" stroke="url(#goldGrad)" stroke-width="6" filter="url(#shadow)"/>
  <circle cx="435" cy="115" r="46" fill="#0c0a09" stroke="#d4af37" stroke-width="2"/>
  <line x1="435" y1="115" x2="435" y2="85" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>
  <line x1="435" y1="115" x2="465" y2="125" stroke="#f59e0b" stroke-width="2" stroke-linecap="round"/>
  <circle cx="435" cy="115" r="4" fill="#fbbf24"/>
  <text x="435" y="80" fill="#d4af37" font-size="10" text-anchor="middle" font-family="serif">XII</text>
  <text x="475" y="119" fill="#d4af37" font-size="10" text-anchor="middle" font-family="serif">III</text>
  <text x="435" y="153" fill="#d4af37" font-size="10" text-anchor="middle" font-family="serif">VI</text>
  <text x="395" y="119" fill="#d4af37" font-size="10" text-anchor="middle" font-family="serif">IX</text>

  <!-- Desk & Lamp in Center -->
  <rect x="320" y="210" width="240" height="80" rx="4" fill="#2d1d14" stroke="#4a3325" stroke-width="3" filter="url(#shadow)"/>
  <rect x="340" y="235" width="90" height="40" rx="3" fill="#1b120c" stroke="#3b271b" stroke-width="2"/>
  <!-- Leather Diary on Desk -->
  <rect x="450" y="225" width="60" height="45" rx="3" fill="#581c87" stroke="#9333ea" stroke-width="1.5"/>
  <circle cx="480" cy="247" r="4" fill="#eab308"/>

  <!-- Candle / Lamp Glow -->
  <circle cx="370" cy="195" r="60" fill="url(#candleGlow)"/>
  <path d="M 368 200 Q 370 190 372 200 Z" fill="#ffedd5"/>

  <!-- Center-Right: Ornate Locked Drawer -->
  <rect x="660" y="180" width="160" height="110" rx="4" fill="#241a14" stroke="#4a3728" stroke-width="3" filter="url(#shadow)"/>
  <rect x="680" y="200" width="120" height="35" rx="2" fill="#17110c" stroke="#35261b" stroke-width="2"/>
  <!-- Keypad on drawer -->
  <rect x="720" y="206" width="40" height="22" rx="2" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
  <circle cx="728" cy="217" r="2" fill="#38bdf8"/>
  <circle cx="736" cy="217" r="2" fill="#38bdf8"/>
  <circle cx="744" cy="217" r="2" fill="#38bdf8"/>
  <circle cx="752" cy="217" r="2" fill="#38bdf8"/>

  <!-- Right: Steel Reinforced Exit Door -->
  <rect x="940" y="40" width="180" height="250" rx="4" fill="#1e293b" stroke="#475569" stroke-width="5" filter="url(#shadow)"/>
  <rect x="960" y="60" width="140" height="100" rx="2" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <rect x="960" y="175" width="140" height="95" rx="2" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <!-- Digital Keypad lock on door -->
  <rect x="915" y="140" width="35" height="55" rx="3" fill="#020617" stroke="#ef4444" stroke-width="2"/>
  <rect x="920" y="146" width="25" height="14" fill="#1e293b"/>
  <circle cx="925" cy="168" r="2" fill="#94a3b8"/>
  <circle cx="932" cy="168" r="2" fill="#94a3b8"/>
  <circle cx="939" cy="168" r="2" fill="#94a3b8"/>
  <circle cx="925" cy="176" r="2" fill="#94a3b8"/>
  <circle cx="932" cy="176" r="2" fill="#94a3b8"/>
  <circle cx="939" cy="176" r="2" fill="#94a3b8"/>
  <circle cx="932" cy="184" r="2" fill="#ef4444"/>

  <!-- Atmosphere Vignette Overlay -->
  <rect width="1200" height="360" fill="none" stroke="#000" stroke-width="20" opacity="0.3"/>

  <!-- Atmospheric Title text overlay -->
  <text x="600" y="45" fill="url(#goldGrad)" font-size="24" font-weight="bold" letter-spacing="4" text-anchor="middle" font-family="Georgia, serif" filter="url(#shadow)">THE VICTORIAN LIBRARY ESCAPE</text>
  <text x="600" y="70" fill="#94a3b8" font-size="12" letter-spacing="2" text-anchor="middle" font-family="sans-serif">5 OBJECTS • 3 PUZZLES • 1 ESCAPE</text>
</svg>"""

    with open("assets/library_banner.svg", "w", encoding="utf-8") as f:
        f.write(banner_svg)

    # 2. Bookshelf Card Graphic
    bookshelf_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240" width="100%">
  <rect width="400" height="240" fill="#18120c" rx="8"/>
  <rect x="20" y="20" width="360" height="200" rx="4" fill="#241a12" stroke="#4a3728" stroke-width="4"/>
  <line x1="30" y1="120" x2="370" y2="120" stroke="#5a4332" stroke-width="8"/>
  <line x1="30" y1="190" x2="370" y2="190" stroke="#5a4332" stroke-width="8"/>
  <!-- Top Shelf Decorative books -->
  <rect x="40" y="45" width="25" height="70" fill="#3f3f46" rx="2"/>
  <rect x="68" y="50" width="20" height="65" fill="#52525b" rx="2"/>
  <rect x="91" y="40" width="30" height="75" fill="#3f3f46" rx="2"/>
  <!-- Middle Shelf: The 4 Clue Books -->
  <g>
    <rect x="70" y="126" width="45" height="60" rx="3" fill="#dc2626" stroke="#b91c1c" stroke-width="2"/>
    <text x="92" y="162" fill="#ffffff" font-size="22" font-weight="bold" font-family="Georgia, serif" text-anchor="middle">7</text>
    <text x="92" y="180" fill="#fca5a5" font-size="9" text-anchor="middle">Astronomy</text>

    <rect x="130" y="130" width="45" height="56" rx="3" fill="#2563eb" stroke="#1d4ed8" stroke-width="2"/>
    <text x="152" y="162" fill="#ffffff" font-size="22" font-weight="bold" font-family="Georgia, serif" text-anchor="middle">3</text>
    <text x="152" y="180" fill="#93c5fd" font-size="9" text-anchor="middle">Botany</text>

    <rect x="190" y="124" width="45" height="62" rx="3" fill="#16a34a" stroke="#15803d" stroke-width="2"/>
    <text x="212" y="162" fill="#ffffff" font-size="22" font-weight="bold" font-family="Georgia, serif" text-anchor="middle">9</text>
    <text x="212" y="180" fill="#86efac" font-size="9" text-anchor="middle">Cryptology</text>

    <rect x="250" y="128" width="45" height="58" rx="3" fill="#18181b" stroke="#52525b" stroke-width="2"/>
    <text x="272" y="162" fill="#ffffff" font-size="22" font-weight="bold" font-family="Georgia, serif" text-anchor="middle">2</text>
    <text x="272" y="180" fill="#cbd5e1" font-size="9" text-anchor="middle">Dynamite</text>
  </g>
</svg>"""
    with open("assets/bookshelf.svg", "w", encoding="utf-8") as f:
        f.write(bookshelf_svg)

    # 3. Drawer Card Graphic
    drawer_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240" width="100%">
  <rect width="400" height="240" fill="#1c1917" rx="8"/>
  <rect x="40" y="40" width="320" height="160" rx="6" fill="#292524" stroke="#78716c" stroke-width="3"/>
  <rect x="60" y="65" width="280" height="110" rx="4" fill="#1c1917" stroke="#44403c" stroke-width="2"/>
  <!-- Keypad on Drawer -->
  <rect x="150" y="80" width="100" height="80" rx="4" fill="#090d16" stroke="#38bdf8" stroke-width="2"/>
  <rect x="160" y="90" width="80" height="24" rx="2" fill="#1e293b"/>
  <text x="200" y="107" fill="#38bdf8" font-size="14" font-family="monospace" font-weight="bold" text-anchor="middle">[ * * * * ]</text>
  <!-- Keypad buttons -->
  <circle cx="170" cy="125" r="5" fill="#475569"/><circle cx="185" cy="125" r="5" fill="#475569"/>
  <circle cx="200" cy="125" r="5" fill="#475569"/><circle cx="215" cy="125" r="5" fill="#475569"/>
  <circle cx="230" cy="125" r="5" fill="#475569"/><circle cx="170" cy="142" r="5" fill="#475569"/>
  <circle cx="185" cy="142" r="5" fill="#475569"/><circle cx="200" cy="142" r="5" fill="#475569"/>
  <circle cx="215" cy="142" r="5" fill="#475569"/><circle cx="230" cy="142" r="5" fill="#22c55e"/>
</svg>"""
    with open("assets/locked_drawer.svg", "w", encoding="utf-8") as f:
        f.write(drawer_svg)

    # 4. Painting Card Graphic
    painting_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240" width="100%">
  <rect width="400" height="240" fill="#111827" rx="8"/>
  <rect x="60" y="20" width="280" height="200" rx="6" fill="#1f2937" stroke="#d97706" stroke-width="8"/>
  <circle cx="200" cy="120" r="70" fill="#030712" stroke="#f59e0b" stroke-width="3"/>
  <!-- Clock numerals -->
  <text x="200" y="70" fill="#fbbf24" font-size="16" font-family="serif" text-anchor="middle">XII</text>
  <text x="255" y="125" fill="#fbbf24" font-size="16" font-family="serif" text-anchor="middle">III</text>
  <text x="200" y="175" fill="#fbbf24" font-size="16" font-family="serif" text-anchor="middle">VI</text>
  <text x="145" y="125" fill="#fbbf24" font-size="16" font-family="serif" text-anchor="middle">IX</text>
  <!-- Clock hands pointing towards 4 and 8 -->
  <line x1="200" y1="120" x2="238" y2="150" stroke="#f59e0b" stroke-width="4" stroke-linecap="round"/>
  <line x1="200" y1="120" x2="160" y2="150" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>
  <circle cx="200" cy="120" r="5" fill="#fef3c7"/>
</svg>"""
    with open("assets/clock_painting.svg", "w", encoding="utf-8") as f:
        f.write(painting_svg)

    # 5. Study Desk & Diary Graphic
    desk_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240" width="100%">
  <rect width="400" height="240" fill="#18120c" rx="8"/>
  <!-- Desk top -->
  <rect x="30" y="90" width="340" height="120" rx="6" fill="#2d1c12" stroke="#543725" stroke-width="4"/>
  <!-- Diary -->
  <rect x="130" y="110" width="140" height="80" rx="4" fill="#4c1d95" stroke="#7c3aed" stroke-width="2"/>
  <line x1="200" y1="110" x2="200" y2="190" stroke="#a78bfa" stroke-width="2"/>
  <circle cx="200" cy="150" r="8" fill="#eab308"/>
  <circle cx="200" cy="150" r="3" fill="#1e1b4b"/>
  <!-- Antique Lamp -->
  <path d="M 70 170 L 100 170 L 90 120 L 80 120 Z" fill="#d97706"/>
  <path d="M 65 120 Q 85 90 105 120 Z" fill="#047857" stroke="#065f46" stroke-width="2"/>
  <circle cx="85" cy="130" r="15" fill="#fef08a" opacity="0.6"/>
</svg>"""
    with open("assets/study_desk.svg", "w", encoding="utf-8") as f:
        f.write(desk_svg)

    # 6. Exit Door Graphic
    door_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240" width="100%">
  <rect width="400" height="240" fill="#0f172a" rx="8"/>
  <rect x="110" y="20" width="180" height="200" rx="4" fill="#1e293b" stroke="#475569" stroke-width="6"/>
  <rect x="130" y="40" width="140" height="75" rx="3" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <rect x="130" y="130" width="140" height="75" rx="3" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <!-- Electronic keypad -->
  <rect x="80" y="90" width="30" height="60" rx="3" fill="#020617" stroke="#ef4444" stroke-width="2"/>
  <circle cx="95" cy="105" r="4" fill="#ef4444"/>
  <line x1="86" y1="120" x2="104" y2="120" stroke="#94a3b8" stroke-width="2"/>
  <line x1="86" y1="130" x2="104" y2="130" stroke="#94a3b8" stroke-width="2"/>
  <line x1="86" y1="140" x2="104" y2="140" stroke="#94a3b8" stroke-width="2"/>
</svg>"""
    with open("assets/exit_door.svg", "w", encoding="utf-8") as f:
        f.write(door_svg)

    print("SVG visual scene assets generated in assets/")

if __name__ == "__main__":
    create_svgs()
