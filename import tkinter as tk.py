import tkinter as tk
from tkinter import messagebox
import random
import webbrowser
import winsound  

class RainbowTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Rainbow Tic-Tac-Toe: Sound Edition")
        
        self.LOSER_URL = "https://youtu.be/7QHVszlncmM"
        
        self.player_score = 0
        self.cpu_score = 0
        self.draws = 0
        self.board = ["_" for _ in range(9)]
        self.buttons = []
        self.game_end = False
        
        self.colors = [
            "#FF0000", "#FF7F00", "#FFFF00", 
            "#00FF00", "#0000FF", "#4B0082", 
            "#8B00FF", "#FF1493", "#00FFFF"
        ]
        
        self.setup_ui()

    def play_click_sound(self, player):
        """Plays a beep sound based on who moved."""
        if player == "X":
          
            winsound.Beep(1000, 100)
        else:
            
            winsound.Beep(600, 150)

    def setup_ui(self):
        self.score_label = tk.Label(
            self.root, 
            text=f"Player: {self.player_score} | CPU: {self.cpu_score} | Draws: {self.draws}",
            font=('Arial', 12, 'bold')
        )
        self.score_label.pack(pady=10)

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        for i in range(9):
            btn = tk.Button(
                self.grid_frame, 
                text="", 
                font=('Arial', 24, 'bold'), 
                width=5, height=2,
                bg=self.colors[i],
                command=lambda i=i: self.human_move(i)
            )
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

        self.withdraw_btn = tk.Button(
            self.root, text="Withdraw (Accept Defeat)", 
            command=self.withdraw, bg="#333", fg="white"
        )
        self.withdraw_btn.pack(pady=10)

    def human_move(self, index):
        if self.board[index] == "_" and not self.game_end:
            self.make_move(index, "X")
            if not self.game_end:
                self.root.after(500, self.computer_move)

    def computer_move(self):
        if self.game_end: return
        empty = [i for i, val in enumerate(self.board) if val == "_"]
        if empty:
            self.make_move(random.choice(empty), "O")

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player, state="disabled", disabledforeground="black")
        
      
        self.play_click_sound(player)
        
        winner = self.check_winner()
        if winner:
            self.game_end = True
          
            self.root.after(200, lambda: self.process_winner(winner))

    def withdraw(self):
        if not self.game_end:
          
            winsound.Beep(300, 500)
            self.process_winner("O")

    def process_winner(self, winner):
        if winner == "X":
            self.player_score += 1
         
            winsound.Beep(1200, 100); winsound.Beep(1500, 100); winsound.Beep(1800, 200)
            messagebox.showinfo("Result", "You survived... for now.")
        elif winner == "O":
            self.cpu_score += 1
            messagebox.showwarning("L", "You lost. Sending you to the shadow realm.")
            webbrowser.open(self.LOSER_URL)
        else:
            self.draws += 1
            messagebox.showinfo("Result", "A draw. Safe... barely.")

        self.score_label.config(text=f"Player: {self.player_score} | CPU: {self.cpu_score} | Draws: {self.draws}")
        self.reset_game()

    def reset_game(self):
        self.board = ["_" for _ in range(9)]
        self.game_end = False
        for btn in self.buttons:
            btn.config(text="", state="normal")

    def check_winner(self):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for combo in wins:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "_":
                return self.board[combo[0]]
        if "_" not in self.board: return "Draw"
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = RainbowTicTacToe(root)
    root.mainloop()