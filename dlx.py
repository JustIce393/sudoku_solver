class Node:
    """Represents a node in the 4-way circular doubly linked list."""
    def __init__(self, row_idx=-1, col=None):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.col = col  # Reference to ColumnNode
        self.row_idx = row_idx  # Row candidate index


class ColumnNode(Node):
    """Represents a column header in the exact cover matrix."""
    def __init__(self, col_idx=-1, name=""):
        super().__init__()
        self.size = 0  # Number of active 1s in this column
        self.col_idx = col_idx
        self.name = name
        self.col = self  # A column header's col points to itself


class DlxSolver:
    """Implements Donald Knuth's Algorithm X using Dancing Links."""
    def __init__(self, num_cols):
        self.root = ColumnNode(name="root")
        self.columns = []
        
        prev = self.root
        for i in range(num_cols):
            col = ColumnNode(col_idx=i, name=f"C{i}")
            col.left = prev
            col.right = self.root
            prev.right = col
            self.root.left = col
            prev = col
            self.columns.append(col)

    def add_row(self, row_idx, col_indices):
        """Adds a row of 1s at the specified col_indices (0-based) to the matrix."""
        if not col_indices:
            return
        
        first_new_node = None
        prev_new_node = None
        
        for col_idx in col_indices:
            if col_idx < 0 or col_idx >= len(self.columns):
                continue
            
            col_node = self.columns[col_idx]
            node = Node(row_idx=row_idx, col=col_node)
            
            # Link vertically at the bottom of the column list
            last = col_node.up
            node.down = col_node
            node.up = last
            last.down = node
            col_node.up = node
            col_node.size += 1
            
            # Link horizontally in the circular list of this row
            if first_new_node is None:
                first_new_node = node
                first_new_node.left = first_new_node
                first_new_node.right = first_new_node
            else:
                node.left = prev_new_node
                node.right = first_new_node
                prev_new_node.right = node
                first_new_node.left = node
            
            prev_new_node = node

    def cover(self, c):
        """Covers column c, removing it and all conflicting rows from the matrix."""
        c.right.left = c.left
        c.left.right = c.right
        
        i = c.down
        while i != c:
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.col.size -= 1
                j = j.right
            i = i.down

    def uncover(self, c):
        """Uncovers column c, restoring it and its rows back to the matrix."""
        i = c.up
        while i != c:
            j = i.left
            while j != i:
                j.col.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        c.right.left = c
        c.left.right = c

    def select_column(self):
        """Selects the column with the minimum size (MRV heuristic)."""
        min_col = None
        min_size = float('inf')
        
        c = self.root.right
        while c != self.root:
            if c.size < min_size:
                min_size = c.size
                min_col = c
                # Optimization: if size is 0 or 1, we can't do better
                if min_size <= 1:
                    break
            c = c.right
        return min_col

    def solve(self, on_solution):
        """Solves the exact cover problem. Invokes on_solution(list_of_row_indices).
        If on_solution returns True, search terminates early.
        """
        current_solution = []
        return self._search(0, current_solution, on_solution)

    def _search(self, depth, current_solution, on_solution):
        # If no columns remain, we found a solution!
        if self.root.right == self.root:
            return on_solution(current_solution)
        
        c = self.select_column()
        if not c:
            return False
        
        self.cover(c)
        
        r = c.down
        while r != c:
            current_solution.append(r.row_idx)
            
            # Cover columns satisfied by selecting row r
            j = r.right
            while j != r:
                self.cover(j.col)
                j = j.right
            
            # Recurse
            if self._search(depth + 1, current_solution, on_solution):
                return True
            
            # Backtrack: uncover columns (in reverse order)
            j = r.left
            while j != r:
                self.uncover(j.col)
                j = j.left
            
            current_solution.pop()
            r = r.down
            
        self.uncover(c)
        return False
