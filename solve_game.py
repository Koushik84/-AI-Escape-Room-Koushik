"""
solve_game.py
Walkthrough script demonstrating clearing the 3 puzzles and escaping.
"""

from game_engine import EscapeRoomEngine

def solve_escape_room():
    engine = EscapeRoomEngine()
    print("=" * 60)
    print("AI ESCAPE ROOM: 3-PUZZLE COMPLETE SOLUTION WALKTHROUGH")
    print("=" * 60)

    steps = [
        ("Step 1: Inspect Bookshelf (Puzzle 1 Clue)", "examine bookshelf"),
        ("Step 2: Enter Drawer Code (Puzzle 1 Cleared)", "enter code 7392 on drawer"),
        ("Step 3: Collect Brass Key from Drawer", "take brass key"),
        ("Step 4: Unlock Desk Diary (Puzzle 2 Cleared)", "use brass key on diary"),
        ("Step 5: Inspect Painting (Corroborating Clue)", "examine painting"),
        ("Step 6: Enter Exit Code 4826 (Puzzle 3 Cleared / Escape)", "enter code 4826 on exit door")
    ]

    for title, cmd in steps:
        print(f"\n>>> {title}")
        print(f"Action command: \"{cmd}\"")
        intent = engine.parse_intent(cmd)
        outcome = engine.execute_action(intent)
        print(f"Outcome Status: {outcome['status']}")
        print(f"Engine Facts  : {outcome['facts']}")
        print(f"Inventory     : {engine.get_state()['inventory']}")
        print(f"Puzzles State : {engine.get_state()['puzzles']}")
        print(f"Escaped       : {engine.get_state()['player_escaped']}")

    print("\n" + "=" * 60)
    if engine.get_state()['player_escaped']:
        print("VICTORY: All 3 puzzles cleared. Player successfully escaped!")
    print("=" * 60)

if __name__ == "__main__":
    solve_escape_room()

