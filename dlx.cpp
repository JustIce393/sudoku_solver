#include "dlx.h"

DlxSolver::DlxSolver(int num_cols) {
    // Initialize root node to point to itself in all directions
    root.left = &root;
    root.right = &root;
    root.up = &root;
    root.down = &root;
    root.col = &root;
    root.col_idx = -1;
    root.name = "root";

    ColumnNode* prev = &root;
    columns.reserve(num_cols);
    for (int i = 0; i < num_cols; ++i) {
        auto col = std::make_unique<ColumnNode>();
        col->col_idx = i;
        col->name = "C" + std::to_string(i);
        
        // Circular horizontal link
        col->left = prev;
        col->right = &root;
        col->up = col.get();
        col->down = col.get();
        col->col = col.get();
        
        prev->right = col.get();
        root.left = col.get();
        prev = col.get();
        
        columns.push_back(std::move(col));
    }
}

void DlxSolver::add_row(int row_idx, const std::vector<int>& col_indices) {
    if (col_indices.empty()) return;
    
    Node* first_new_node = nullptr;
    Node* prev_new_node = nullptr;
    
    for (int col_idx : col_indices) {
        if (col_idx < 0 || col_idx >= (int)columns.size()) continue;
        
        auto node = std::make_unique<Node>();
        node->row_idx = row_idx;
        ColumnNode* col_node = columns[col_idx].get();
        node->col = col_node;
        
        // Link node vertically at the bottom of its column list
        Node* last = col_node->up;
        node->down = col_node;
        node->up = last;
        last->down = node.get();
        col_node->up = node.get();
        
        col_node->size++;
        
        // Link node horizontally in the circular list of this row
        if (!first_new_node) {
            first_new_node = node.get();
            first_new_node->left = first_new_node;
            first_new_node->right = first_new_node;
        } else {
            node->left = prev_new_node;
            node->right = first_new_node;
            prev_new_node->right = node.get();
            first_new_node->left = node.get();
        }
        
        prev_new_node = node.get();
        all_nodes.push_back(std::move(node));
    }
}

void DlxSolver::cover(ColumnNode* c) {
    // Unlink the column header from the column list
    c->right->left = c->left;
    c->left->right = c->right;
    
    // For each row in the column, unlink all of its nodes from their columns
    for (Node* i = c->down; i != c; i = i->down) {
        for (Node* j = i->right; j != i; j = j->right) {
            j->down->up = j->up;
            j->up->down = j->down;
            j->col->size--;
        }
    }
}

void DlxSolver::uncover(ColumnNode* c) {
    // For each row in the column (in reverse order), relink all of its nodes back into their columns
    for (Node* i = c->up; i != c; i = i->up) {
        for (Node* j = i->left; j != i; j = j->left) {
            j->col->size++;
            j->down->up = j;
            j->up->down = j;
        }
    }
    
    // Relink the column header back into the column list
    c->right->left = c;
    c->left->right = c;
}

ColumnNode* DlxSolver::select_column() {
    ColumnNode* min_col = nullptr;
    int min_size = 1e9;
    
    // Scan all active columns to find the one with the smallest size (MRV heuristic)
    for (Node* c = root.right; c != &root; c = c->right) {
        ColumnNode* col_node = static_cast<ColumnNode*>(c);
        if (col_node->size < min_size) {
            min_size = col_node->size;
            min_col = col_node;
            // Quick optimization: if size is 0 or 1, we can't do better
            if (min_size <= 1) {
                break;
            }
        }
    }
    return min_col;
}

bool DlxSolver::solve(const std::function<bool(const std::vector<int>&)>& on_solution) {
    std::vector<int> current_solution;
    return search(0, current_solution, on_solution);
}

bool DlxSolver::search(int depth, std::vector<int>& current_solution, const std::function<bool(const std::vector<int>&)>& on_solution) {
    // If no columns are left in the header list, a solution is found!
    if (root.right == &root) {
        return on_solution(current_solution);
    }
    
    ColumnNode* c = select_column();
    if (!c) return false;
    
    cover(c);
    
    for (Node* r = c->down; r != c; r = r->down) {
        current_solution.push_back(r->row_idx);
        
        // Cover all columns satisfied by selecting row r
        for (Node* j = r->right; j != r; j = j->right) {
            cover(j->col);
        }
        
        // Recurse to solve remaining sub-problem
        if (search(depth + 1, current_solution, on_solution)) {
            return true;
        }
        
        // Backtrack: uncover columns satisfied by row r (in reverse order)
        for (Node* j = r->left; j != r; j = j->left) {
            uncover(j->col);
        }
        
        current_solution.pop_back();
    }
    
    uncover(c);
    return false;
}
