#ifndef DLX_H
#define DLX_H

#include <vector>
#include <string>
#include <functional>
#include <memory>

struct ColumnNode;

// Represents a node in the 4-way circular doubly linked list.
struct Node {
    Node* left = nullptr;
    Node* right = nullptr;
    Node* up = nullptr;
    Node* down = nullptr;
    ColumnNode* col = nullptr;
    int row_idx = -1; // Index representing the row candidate this node belongs to
};

// Represents a column header in the exact cover matrix.
struct ColumnNode : public Node {
    int size = 0;        // Number of active 1s in this column
    std::string name;    // Name of the constraint (useful for debugging)
    int col_idx = -1;    // Index of the column constraint
};

// DlxSolver implements Knuth's Algorithm X using Dancing Links.
class DlxSolver {
public:
    DlxSolver(int num_cols);
    ~DlxSolver() = default;

    // Disable copy/move to avoid pointer invalidation
    DlxSolver(const DlxSolver&) = delete;
    DlxSolver& operator=(const DlxSolver&) = delete;
    DlxSolver(DlxSolver&&) = delete;
    DlxSolver& operator=(DlxSolver&&) = delete;

    // Adds a row of 1s at the specified col_indices (0-based) to the exact cover matrix
    void add_row(int row_idx, const std::vector<int>& col_indices);

    // Solves the exact cover problem. Invokes on_solution for each solution found.
    // If on_solution returns true, search terminates.
    // Returns true if a solution was found and search was stopped.
    bool solve(const std::function<bool(const std::vector<int>&)>& on_solution);

private:
    ColumnNode root;
    std::vector<std::unique_ptr<ColumnNode>> columns;
    std::vector<std::unique_ptr<Node>> all_nodes; // Owns all matrix nodes for easy memory cleanup

    // Core DLX operations
    void cover(ColumnNode* c);
    void uncover(ColumnNode* c);
    ColumnNode* select_column();
    bool search(int depth, std::vector<int>& current_solution, const std::function<bool(const std::vector<int>&)>& on_solution);
};

#endif // DLX_H
