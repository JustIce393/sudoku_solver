import tkinter as tk
from tkinter import messagebox
import time
from sudoku import SudokuSolver

# --- Cyberpunk/Neon High-Vibrancy Palette ---
COLOR_BG = "#06070c"          # Space Pitch Black (Main window background)
COLOR_CRUST = "#0c0d16"       # Dark Room crust (Sudoku board background)
COLOR_SURFACE = "#1c122c"     # Deep Glowing Violet (Selected cell overlay)
COLOR_HOVER = "#121324"       # Soft Indigo (Hovered cell background)
COLOR_TEXT = "#e2e4f0"        # Crisp Off-White (Labels and instructions)
COLOR_LINE_THIN = "#1e2035"   # Thin grid lines
COLOR_LINE_THICK = "#58609a"  # Vibrant Indigo-Blue (Thick 3x3 block dividers)
COLOR_CLUE = "#ff2a2a"        # Vibrant Neon Red (Problem clues)
COLOR_USER = "#ff2a2a"        # Vibrant Neon Red (User entered clues)
COLOR_SOLVED = "#39ff14"      # Ultra Neon Green (Solution)
COLOR_ACCENT = "#7f00ff"      # Electric Violet (Buttons and main bezel outline)
COLOR_SELECT = "#39ff14"      # Ultra Neon Green (Glowing cell selection border)
COLOR_ERROR = "#ff2a2a"       # Vivid Red (Errors/Contradictions)
COLOR_STATUS_TXT = "#a2a6c2"  # Slate Gray (Status message)

CELL_SIZE = 58
MARGIN = 25
BOARD_SIZE = 9 * CELL_SIZE

def draw_rounded_rect(canvas, x1, y1, x2, y2, r, fill, outline="", width=1):
    """Draws a mathematically precise rounded rectangle on a Tkinter Canvas."""
    # Corners
    canvas.create_oval(x1, y1, x1 + 2*r, y1 + 2*r, fill=fill, outline=outline, width=width)
    canvas.create_oval(x2 - 2*r, y1, x2, y1 + 2*r, fill=fill, outline=outline, width=width)
    canvas.create_oval(x1, y2 - 2*r, x1 + 2*r, y2, fill=fill, outline=outline, width=width)
    canvas.create_oval(x2 - 2*r, y2 - 2*r, x2, y2, fill=fill, outline=outline, width=width)
    
    # Inner boxes
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill, outline="")
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill, outline="")
    
    # Borders
    if outline:
        canvas.create_line(x1 + r, y1, x2 - r, y1, fill=outline, width=width)
        canvas.create_line(x1 + r, y2, x2 - r, y2, fill=outline, width=width)
        canvas.create_line(x1, y1 + r, x1, y2 - r, fill=outline, width=width)
        canvas.create_line(x2, y1 + r, x2, y2 - r, fill=outline, width=width)


