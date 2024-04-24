from logic import Grid
import tkinter as tk
from tkinter import simpledialog, messagebox
from MCT_heuristic import *



tile_colors = {
    0: "#CDC1B4",
    2: "#eee4da",
    4: "#eee1c9",
    8: "#f3b27a",
    16: "#f69664",
    32: "#f77c5f",
    64: "#F65E3B",
    128: "#EDCF73",
    256: "#EDCC62",
    512: "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22D",
}

text_colors = {
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#F9F6F2",
    128: "#F9F6F2",
    256: "#F9F6F2",
    512: "#F9F6F2",
    1024: "#F9F6F2",
    2048: "#F9F6F2",
}


class GameUI:
    def __init__(self, grid, size=4):
        self.size = size
        self.grid = grid
        self.root = tk.Tk()
        self.root.title("2048")

        "probably better to have a function for the setup!!!"

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#faf8ef", bd=2, padx=10, pady=10)
        self.main_frame.pack(padx=10, pady=10)

        # Header Frame
        self.header_frame = tk.Frame(self.main_frame, bg="#faf8ef")
        self.header_frame.pack(pady=(0, 20))

        self.title_label = tk.Label(
            self.header_frame, bg="#faf8ef", text="2048", font=("Helvetica", 30, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=5)

        self.score_label = tk.Label(
            self.header_frame, bg="#bbada0", text="Score: 0", font=("Helvetica", 20)
        )
        self.score_label.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(
            self.header_frame,
            bg="#8f7a66",
            text="New Game",
            command=self.reset_game,
            font=("Helvetica", 16),
        )
        self.reset_button.grid(row=0, column=2, padx=5)

        self.change_size_button = tk.Button(
            self.header_frame,
            bg="#8f7a66",
            text="Grid Size",
            command=self.change_grid_size,
            font=("Helvetica", 16),
        )
        self.change_size_button.grid(row=0, column=3, padx=5)

        self.ai_run_button = tk.Button(
            self.header_frame,
            bg="#8f7a66",
            text="Run AI",
            command=self.run_ai_game,
            font=("Helvetica", 16),
        )
        self.ai_run_button.grid(row=0, column=4, padx=5)

        # Game Grid Frame
        self.grid_frame = tk.Frame(self.main_frame, bg="#776e65")
        self.grid_frame.pack()

        self.tiles = {}
        self.init_grid()

    def init_grid(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                tile = tk.Label(
                    self.grid_frame,
                    text="",
                    bg="azure3",
                    font=("Helvetica", 22),
                    width=4,
                    height=2,
                )
                tile.grid(row=i, column=j, padx=5, pady=5)
                self.tiles[(i, j)] = tile
        self.update_grid()

    def update_grid(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                value = self.grid.matrix[i][j]
                tile = self.tiles[(i, j)]
                bg_color = tile_colors.get(value, "azure3")
                fg_color = text_colors.get(value, "black")
                if value == 0:
                    tile.config(
                        text="", bg=bg_color, fg="black"
                    )  
                else:
                    font_settings = (
                        "Helvetica",
                        22,
                        "bold",
                    ) 
                    tile.config(
                        text=str(value), bg=bg_color, fg=fg_color, font=font_settings
                    )

        self.score_label.config(text=f"Score: {self.grid.score}")
        self.root.update_idletasks()

    def change_grid_size(self):
        # Prompt user for new grid size
        new_size = simpledialog.askinteger(
            "Change Grid Size",
            "Enter new grid size (min 2, max 10):",
            minvalue=2,
            maxvalue=10,
        )
        if new_size is not None and 2 <= new_size <= 10:
            self.grid = Grid(new_size)
            self.size = new_size
            self.tiles = {}
            self.grid_frame.destroy()  
            self.grid_frame = tk.Frame(
                self.main_frame, bg="#faf8ef"
            )  # Create a new grid frame
            self.grid_frame.pack()
            self.init_grid()
            self.update_grid()
            self.start()
        else:
            messagebox.showwarning(
                "Invalid Size", "The grid size must be an integer between 2 and 10."
            )

    def key_pressed(self, event):
        if event.keysym == "Left":
            self.grid.shift_left()
        elif event.keysym == "Right":
            self.grid.shift_right()
        elif event.keysym == "Up":
            self.grid.shift_up()
        elif event.keysym == "Down":
            self.grid.shift_down()
        else:
            return  

        self.update_grid()  

    
        if self.grid.is_gameover() is True:
            messagebox.showinfo("Game Over", "Game over")

    def reset_game(self):
        self.grid = Grid(self.size) 
        self.grid.start_game()
        self.update_grid()

    def start(self):
        self.root.bind("<Key>", self.key_pressed)
        self.grid.start_game()
        self.update_grid()
        self.root.mainloop()

    def run_ai_game(self):
        if self.grid.is_gameover() is True:
            messagebox.showinfo("Game Over", "Game over")
            return
        best_move = monte_carlo_tree_search(self.grid)
        getattr(self.grid, f"shift_{best_move}")()
        self.update_grid()
        if self.grid.is_gameover() is True:
            messagebox.showinfo("Game Over", "Game over")
        else:
            self.root.after(10, self.run_ai_game) 


if __name__ == "__main__":
    game_grid = Grid()
    app = GameUI(game_grid)
    app.start()
