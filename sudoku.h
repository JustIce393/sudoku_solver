#ifndef SUDOKU_H
#define SUDOKU_H

#include <vector>
#include <string>
#include "dlx.h"

class SudokuSolver {
public:
    SudokuSolver();
    ~SudokuSolver() = default;

    // Load Sudoku from a string of 81 characters (e.g. "53..7....6..195....")
    // where '.' or '0' represents an empty cell.
    bool load_from_string(const std::string& s);

    // Load Sudoku from a 9x9 grid
    bool load_from_grid(const std::vector<std::vector<int>>& g);

    // Solves the Sudoku. Returns true if at least one solution is found.
    // limit_solutions: max number of solutions to find (0 for all solutions)
    bool solve(int limit_solutions = 1);

    // Prints the initial grid in a human-readable ASCII layout
    void print_initial_grid() const;

    // Prints the specified solution grid in a human-readable ASCII layout
    void print_solution(int solution_idx = 0) const;

    // Get the list of solved grids
    const std::vector<std::vector<std::vector<int>>>& get_solutions() const {
        return solutions;
    }

private:
    std::vector<std::vector<int>> initial_grid;
    std::vector<std::vector<std::vector<int>>> solutions;

    // Decode a DLX row index to Sudoku triplet: row r, col c, value val (all 0-indexed)
    void decode_row(int row_idx, int& r, int& c, int& val) const;

    // Encode Sudoku triplet to a unique DLX row index
    int encode_row(int r, int c, int val) const;

    // Helper to print a 9x9 grid
    void print_raw_grid(const std::vector<std::vector<int>>& grid) const;
};

#endif // SUDOKU_H
