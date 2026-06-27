#include <iostream>
#include <string>
#include <chrono>
#include <vector>
#include "sudoku.h"

void print_usage(const char* prog_name) {
    std::cout << "Sudoku Solver using Dancing Links (DLX) Algorithm\n\n";
    std::cout << "Usage: " << prog_name << " [options] [sudoku_string]\n\n";
    std::cout << "Options:\n";
    std::cout << "  -a, --all        Find and print all solutions instead of just the first one\n";
    std::cout << "  -h, --help       Show this help message\n\n";
    std::cout << "Sudoku String Format:\n";
    std::cout << "  An 81-character string where '.' or '0' represents an empty cell,\n";
    std::cout << "  and '1'-'9' represent filled cells.\n";
    std::cout << "  Example: 53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79\n";
}

int main(int argc, char* argv[]) {
    bool find_all = false;
    std::string puzzle_str = "";
    
    // Simple argument parsing
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "-h" || arg == "--help") {
            print_usage(argv[0]);
            return 0;
        } else if (arg == "-a" || arg == "--all") {
            find_all = true;
        } else {
            if (puzzle_str.empty()) {
                puzzle_str = arg;
            } else {
                std::cerr << "Error: Multiple puzzles provided.\n";
                print_usage(argv[0]);
                return 1;
            }
        }
    }
    
    // Default puzzle if none is provided: a highly challenging puzzle (minimum 17 clues)
    if (puzzle_str.empty()) {
        std::cout << "No puzzle provided. Using a default hard puzzle (17 clues):\n";
        puzzle_str = "000000010400000000020000000000050407008000300001090000300400200050100000000806000";
    }
    
    SudokuSolver solver;
    if (!solver.load_from_string(puzzle_str)) {
        std::cerr << "Error: Invalid puzzle string. Must contain exactly 81 characters (digits 1-9, '.' or '0').\n";
        return 1;
    }
    
    std::cout << "\n--- Initial Sudoku Board ---\n";
    solver.print_initial_grid();
    
    std::cout << "\nSolving puzzle using Dancing Links (DLX)...\n";
    
    int limit = find_all ? 0 : 1;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    bool solved = solver.solve(limit);
    auto end_time = std::chrono::high_resolution_clock::now();
    
    auto duration_us = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();
    double duration_ms = duration_us / 1000.0;
    
    const auto& solutions = solver.get_solutions();
    
    if (solved) {
        std::cout << "\n--- Solution(s) Found ---\n";
        for (size_t i = 0; i < solutions.size(); ++i) {
            std::cout << "\nSolution #" << (i + 1) << ":\n";
            solver.print_solution(i);
        }
        std::cout << "\nFound " << solutions.size() << " solution(s) in " 
                  << duration_ms << " ms (" << duration_us << " microseconds).\n";
    } else {
        std::cout << "\nNo solution exists!\n";
        std::cout << "Solver finished in " << duration_ms << " ms (" << duration_us << " microseconds).\n";
    }
    
    return 0;
}
