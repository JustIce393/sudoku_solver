CXX = g++
CXXFLAGS = -O3 -Wall -Wextra -std=c++17

TARGET = sudoku_solver
SRCS = main.cpp dlx.cpp sudoku.cpp
OBJS = $(SRCS:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET) $(TARGET).exe
