import tkinter as tk
from tkinter import messagebox

from game import TicTacToeGame
import settings as cfg
class TicTacToeApp:

    def __init__(self, root):
        self.root = root
        self.root.title(cfg.WINDOW_TITLE)
        self.root.geometry(f"{cfg.WINDOW_WIDTH}x{cfg.WINDOW_HEIGHT}")
        self.root.configure(bg=cfg.NEON_BG)
        self.root.resizable(False, False)

        self.W = cfg.WINDOW_WIDTH
        self.H = cfg.WINDOW_HEIGHT

        self.canvas = tk.Canvas(
            self.root, width=self.W, height=self.H,
            bg=cfg.NEON_BG, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.game = None
        self.cell_rects = []   
        self.cell_marks = []   
        self.board_active = False

        self._embedded_widgets = []

        self.show_splash_screen()

    def _clear(self):
        """Wipes the canvas and destroys any embedded widgets (Entry, etc.)."""
        self.canvas.delete("all")
        for w in self._embedded_widgets:
            w.destroy()
        self._embedded_widgets = []

    def _draw_floor_grid(self):
        """Decorative faint grid lines near the bottom, synthwave-style."""
        for x in range(0, self.W + 40, 40):
            self.canvas.create_line(x, self.H * 0.55, x - 60, self.H,
                                     fill=cfg.NEON_BG_GRID, width=1)
        for y in range(int(self.H * 0.55), self.H, 25):
            self.canvas.create_line(0, y, self.W, y, fill=cfg.NEON_BG_GRID, width=1)

    def _glow_text(self, x, y, text, font, bright, dim, size_boost=5):
        """Fakes a neon glow: draws a slightly larger dim-colored copy of the
        text behind a normal-sized bright copy on top."""
        family, size, weight = font
        big_font = (family, size + size_boost, weight)
        self.canvas.create_text(x, y, text=text, font=big_font, fill=dim)
        return self.canvas.create_text(x, y, text=text, font=font, fill=bright)

    def _round_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        """Draws a rounded rectangle using a smoothed polygon."""
        points = [
            x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def _neon_button(self, cx, cy, w, h, text, border_color, command,
                      font=None, text_color=None, fill=None):
        """Creates a rounded neon-bordered button on the canvas.
        Returns (rect_id, text_id)."""
        font = font or cfg.FONT_NEON_BTN
        text_color = text_color or cfg.NEON_WHITE
        fill = fill or cfg.NEON_PANEL
        x1, y1, x2, y2 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2

        rect = self._round_rect(x1, y1, x2, y2, radius=h / 2.2,
                                 outline=border_color, width=2, fill=fill)
        label = self.canvas.create_text(cx, cy, text=text, font=font, fill=text_color)

        def on_enter(e):
            self.canvas.itemconfig(rect, fill=border_color)
            self.canvas.itemconfig(label, fill=cfg.NEON_BG)

        def on_leave(e):
            self.canvas.itemconfig(rect, fill=fill)
            self.canvas.itemconfig(label, fill=text_color)

        def on_click(e):
            command()

        for item in (rect, label):
            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)
            self.canvas.tag_bind(item, "<Button-1>", on_click)

        return rect, label
    def show_splash_screen(self):
        self._clear()
        self._draw_floor_grid()

        cx = self.W / 2
        self._glow_text(cx, self.H * 0.30, "TIC TAC TOE", cfg.FONT_NEON_TITLE,
                         cfg.NEON_CYAN, cfg.NEON_CYAN_DIM)

        sub_y = self.H * 0.30 + 55
        self._glow_text(cx - 60, sub_y, "X", cfg.FONT_NEON_SUB, cfg.NEON_BLUE, cfg.NEON_BLUE_DIM)
        self._glow_text(cx, sub_y, "X", cfg.FONT_NEON_SUB, cfg.NEON_BLUE, cfg.NEON_BLUE_DIM)
        self._glow_text(cx + 60, sub_y, "O", cfg.FONT_NEON_SUB, cfg.NEON_RED, cfg.NEON_RED_DIM)

        bar_w, bar_h = self.W * 0.7, 26
        bar_x1 = cx - bar_w / 2
        bar_y1 = self.H * 0.85
        bar_x2 = bar_x1 + bar_w
        bar_y2 = bar_y1 + bar_h

        self._round_rect(bar_x1, bar_y1, bar_x2, bar_y2, radius=13,
                          outline=cfg.NEON_PURPLE, width=2, fill=cfg.NEON_PANEL)
        self.loading_fill = self._round_rect(bar_x1, bar_y1, bar_x1 + 4, bar_y2,
                                              radius=13, outline="", fill=cfg.NEON_PINK)
        self.loading_text = self.canvas.create_text(
            cx, (bar_y1 + bar_y2) / 2, text="0 %", font=cfg.FONT_NEON_LOAD, fill=cfg.NEON_WHITE
        )

        self._bar_x1, self._bar_x2 = bar_x1, bar_x2
        self._bar_y1, self._bar_y2 = bar_y1, bar_y2

        self._animate_loading(0)

    def _animate_loading(self, pct):
        """Recursively fills the loading bar, then moves to mode select."""
        pct = min(pct, 100)
        fraction = pct / 100
        new_x2 = self._bar_x1 + fraction * (self._bar_x2 - self._bar_x1)

        self.canvas.delete(self.loading_fill)
        if new_x2 > self._bar_x1 + 4:
            self.loading_fill = self._round_rect(
                self._bar_x1, self._bar_y1, new_x2, self._bar_y2,
                radius=13, outline="", fill=cfg.NEON_PINK
            )
        self.canvas.itemconfig(self.loading_text, text=f"{pct} %")
        self.canvas.tag_raise(self.loading_text)

        if pct < 100:
            self.root.after(25, lambda: self._animate_loading(pct + 4))
        else:
            self.root.after(300, self.show_mode_select_scre)

    def show_mode_select_screen(self):
        self._clear()
        self._draw_floor_grid()
        cx = self.W / 2

        self._glow_text(cx, 70, "TIC TAC TOE", cfg.FONT_NEON_SUB,
                         cfg.NEON_CYAN, cfg.NEON_CYAN_DIM, size_boost=3)
        self._glow_text(cx, 130, "3 x 3", cfg.FONT_NEON_LABEL,
                         cfg.NEON_YELLOW, cfg.NEON_YELLOW_DIM, size_boost=2)

        self._draw_mini_preview_board(cx, 350)

        self._neon_button(
            cx, 560, self.W * 0.75, 55, "\U0001F9CD  VS  \U0001F9CD  (2 Player)",
            cfg.NEON_PINK, self.show_name_entry_screen
        )

    def _draw_mini_preview_board(self, cx, cy):
        """Decorative, non-interactive mini board for visual flair."""
        size = 200
        x1, y1 = cx - size / 2, cy - size / 2
        x2, y2 = cx + size / 2, cy + size / 2
        self._round_rect(x1, y1, x2, y2, radius=16, outline=cfg.NEON_PINK,
                          width=2, fill=cfg.NEON_PANEL)
        step = size / 3
        for i in (1, 2):
            self.canvas.create_line(x1 + step * i, y1, x1 + step * i, y2,
                                     fill=cfg.NEON_PURPLE, width=1)
            self.canvas.create_line(x1, y1 + step * i, x2, y1 + step * i,
                                     fill=cfg.NEON_PURPLE, width=1)

        demo = ["O", "X", "X", "O", "O", "", "X", "X", "O"]
        for i, val in enumerate(demo):
            if not val:
                continue
            row, col = divmod(i, 3)
            px = x1 + step * col + step / 2
            py = y1 + step * row + step / 2
            color = cfg.NEON_BLUE if val == "X" else cfg.NEON_RED
            dim = cfg.NEON_BLUE_DIM if val == "X" else cfg.NEON_RED_DIM
            self._glow_text(px, py, val, ("Arial Black", 22, "bold"), color, dim, size_boost=3)

    def show_name_entry_screen(self):
        self._clear()
        self._draw_floor_grid()
        cx = self.W / 2

        self._glow_text(cx, 90, "ENTER NAMES", cfg.FONT_NEON_SUB,
                         cfg.NEON_CYAN, cfg.NEON_CYAN_DIM, size_boost=3)

        self.canvas.create_text(cx, 180, text="Player X Name", font=cfg.FONT_NEON_LABEL,
                                 fill=cfg.NEON_BLUE)
        x_entry = tk.Entry(self.canvas, font=cfg.FONT_ENTRY, justify="center",
                            bg=cfg.NEON_PANEL, fg=cfg.NEON_WHITE,
                            insertbackground=cfg.NEON_WHITE, relief="flat")
        self.canvas.create_window(cx, 215, window=x_entry, width=220, height=32)
        self._embedded_widgets.append(x_entry)

        self.canvas.create_text(cx, 280, text="Player O Name", font=cfg.FONT_NEON_LABEL,
                                 fill=cfg.NEON_RED)
        o_entry = tk.Entry(self.canvas, font=cfg.FONT_ENTRY, justify="center",
                            bg=cfg.NEON_PANEL, fg=cfg.NEON_WHITE,
                            insertbackground=cfg.NEON_WHITE, relief="flat")
        self.canvas.create_window(cx, 315, window=o_entry, width=220, height=32)
        self._embedded_widgets.append(o_entry)

        x_entry.focus_set()
        o_entry.bind("<Return>", lambda e: self._start_game(x_entry, o_entry))

        self._neon_button(cx, 400, 200, 50, "START GAME", cfg.NEON_YELLOW,
                           lambda: self._start_game(x_entry, o_entry))

        self._neon_button(cx, self.H - 60, 160, 44, "\u2190 Back", cfg.NEON_PURPLE,
                           self.show_mode_select_screen)

    def _start_game(self, x_entry, o_entry):
        x_name = x_entry.get().strip() or "Player 1"
        o_name = o_entry.get().strip() or "Player 2"
        self.game = TicTacToeGame(x_name, o_name)
        self.show_game_screen()
    def show_game_screen(self):
        self._clear()
        self.cell_rects = []
        self.cell_marks = []

        # Top bar: home + settings icons
        self._neon_button(45, 40, 60, 44, "\u2190", cfg.NEON_YELLOW, self.confirm_go_home,
                           font=cfg.FONT_NEON_ICON)
        self._neon_button(self.W - 45, 40, 60, 44, "\u2699", cfg.NEON_PINK, self.open_settings,
                           font=cfg.FONT_NEON_ICON)

        cx = self.W / 2
        self._round_rect(20, 75, self.W - 20, 130, radius=25,
                          outline=cfg.NEON_PURPLE, width=2, fill=cfg.NEON_PANEL)
        self.score_x_text = self._glow_text(
            self.W * 0.22, 102, f"X  {self.game.scores['X']}",
            ("Arial Black", 16, "bold"), cfg.NEON_BLUE, cfg.NEON_BLUE_DIM, size_boost=2
        )
        self.draw_text = self.canvas.create_text(
            cx, 102, text=f"Draws: {self.game.scores['Draws']}",
            font=cfg.FONT_NEON_LABEL, fill=cfg.NEON_TEXT_DIM
        )
        self.score_o_text = self._glow_text(
            self.W * 0.78, 102, f"O  {self.game.scores['O']}",
            ("Arial Black", 16, "bold"), cfg.NEON_RED, cfg.NEON_RED_DIM, size_boost=2
        )

        # Status label
        self.status_text = self.canvas.create_text(
            cx, 155, text=f"{self.game.get_current_player_name()}'s Turn",
            font=cfg.FONT_NEON_STATUS, fill=cfg.NEON_WHITE
        )

        # Board
        board_size = self.W * 0.78
        bx1 = cx - board_size / 2
        by1 = 190
        bx2 = bx1 + board_size
        by2 = by1 + board_size
        self._round_rect(bx1, by1, bx2, by2, radius=18, outline=cfg.NEON_PURPLE,
                          width=3, fill=cfg.NEON_BG)

        step = board_size / 3
        for i in (1, 2):
            self.canvas.create_line(bx1 + step * i, by1, bx1 + step * i, by2,
                                     fill=cfg.NEON_PURPLE, width=2)
            self.canvas.create_line(bx1, by1 + step * i, bx2, by1 + step * i,
                                     fill=cfg.NEON_PURPLE, width=2)

        self._board_origin = (bx1, by1)
        self._cell_step = step

        for i in range(9):
            row, col = divmod(i, 3)
            cx1 = bx1 + col * step
            cy1 = by1 + row * step
            cx2 = cx1 + step
            cy2 = cy1 + step
            rect = self.canvas.create_rectangle(cx1, cy1, cx2, cy2, outline="", fill="")
            self.cell_rects.append(rect)
            self.cell_marks.append(None)
            self.canvas.tag_bind(rect, "<Button-1>", lambda e, idx=i: self.on_cell_click(idx))

        self.board_active = True

        # Bottom buttons
        by = by2 + 55
        self._neon_button(cx - 130, by, 130, 46, "New Game", cfg.NEON_CYAN, self.new_game)
        self._neon_button(cx, by, 130, 46, "Restart", cfg.NEON_YELLOW, self.restart_game)
        self._neon_button(cx + 130, by, 130, 46, "Exit", cfg.NEON_RED, self.exit_app)

    # Cell click handling 

    def on_cell_click(self, index):
        if not self.board_active:
            return

        symbol = self.game.current_player
        moved = self.game.make_move(index)
        if not moved:
            return

        color = cfg.NEON_BLUE if symbol == "X" else cfg.NEON_RED
        dim = cfg.NEON_BLUE_DIM if symbol == "X" else cfg.NEON_RED_DIM

        bx1, by1 = self._board_origin
        step = self._cell_step
        row, col = divmod(index, 3)
        px = bx1 + col * step + step / 2
        py = by1 + row * step + step / 2

        mark_id = self._glow_text(px, py, symbol, cfg.FONT_NEON_CELL, color, dim, size_boost=4)
        self.cell_marks[index] = mark_id

        if self.game.game_over:
            self.board_active = False
            self.update_scoreboard()
            if self.game.winner in ("X", "O"):
                self.highlight_winner()
                winner_name = self.game.get_player_name(self.game.winner)
                self.canvas.itemconfig(self.status_text, text=f"{winner_name} Wins! \U0001F389")
            else:
                self.canvas.itemconfig(self.status_text, text="It's a Draw!")
        else:
            self.canvas.itemconfig(
                self.status_text, text=f"{self.game.get_current_player_name()}'s Turn"
            )

    def highlight_winner(self):
        if not self.game.winning_combination:
            return
        bx1, by1 = self._board_origin
        step = self._cell_step
        combo = self.game.winning_combination
        a, c = combo[0], combo[-1]
        row_a, col_a = divmod(a, 3)
        row_c, col_c = divmod(c, 3)
        x1 = bx1 + col_a * step + step / 2
        y1 = by1 + row_a * step + step / 2
        x2 = bx1 + col_c * step + step / 2
        y2 = by1 + row_c * step + step / 2
        line = self.canvas.create_line(x1, y1, x2, y2, fill=cfg.NEON_GOLD, width=6,
                                        capstyle="round")
        glow = self.canvas.create_line(x1, y1, x2, y2, fill=cfg.NEON_GOLD_DIM, width=12,
                                        capstyle="round")
        self.canvas.tag_lower(glow, line)

    def update_scoreboard(self):
        self.canvas.itemconfig(self.score_x_text, text=f"X  {self.game.scores['X']}")
        self.canvas.itemconfig(self.score_o_text, text=f"O  {self.game.scores['O']}")
        self.canvas.itemconfig(self.draw_text, text=f"Draws: {self.game.scores['Draws']}")



    def new_game(self):
        self.game.new_game()
        self.game.reset_scores()
        self.show_game_screen()

    def restart_game(self):
        self.game.reset_board()
        self.show_game_screen()

    def confirm_go_home(self):
        self.show_mode_select_screen()

    def exit_app(self):
        self.root.destroy()

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("280x220")
        win.configure(bg=cfg.NEON_BG)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="Settings", font=cfg.FONT_NEON_SUB, bg=cfg.NEON_BG,
                 fg=cfg.NEON_CYAN).pack(pady=(20, 15))

        tk.Button(win, text="About", font=cfg.FONT_NEON_BTN, bg=cfg.NEON_PANEL,
                  fg=cfg.NEON_WHITE, relief="flat", command=self.open_about
                  ).pack(pady=8, ipadx=10, ipady=4)

        tk.Button(win, text="Close", font=cfg.FONT_NEON_BTN, bg=cfg.NEON_PANEL,
                  fg=cfg.NEON_WHITE, relief="flat", command=win.destroy
                  ).pack(pady=8, ipadx=10, ipady=4)

    def open_about(self):
        win = tk.Toplevel(self.root)
        win.title("About")
        win.geometry("280x160")
        win.configure(bg=cfg.NEON_BG)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="Tic Tac Toe", font=cfg.FONT_NEON_SUB, bg=cfg.NEON_BG,
                 fg=cfg.NEON_CYAN).pack(pady=(20, 5))
        tk.Label(win, text="Developed by: Hibba Iftikhar", font=cfg.FONT_NEON_LABEL,
                 bg=cfg.NEON_BG, fg=cfg.NEON_WHITE).pack(pady=(5, 0))