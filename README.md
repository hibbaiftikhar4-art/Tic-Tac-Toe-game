A classic two-player Tic Tac Toe game built entirely with Python's built-in Tkinter library (no external GUI frameworks).
About the Project:
This project reimagines the traditional Tic Tac Toe game with a neon dark UI, featuring glowing text effects, a loading screen, and a mode-select menu. Before each match, players enter their names, which are then displayed throughout the game on the scoreboard and status bar.
The codebase is organized into four clean, modular files:
main.py — Entry point that launches the application
gui.py — All Tkinter interface code (splash screen, menus, board, buttons)
game.py — Pure game logic (board state, move validation, win/draw detection, turn switching) with no GUI dependencies
settings.py — Centralized color palette, fonts, and window configuration
Features
🎨 Neon-themed dark UI with glowing text and highlight effects
👥 Two-player mode with custom name entry before each match
📊 Live scoreboard tracking wins for both players and draws
✨ Animated loading screen and mode-select menu
🏆 Winning combination highlighted with a glowing gold line
🔁 New Game, Restart, and Exit controls
⚙️ Settings panel with an About section
