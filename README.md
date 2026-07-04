Tic Tac Toe:
A classic two-player Tic Tac Toe game reimagined with a glowing neon aesthetic, built entirely in Python using the Tkinter standard library with zero external dependencies.


About the Project:
This project reimagines the traditional Tic Tac Toe game with a neon dark UI, featuring glowing text effects, a loading screen, and a mode-select menu . Before each match, players enter their names, which are then displayed throughout the game on the scoreboard and status bar. Project Architecture
The code is split into four focused modules, keeping game logic completely independent of the interface.


FileResponsibility:
main.py->Entry point that creates the window and launches the app.
gui.py->All Tkinter which include splash screen, menus, board, buttons, settings.
game.py->Pure game logic includes board state, move validation, win/draw detection, turn switching (no GUI code).
settings.py->Centralized colors, fonts, and window configuration.


 Features:
🌌 Neon-themed dark UI —> glowing text effects and a synthwave color palette, built without any image or design libraries
🎬 Animated splash screen —>glowing title with a loading progress bar
🕹️ Mode-select menu with a decorative preview board
👥 Two-player mode with custom name entry before each match
📊 Live scoreboard tracking wins for both players and draws
🏆 Winning line highlight — glowing gold line marks the winning combination
🔁 Game controls — New Game, Restart, and Exit
⚙️ Settings & About panel


 Future Improvements:
1. Computer (AI) opponent mode
2. Sound effects
3. Adjustable board size (4x4, 5x5)

