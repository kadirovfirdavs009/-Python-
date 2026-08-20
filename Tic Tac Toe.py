import tkinter as tk
from tkinter import messagebox
import winsound  # Built-in Windows library for audio effects

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Audio & Visual Edition")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        # Game state variables
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.scores = {"X": 0, "O": 0, "Ties": 0}

        self.setup_ui()

    def play_audio(self, sound_type):
        """Plays audio effects using built-in Windows sound frequencies."""
        try:
            if sound_type == "move":
                # Short frequency beep for a move
                pitch = 700 if self.current_player == "X" else 500
                winsound.Beep(pitch, 80)
            elif sound_type == "win":
                # Winning sound sequence
                for freq in [523, 659, 784, 1046]:
                    winsound.Beep(freq, 100)
            elif sound_type == "tie":
                # Tie sound
                winsound.Beep(300, 250)
        except Exception:
            # Silently pass if platform doesn't support winsound
            pass

    def setup_ui(self):
        # Header / Title
        title_label = tk.Label(
            self.root,
            text="TIC TAC TOE",
            font=("Comic Sans MS", 22, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(15, 5))

        # Score Tracker Display
        self.score_label = tk.Label(
            self.root,
            text=self.get_score_text(),
            font=("Arial", 12, "bold"),
            bg="#181825",
            fg="#a6adc8",
            padx=10,
            pady=5
        )
        self.score_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))

        # 3x3 Grid Frame
        grid_frame = tk.Frame(self.root, bg="#11111b", padx=5, pady=5)
        grid_frame.grid(row=2, column=0, columnspan=3, padx=15, pady=5)

        # Create 9 Buttons for the Game Grid
        for i in range(9):
            row, col = i // 3, i % 3
            btn = tk.Button(
                grid_frame,
                text="",
                font=("Arial", 28, "bold"),
                width=4,
                height=2,
                bg="#313244",
                fg="#cdd6f4",
                activebackground="#45475a",
                relief="flat",
                bd=0,
                command=lambda idx=i: self.handle_click(idx)
            )
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.buttons.append(btn)

        # Reset Button
        reset_btn = tk.Button(
            self.root,
            text="Reset Game",
            font=("Arial", 11, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            activebackground="#eba0ac",
            relief="flat",
            command=self.reset_board
        )
        reset_btn.grid(row=3, column=0, columnspan=3, pady=15)

    def get_score_text(self):
        return f"Player X: {self.scores['X']}   |   Player O: {self.scores['O']}   |   Ties: {self.scores['Ties']}"

    def handle_click(self, index):
        if self.board[index] == "":
            self.play_audio("move")
            self.board[index] = self.current_player

            # Custom visual colors per player
            if self.current_player == "X":
                color = "#89b4fa"  # Soft Blue
            else:
                color = "#f9e2af"  # Soft Yellow

            self.buttons[index].config(text=self.current_player, fg=color, bg="#1e1e2e")

            # Check Game Conditions
            winning_line = self.check_winner()
            if winning_line:
                self.highlight_winner(winning_line)
                self.play_audio("win")
                self.scores[self.current_player] += 1
                self.score_label.config(text=self.get_score_text())
                messagebox.showinfo("Game Over", f"Player {self.current_player} Wins!")
                self.reset_board()
            elif "" not in self.board:
                self.play_audio("tie")
                self.scores["Ties"] += 1
                self.score_label.config(text=self.get_score_text())
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)               # Diagonals
        ]
        for a, b, c in lines:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return (a, b, c)
        return None

    def highlight_winner(self, line):
        """Highlights the winning buttons in green."""
        for idx in line:
            self.buttons[idx].config(bg="#a6e3a1", fg="#11111b")

    def reset_board(self):
        self.board = [""] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text="", bg="#313244", fg="#cdd6f4")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
