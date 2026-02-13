import tkinter as tk
from tkinter import messagebox
import random
import webbrowser
import winsound  

class RainbowTicTacToePro:
    def __init__(self, root):
        self.root = root
        self.root.title("☠︎Tic-Tac-Toe☠︎︎")
        self.root.geometry("450x750")
        self.root.resizable(False, False)
        
        self.LOSER_URL = "https://youtu.be/7QHVszlncmM"
        
        self.player_score = 0
        self.cpu_score = 0
        self.draws = 0
        self.board = ["_" for _ in range(9)]
        self.buttons = []
        self.game_end = False
        self.is_pvp = False  
        self.current_player = "X"
        self.is_thinking = False
        
        self.player1_name = "Player X"
        self.player2_name = "CPU"

        self.WINS = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        
        self.roasts = {
            "horizontal": [
                "A horizontal win? Even a toddler sees those coming. You're blind.",
                "You just let them line up like ducks in a row. Absolutely pathetic.",
                "Is your 'Block' button broken, or is it just your brain?"
            ],
            "vertical": [
                "Watching you miss a vertical win is like watching a train wreck in slow motion.",
                "You got stacked. Uninstall the game and try Solitaire.",
                "How do you let someone win top-to-bottom? Do you even have eyes?"
            ],
            "diagonal": [
                "The diagonal snipe. You're so predictable it's actually painful.",
                "You just got 360-no-scoped in Tic-Tac-Toe. Absolute clown behavior.",
                "Diagonal wins are for people who actually think. Clearly, that's not you."
            ],
            "cpu_wins": [
                "I am literally a collection of 'if' statements and I still owned you. 🤡",
                "Your gameplay is so bad it should be a criminal offense.",
                "I'd call you a 'Loser,' but even losers win occasionally. You're just a failure.",
                "If embarrassment was a person, it would look exactly like your last move.",
                "Stop playing. Go outside. Maybe the grass can teach you logic."
            ],
            "draw": [
                "A draw? You both failed at the simplest game in human history.",
                "Two idiots, zero winners. Congrats on wasting everyone's time."
            ]
        }
        
        self.colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF", "#FF1493", "#00FFFF"]
        self.show_menu()

    def shake_window(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        for i in range(10):
            self.root.geometry(f"+{x+random.randint(-10,10)}+{y+random.randint(-10,10)}")
            self.root.update()
            self.root.after(20)
        self.root.geometry(f"+{x}+{y}")

    def get_roast(self, pattern_idx, winner_name, is_cpu_win):
        if is_cpu_win:
            return random.choice(self.roasts["cpu_wins"])
        if pattern_idx in [0, 1, 2]: style = "horizontal"
        elif pattern_idx in [3, 4, 5]: style = "vertical"
        else: style = "diagonal"
        return f"{winner_name} wins! {random.choice(self.roasts[style])}"

    def clear_screen(self):
        for widget in self.root.winfo_children(): widget.destroy()

    def show_menu(self):
        self.clear_screen()
        self.canvas = tk.Canvas(self.root, width=450, height=720, highlightthickness=0); self.canvas.pack()
        self.draw_rainbow_bg()
        self.canvas.create_text(225, 150, text="𝕿RAINBOW𝕿\nTIC-TAC-TOE\n𝕿BRUTALITY𝕿\n☠", font=('Arial Rounded MT Bold', 40, 'bold'), fill="white", justify="center")
        f = tk.Frame(self.root, bg="#000000", bd=5, relief="ridge"); self.canvas.create_window(225, 400, window=f)
        tk.Button(f, text="PvE (Hard)", font=('Segoe UI', 14, 'bold'), width=18, bg="#333", fg="white", command=self.start_pve).pack(pady=10)
        tk.Button(f, text="PvP (Local)", font=('Segoe UI', 14, 'bold'), width=18, bg="#333", fg="white", command=self.setup_pvp_names).pack(pady=10)
        tk.Button(f, text="Quit", font=('Segoe UI', 14, 'bold'), width=18, bg="#500", fg="white", command=self.root.quit).pack(pady=10)

    def draw_rainbow_bg(self):
        rainbow = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
        for i in range(720):
            seg = i / (720 / (len(rainbow)-1)); idx = int(seg); f = seg - idx
            c1, c2 = self.root.winfo_rgb(rainbow[idx]), self.root.winfo_rgb(rainbow[min(idx+1, 6)])
            r, g, b = [int((c1[j] + (c2[j]-c1[j])*f)/256) for j in range(3)]
            self.canvas.create_line(0, i, 450, i, fill=f'#{r:02x}{g:02x}{b:02x}')

    def setup_pvp_names(self):
        self.clear_screen()
        self.canvas = tk.Canvas(self.root, width=450, height=720); self.canvas.pack(); self.draw_rainbow_bg()
        ef = tk.Frame(self.root, bg="#1a1a1a", bd=5, relief="ridge", padx=20, pady=20); self.canvas.create_window(225, 360, window=ef)
        self.p1_e = tk.Entry(ef, font=('Segoe UI', 12)); self.p1_e.pack(pady=5); self.p1_e.insert(0, "Player 1")
        self.p2_e = tk.Entry(ef, font=('Segoe UI', 12)); self.p2_e.pack(pady=5); self.p2_e.insert(0, "Player 2")
        tk.Button(ef, text="FIGHT", font=('Segoe UI', 12, 'bold'), bg="#060", fg="white", command=self.val_pvp).pack(pady=10)

    def val_pvp(self):
        self.player1_name, self.player2_name, self.is_pvp = self.p1_e.get()[:15] or "P1", self.p2_e.get()[:15] or "P2", True; self.start_game()

    def start_pve(self):
        self.player1_name, self.player2_name, self.is_pvp = "Noob", "CPU", False; self.start_game()

    def reset_match(self):
        self.player_score = 0
        self.cpu_score = 0
        self.draws = 0
        self.reset_game_board()

    def start_game(self):
        self.clear_screen()
        self.canvas = tk.Canvas(self.root, width=450, height=720); self.canvas.pack(); self.draw_rainbow_bg()
        self.buttons, self.board, self.game_end, self.current_player = [], ["_" for _ in range(9)], False, "X"
        self.sf = tk.Frame(self.root, bg="#1a1a1a", bd=2, relief="ridge"); self.canvas.create_window(225, 60, window=self.sf, width=400)
        self.sl = tk.Label(self.sf, text=f"{self.player1_name}: {self.player_score} | {self.player2_name}: {self.cpu_score}", font=('Segoe UI', 11, 'bold'), bg="#1a1a1a", fg="white"); self.sl.pack(pady=5)
        self.gf = tk.Frame(self.root, bg="#111111", relief="sunken", borderwidth=12); self.canvas.create_window(225, 340, window=self.gf)
        for i in range(9):
            btn = tk.Button(self.gf, text="", font=('Arial Rounded MT Bold', 22, 'bold'), width=5, height=2, bg=self.colors[i], fg="white", command=lambda i=i: self.handle_click(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5); self.buttons.append(btn)
        
        tk.Button(self.root, text="MENU", font=('Segoe UI', 10, 'bold'), command=self.show_menu, bg="#333", fg="white", width=10).place(x=20, y=655)
        tk.Button(self.root, text="RESET MATCH", font=('Segoe UI', 10, 'bold'), command=self.reset_match, bg="#822", fg="white", width=12).place(x=325, y=655)
        
        self.status_var = tk.StringVar(value=f"{self.player1_name}'s Turn")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", bg="#000", fg="#aaa").pack(side="bottom", fill="x")

    def handle_click(self, index):
        if self.board[index] == "_" and not self.game_end and not self.is_thinking:
            self.make_move(index, self.current_player)
            if not self.game_end:
                if self.is_pvp:
                    self.current_player = "O" if self.current_player == "X" else "X"
                    n = self.player1_name if self.current_player == "X" else self.player2_name
                    self.status_var.set(f"{n}'s Turn")
                else:
                    self.is_thinking = True; self.status_var.set("CPU is mocking you..."); self.root.after(600, self.comp_move)

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player, state="disabled", bg="#222", disabledforeground=self.colors[index])
        winsound.Beep(800 if player == "X" else 500, 80)
        res = self.check_winner_full(self.board)
        if res: self.game_end = True; self.root.after(300, lambda: self.process_winner(res[0], res[1]))

    def comp_move(self):
        move = self.get_best_move("O"); self.is_thinking = False
        if move is not None: self.make_move(move, "O"); self.status_var.set(f"{self.player1_name}'s Turn")

    def get_best_move(self, p):
        best = -1000 if p == "O" else 1000; move = None
        for i in range(9):
            if self.board[i] == "_":
                self.board[i] = p; score = self.minimax(self.board, 0, p == "X"); self.board[i] = "_"
                if (p == "O" and score > best) or (p == "X" and score < best): best, move = score, i
        return move

    def minimax(self, b, d, is_max):
        res = self.check_winner_full(b)
        if res:
            if res[0] == "O": return 1
            if res[0] == "X": return -1
            if res[0] == "Draw": return 0
        scores = []
        for i in range(9):
            if b[i] == "_":
                b[i] = "O" if is_max else "X"; scores.append(self.minimax(b, d+1, not is_max)); b[i] = "_"
        return max(scores) if is_max else min(scores)

    def check_winner_full(self, b):
        for idx, c in enumerate(self.WINS):
            if b[c[0]] == b[c[1]] == b[c[2]] != "_": return (b[c[0]], idx)
        return ("Draw", -1) if "_" not in b else None

    def process_winner(self, winner, pattern_idx):
        if winner == "O" or winner == "Draw": self.shake_window()
        if winner == "X":
            self.player_score += 1
            msg = self.get_roast(pattern_idx, self.player1_name, False)
            messagebox.showinfo("Result", msg)
        elif winner == "O":
            self.cpu_score += 1
            is_cpu = not self.is_pvp
            msg = self.get_roast(pattern_idx, self.player2_name, is_cpu)
            if is_cpu:
                messagebox.showwarning("BRUTAL L", msg)
                webbrowser.open(self.LOSER_URL)
            else:
                messagebox.showinfo("Result", msg)
        else:
            self.draws += 1
            messagebox.showinfo("Draw", random.choice(self.roasts["draw"]))
        self.reset_game_board()

    def reset_game_board(self):
        if hasattr(self, 'sl'):
            self.sl.config(text=f"{self.player1_name}: {self.player_score} | {self.player2_name}: {self.cpu_score}")
        self.board, self.game_end, self.current_player = ["_" for _ in range(9)], False, "X"
        for i, btn in enumerate(self.buttons): btn.config(text="", state="normal", bg=self.colors[i])
        if hasattr(self, 'status_var'):
            self.status_var.set(f"{self.player1_name}'s Turn")

if __name__ == "__main__":
    root = tk.Tk(); app = RainbowTicTacToePro(root); root.mainloop()
