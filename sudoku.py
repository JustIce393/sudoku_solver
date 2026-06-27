from dlx import DlxSolver

class SudokuSolver:
    def __init__(self):
        self.initial_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solutions = []

    def load_from_string(self, s):
        """Load Sudoku from an 81-character string."""
        chars = [c for c in s if c in ('.', '0') or ('1' <= c <= '9')]
        if len(chars) != 81:
            return False
        
        self.initial_grid = [[0 for _ in range(9)] for _ in range(9)]
        for i, char in enumerate(chars):
            r = i // 9
            c = i % 9
            if char == '.':
                self.initial_grid[r][c] = 0
            else:
                self.initial_grid[r][c] = int(char)
        
        self.solutions = []
        return True

    def load_from_grid(self, g):
        """Load Sudoku from a 2D 9x9 list."""
        if len(g) != 9:
            return False
        for r in range(9):
            if len(g[r]) != 9:
                return False
            for c in range(9):
                if not (0 <= g[r][c] <= 9):
                    return False
        
        self.initial_grid = [row[:] for row in g]
        self.solutions = []
        return True

    def decode_row(self, row_idx):
        """Decode exact cover row index to (r, c, val) (all 0-indexed)."""
        val = row_idx % 9
        temp = row_idx // 9
        c = temp % 9
        r = temp // 9
        return r, c, val

    def encode_row(self, r, c, val):
        """Encode (r, c, val) to a unique exact cover row index."""
        return r * 81 + c * 9 + val

    def solve(self, limit_solutions=1):
        """Solves the Sudoku puzzle. Returns True if solved, False otherwise."""
        self.solutions = []
        
        # 324 constraints (columns)
        solver = DlxSolver(324)
        
        for r in range(9):
            for c in range(9):
                fixed_val = self.initial_grid[r][c]
                
                # If pre-filled, only generate one row choice. Otherwise, all 9.
                start_val = fixed_val - 1 if fixed_val != 0 else 0
                end_val = fixed_val - 1 if fixed_val != 0 else 8
                
                for val in range(start_val, end_val + 1):
                    row_idx = self.encode_row(r, c, val)
                    box = (r // 3) * 3 + (c // 3)
                    
                    # Columns representing constraints:
                    # 1. Cell: Cell (r, c) is filled. [0-80]
                    # 2. Row: Row r has value val. [81-161]
                    # 3. Col: Col c has value val. [162-242]
                    # 4. Box: Box box has value val. [243-323]
                    col_indices = [
                        r * 9 + c,
                        81 + r * 9 + val,
                        162 + c * 9 + val,
                        243 + box * 9 + val
                    ]
                    solver.add_row(row_idx, col_indices)
        
        def on_solution(dlx_solution):
            solved_grid = [[0 for _ in range(9)] for _ in range(9)]
            for row_idx in dlx_solution:
                r_dec, c_dec, val_dec = self.decode_row(row_idx)
                solved_grid[r_dec][c_dec] = val_dec + 1
            
            self.solutions.append(solved_grid)
            
            # Stop if we hit our limit
            if limit_solutions > 0 and len(self.solutions) >= limit_solutions:
                return True
            return False

        solver.solve(on_solution)
        return len(self.solutions) > 0

    def print_grid(self, grid=None):
        """Prints a 9x9 grid in human-readable ASCII layout."""
        if grid is None:
            grid = self.initial_grid
            
        print("+-------+-------+-------+")
        for r in range(9):
            row_str = "| "
            for c in range(9):
                val = grid[r][c]
                row_str += f"{val if val != 0 else '.'} "
                if (c + 1) % 3 == 0:
                    row_str += "| "
            print(row_str)
            if (r + 1) % 3 == 0:
                print("+-------+-------+-------+")
