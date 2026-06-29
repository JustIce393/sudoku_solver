# Exact Cover Sudoku Solver (Dancing Links DLX)

> A high-performance Sudoku game and solver utilizing **Donald Knuth's Dancing Links (DLX)** implementation of **Algorithm X** to solve the Sudoku exact cover matrix. Written in **C++17** and **Python 3**.

![Languages](https://img.shields.io/badge/languages-C%2B%2B17%20%2F%20Python%203-blue)
![Algorithm](https://img.shields.io/badge/algorithm-Knuth%27s%20DLX%20%2F%20Algorithm%20X-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 What is this Project?

This project is a Sudoku game and solver. It showcases:
1. **Exact Cover Modeling:** Formulates the Sudoku puzzle as an exact cover constraint matrix.
2. **Dancing Links (DLX) Engine:** Implements Donald Knuth's DLX pointer-manipulation algorithm, solving even the most difficult Sudoku puzzles (like AI Escargot) in milliseconds.
3. **Cross-Language Code:** Features both a compiled, high-performance C++ CLI solver and an interactive Python desktop application with a Tkinter GUI.

---

## 🏗️ Algorithmic Design: Sudoku as Exact Cover

Sudoku can be modeled as an **exact cover problem**—finding a subset of rows from a binary matrix such that every column contains exactly one `1`.

### The Constraint Matrix
* **Rows (729 candidates):** 9 rows \(\times\) 9 columns \(\times\) 9 values = 729 possible moves.
* **Columns (324 constraints):** A standard 9x9 Sudoku has exactly 324 constraints:
  1. **Cell Constraint (81):** Every cell must contain exactly one number.
  2. **Row Constraint (81):** Every row must contain digits 1–9.
  3. **Column Constraint (81):** Every column must contain digits 1–9.
  4. **Box/Grid Constraint (81):** Every 3x3 box must contain digits 1–9.

### Dancing Links (DLX) Data Structure
DLX represents the sparse matrix as a **4-way circular doubly linked list**. Each cell containing a `1` is represented as a node linked to its neighbors (`up`, `down`, `left`, `right`), with header nodes for columns. 

```
   Columns Headers:   Root  <-->  C0  <-->  C1  <-->  C2
                                   ^         ^
                                   |         |
   Row Nodes:                     Node      Node  <-->  Node
                                   v         v
                                  Node      Node
```

---

## 🛠️ Tech Stack

* **Core Engine:** C++17 (C++ standard templates, compiled CLI).
* **Desktop App:** Python 3, Tkinter (GUI), DLX algorithm mapped in Python.
* **Build System:** Makefile (for C++ compilation).

---

## 🚀 How to Run

### 1. Running the Python GUI App
Ensure Python is installed, then run the batch script:
```bash
run_gui.bat
```
Or run directly:
```bash
python gui.py
```

### 2. Building and Running the C++ CLI
**Compile the binary:**
```bash
make
```
**Solve a puzzle:**
Provide a 81-character string representing the Sudoku board (with `.` or `0` for empty cells):
```bash
./sudoku_solver.exe 000000000302540000050301070000000000000000000000000000000000000000000000000000000
```

---

## 📁 Project Structure

```
sudoku_solver/
├── Makefile            <- Compilation script for C++ engine
├── dlx.h / dlx.cpp     <- C++ Dancing Links node definitions & solver
├── sudoku.h / .cpp     <- C++ board parsing and constraint mapping
├── main.cpp            <- C++ CLI entry point
├── dlx.py              <- Python Dancing Links solver
├── sudoku.py           <- Python Sudoku constraint mapper
├── gui.py              <- Python Tkinter interactive game & solver UI
└── run_gui.bat         <- Windows one-click start script
```


