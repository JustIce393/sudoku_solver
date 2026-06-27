#include "sudoku.h"
#include <iostream>
#include <iomanip>
#include <algorithm>

SudokuSolver::SudokuSolver() {
    initial_grid.assign(9, std::vector<int>(9, 0));
}

bool SudokuSolver::load_from_string(const std::string& s) {
    std::vector<char> chars;
    for (char c : s) {
        if (c == '.' || c == '0' || (c >= '1' && c <= '9')) {
            chars.push_back(c);
        }
    }
    if (chars.size() != 81) return false;
    
    initial_grid.assign(9, std::vector<int>(9, 0));
    for (int i = 0; i < 81; ++i) {
        int r = i / 9;
        int c = i % 9;
        if (chars[i] == '.') {
            initial_grid[r][c] = 0;
        } else {
            initial_grid[r][c] = chars[i] - '0';
        }
    }
    solutions.clear();
    return true;
}

bool SudokuSolver::load_from_grid(const std::vector<std::vector<int>>& g) {
    if (g.size() != 9) return false;
    for (int r = 0; r < 9; ++r) {
        if (g[r].size() != 9) return false;
        for (int c = 0; c < 9; ++c) {
            if (g[r][c] < 0 || g[r][c] > 9) return false;
        }
    }
    initial_grid = g;
    solutions.clear();
    return true;
}

void SudokuSolver::decode_row(int row_idx, int& r, int& c, int& val) const {
    val = row_idx % 9;
    int temp = row_idx / 9;
    c = temp % 9;
    r = temp / 9;
}

int SudokuSolver::encode_row(int r, int c, int val) const {
    return r * 81 + c * 9 + val;
}

bool SudokuSolver::solve(int limit_solutions) {
    solutions.clear();
    
    // Exact cover matrix has 324 columns for standard 9x9 Sudoku
    DlxSolver solver(324);
    
    // Populate rows in the exact cover matrix
    for (int r = 0; r < 9; ++r) {
        for (int c = 0; c < 9; ++c) {
            int fixed_val = initial_grid[r][c];
            
            // If cell is pre-filled, we only add the candidate row for that value.
            // Otherwise, we add all 9 candidate rows (values 0 to 8).
            int start_val = (fixed_val != 0) ? (fixed_val - 1) : 0;
            int end_val = (fixed_val != 0) ? (fixed_val - 1) : 8;
            
            for (int val = start_val; val <= end_val; ++val) {
                int row_idx = encode_row(r, c, val);
                int box = (r / 3) * 3 + (c / 3);
                
                // Constraints:
                // 1. Cell Constraint: Cell (r, c) is filled. [0, 80]
                // 2. Row Constraint: Row r has value val. [81, 161]
                // 3. Column Constraint: Col c has value val. [162, 242]
                // 4. Box Constraint: Box box has value val. [243, 323]
                std::vector<int> col_indices = {
                    r * 9 + c,
                    81 + r * 9 + val,
                    162 + c * 9 + val,
                    243 + box * 9 + val
                };
                
                solver.add_row(row_idx, col_indices);
            }
        }
    }
    
    // Callback when DLX finds a solution
    auto on_solution = [&](const std::vector<int>& dlx_solution) -> bool {
        std::vector<std::vector<int>> solved_grid(9, std::vector<int>(9, 0));
        for (int row_idx : dlx_solution) {
            int r, c, val;
            decode_row(row_idx, r, c, val);
            solved_grid[r][c] = val + 1;
        }
        solutions.push_back(solved_grid);
        
        // Stop solving if we have reached our limit (and limit_solutions > 0)
        if (limit_solutions > 0 && (int)solutions.size() >= limit_solutions) {
            return true; // Terminate search
        }
        return false; // Keep searching
    };
    
    solver.solve(on_solution);
    return !solutions.empty();
}

void SudokuSolver::print_initial_grid() const {
    print_raw_grid(initial_grid);
}

void SudokuSolver::print_solution(int solution_idx) const {
    if (solution_idx < 0 || solution_idx >= (int)solutions.size()) {
        std::cout << "Invalid solution index: " << solution_idx << "\n";
        return;
    }
    print_raw_grid(solutions[solution_idx]);
}

void SudokuSolver::print_raw_grid(const std::vector<std::vector<int>>& grid) const {
    std::cout << "+-------+-------+-------+\n";
    for (int r = 0; r < 9; ++r) {
        std::cout << "| ";
        for (int c = 0; c < 9; ++c) {
            if (grid[r][c] == 0) {
                std::cout << ". ";
            } else {
                std::cout << grid[r][c] << " ";
            }
            if ((c + 1) % 3 == 0) {
                std::cout << "| ";
            }
        }
        std::cout << "\n";
        if ((r + 1) % 3 == 0) {
            std::cout << "+-------+-------+-------+\n";
        }
    }
}