class ModernButton(tk.Canvas):
    """Custom Canvas-based button with rounded corners and smooth hover transitions."""
    def __init__(self, parent, text, command, bg_color=COLOR_ACCENT, hover_color="#b4befe", fg_color="#ffffff", is_outline=False, width=250, height=44):
        super().__init__(parent, width=width, height=height, bg=COLOR_BG, highlightthickness=0, cursor="hand2")
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.is_outline = is_outline
        self.width = width
        self.height = height
        
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.draw(self.bg_color if not self.is_outline else COLOR_BG)
        
    def draw(self, fill_color):
        self.delete("all")
        x1, y1 = 2, 2
        x2, y2 = self.width - 2, self.height - 2
        r = 12
        
        if self.is_outline:
            # Hollow outline button
            draw_rounded_rect(self, x1, y1, x2, y2, r, fill=fill_color, outline=self.bg_color, width=1.5)
            text_color = self.bg_color if fill_color == COLOR_BG else COLOR_TEXT
        else:
            # Solid button
            draw_rounded_rect(self, x1, y1, x2, y2, r, fill=fill_color, outline="")
            text_color = self.fg_color
            
        self.create_text(
            self.width // 2, 
            self.height // 2, 
            text=self.text, 
            font=("Segoe UI", 11, "bold"), 
            fill=text_color
        )
        
    def on_enter(self, event):
        if self.is_outline:
            self.draw(COLOR_SURFACE)
        else:
            self.draw(self.hover_color)
        
    def on_leave(self, event):
        if self.is_outline:
            self.draw(COLOR_BG)
        else:
            self.draw(self.bg_color)


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("1100x660")  # Spacious widescreen layout
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        self.solver = SudokuSolver()
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.is_clue = [[False for _ in range(9)] for _ in range(9)]
        self.is_solved = [[False for _ in range(9)] for _ in range(9)]
        
        self.selected_cell = None
        self.hovered_cell = None

        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        # --- Left Side: Board Panel (Padded) ---
        self.left_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.left_frame.pack(side=tk.LEFT, padx=(80, 50), pady=30)

        canvas_dim = BOARD_SIZE + 2 * MARGIN
        self.canvas = tk.Canvas(
            self.left_frame, 
            width=canvas_dim, 
            height=canvas_dim, 
            bg=COLOR_BG, 
            highlightthickness=0
        )
        self.canvas.pack()

        # Canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_hover)
        self.canvas.bind("<Leave>", self.on_canvas_leave)
        self.root.bind("<Key>", self.on_key_press)

        # --- Right Side: Controls Panel (Wider padding) ---
        self.right_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(50, 80), pady=35)

        # Header Title
        title_lbl = tk.Label(
            self.right_frame, 
            text="SUDOKU SOLVER", 
            font=("Segoe UI", 24, "bold"), 
            bg=COLOR_BG, 
            fg="#ffffff"  # High-contrast white title
        )
        title_lbl.pack(anchor=tk.W, pady=(25, 10), ipady=5)

        # Divider (Electric Purple)
        divider = tk.Frame(self.right_frame, height=3, bg=COLOR_ACCENT)
        divider.pack(fill=tk.X, pady=(0, 20))

        # Instructions list
        instructions = (
            "Interactive Board Guide:\n"
            "• Click a cell to select it.\n"
            "• Type digits 1-9 to input clues.\n"
            "• Use Backspace/Delete to clear.\n"
            "• Use Arrow keys to navigate.\n"
        )
        info_lbl = tk.Label(
            self.right_frame, 
            text=instructions, 
            font=("Segoe UI", 11), 
            bg=COLOR_BG, 
            fg=COLOR_TEXT, 
            justify=tk.LEFT,
            anchor="w"
        )
        info_lbl.pack(anchor=tk.W, pady=(0, 25))

        # Styled Modern Buttons
        self.btn_solve = ModernButton(
            self.right_frame, 
            text="Solve Board", 
            command=self.solve_sudoku, 
            bg_color="#39ff14",     # Explicit Neon Green
            hover_color="#5ff77e",  # Lighter neon green
            fg_color="#06070c"
        )
        self.btn_solve.pack(pady=6)

        self.btn_clear_solved = ModernButton(
            self.right_frame, 
            text="Clear Solver Solution", 
            command=self.clear_solution_only, 
            bg_color="#ff9f1c",  # Warning Orange
            is_outline=True
        )
        self.btn_clear_solved.pack(pady=6)

        self.btn_clear = ModernButton(
            self.right_frame, 
            text="Reset Entire Board", 
            command=self.clear_board, 
            bg_color=COLOR_ERROR,  # Vivid Red
            is_outline=True
        )
        self.btn_clear.pack(pady=6)

        self.btn_demo = ModernButton(
            self.right_frame, 
            text="Load Notorious 17 Clues", 
            command=self.load_demo, 
            bg_color=COLOR_ACCENT,  # Electric Purple
            is_outline=True
        )
        self.btn_demo.pack(pady=6)

        # Spacer
        spacer = tk.Frame(self.right_frame, bg=COLOR_BG)
        spacer.pack(fill=tk.BOTH, expand=True)

        # Status Panel (At bottom)
        self.status_container = tk.Canvas(self.right_frame, width=250, height=45, bg=COLOR_BG, highlightthickness=0)
        self.status_container.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        self.update_status("Ready", COLOR_STATUS_TXT)

    def update_status(self, text, color):
        """Draws a beautiful rounded box for status messages."""
        self.status_container.delete("all")
        x1, y1 = 2, 2
        x2, y2 = 248, 43
        draw_rounded_rect(self.status_container, x1, y1, x2, y2, 8, fill=COLOR_CRUST, outline=COLOR_LINE_THIN)
        self.status_container.create_text(
            125, 22,
            text=f"Status: {text}",
            font=("Segoe UI", 10, "bold"),
            fill=color,
            width=230
        )

    def draw_board(self):
        self.canvas.delete("all")

        # 1. Draw outer rounded boundary
        draw_rounded_rect(
            self.canvas, 
            MARGIN - 6, 
            MARGIN - 6, 
            MARGIN + BOARD_SIZE + 6, 
            MARGIN + BOARD_SIZE + 6, 
            12, 
            fill=COLOR_CRUST, 
            outline=COLOR_LINE_THICK, 
            width=2.5
        )

        # 2. Draw cell backgrounds (selection or hover)
        for r in range(9):
            for c in range(9):
                x1 = MARGIN + c * CELL_SIZE
                y1 = MARGIN + r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                # Check status
                if self.selected_cell == (r, c):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_SURFACE, outline="")
                elif self.hovered_cell == (r, c):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_HOVER, outline="")

        # 3. Draw grid lines
        for i in range(10):
            width = 2.5 if i % 3 == 0 else 1
            color = COLOR_LINE_THICK if i % 3 == 0 else COLOR_LINE_THIN
            
            coord = MARGIN + i * CELL_SIZE
            # Horizontal lines
            self.canvas.create_line(MARGIN, coord, MARGIN + BOARD_SIZE, coord, fill=color, width=width)
            # Vertical lines
            self.canvas.create_line(coord, MARGIN, coord, MARGIN + BOARD_SIZE, fill=color, width=width)

        # 4. Highlight selection cell borders with a neon indicator
        if self.selected_cell:
            r, c = self.selected_cell
            x1 = MARGIN + c * CELL_SIZE
            y1 = MARGIN + r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, outline=COLOR_SELECT, width=2.5)

        # 5. Draw numbers
        for r in range(9):
            for c in range(9):
                val = self.grid[r][c]
                if val == 0:
                    continue
                
                # Color code
                if self.is_clue[r][c]:
                    color = COLOR_CLUE
                elif self.is_solved[r][c]:
                    color = COLOR_SOLVED
                else:
                    color = COLOR_USER
                
                x = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
                y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
                self.canvas.create_text(
                    x, y, 
                    text=str(val), 
                    font=("Segoe UI", 18, "bold"), 
                    fill=color
                )

    def get_cell_under_cursor(self, event):
        x = event.x - MARGIN
        y = event.y - MARGIN
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            c = int(x // CELL_SIZE)
            r = int(y // CELL_SIZE)
            return r, c
        return None

    def on_canvas_click(self, event):
        self.canvas.focus_set()
        cell = self.get_cell_under_cursor(event)
        if cell:
            self.selected_cell = cell
        else:
            self.selected_cell = None
        self.draw_board()

    def on_canvas_hover(self, event):
        cell = self.get_cell_under_cursor(event)
        if cell != self.hovered_cell:
            self.hovered_cell = cell
            self.draw_board()

    def on_canvas_leave(self, event):
        if self.hovered_cell is not None:
            self.hovered_cell = None
            self.draw_board()

    def on_key_press(self, event):
        if not self.selected_cell:
            return
        
        r, c = self.selected_cell
        key = event.keysym
        
        # Grid Navigation
        if key == "Up":
            self.selected_cell = (max(0, r - 1), c)
            self.draw_board()
        elif key == "Down":
            self.selected_cell = (min(8, r + 1), c)
            self.draw_board()
        elif key == "Left":
            self.selected_cell = (r, max(0, c - 1))
            self.draw_board()
        elif key == "Right":
            self.selected_cell = (r, min(8, c + 1))
            self.draw_board()
            
        # Values Entry
        elif event.char in "123456789":
            val = int(event.char)
            self.is_solved[r][c] = False
            self.is_clue[r][c] = True
            self.grid[r][c] = val
            self.draw_board()
        elif key in ("BackSpace", "Delete") or event.char == "0":
            self.grid[r][c] = 0
            self.is_clue[r][c] = False
            self.is_solved[r][c] = False
            self.draw_board()

    def solve_sudoku(self):
        # Clear any previously solved cells before starting a new solve
        for r in range(9):
            for c in range(9):
                if self.is_solved[r][c]:
                    self.grid[r][c] = 0
                    self.is_solved[r][c] = False

        # Establish clues from current grid state
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] != 0 and not self.is_solved[r][c]:
                    self.is_clue[r][c] = True
                else:
                    self.is_clue[r][c] = False
                    self.is_solved[r][c] = False
        
        self.solver.load_from_grid(self.grid)
        self.update_status("Solving...", COLOR_SELECT)
        self.root.update()
        
        start_time = time.perf_counter()
        solved = self.solver.solve(limit_solutions=1)
        end_time = time.perf_counter()
        
        duration_ms = (end_time - start_time) * 1000.0
        
        if solved:
            solutions = self.solver.solutions
            solved_grid = solutions[0]
            
            # Fill grid and tag solved cells
            for r in range(9):
                for c in range(9):
                    if not self.is_clue[r][c]:
                        self.grid[r][c] = solved_grid[r][c]
                        self.is_solved[r][c] = True
            
            self.update_status(f"Solved in {duration_ms:.2f} ms!", COLOR_USER)
        else:
            self.update_status("No solution exists!", COLOR_ERROR)
            messagebox.showerror("Error", "No solution exists for the current board configuration.")
            
        self.draw_board()

    def clear_solution_only(self):
        """Clears cells filled by the solver, preserving user inputs."""
        for r in range(9):
            for c in range(9):
                if self.is_solved[r][c]:
                    self.grid[r][c] = 0
                    self.is_solved[r][c] = False
        self.update_status("Solution Cleared", COLOR_STATUS_TXT)
        self.draw_board()

    def clear_board(self):
        """Resets the entire board state."""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.is_clue = [[False for _ in range(9)] for _ in range(9)]
        self.is_solved = [[False for _ in range(9)] for _ in range(9)]
        self.selected_cell = None
        self.update_status("Grid Cleared", COLOR_STATUS_TXT)
        self.draw_board()

    def load_demo(self):
        """Loads a notorious, minimal 17-clue grid."""
        self.clear_board()
        demo_str = "000000010400000000020000000000050407008000300001090000300400200050100000000806000"
        
        for i, char in enumerate(demo_str):
            r = i // 9
            c = i % 9
            val = int(char)
            if val != 0:
                self.grid[r][c] = val
                self.is_clue[r][c] = True
        
        self.update_status("Demo clues loaded", COLOR_STATUS_TXT)
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
