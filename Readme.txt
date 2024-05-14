File name: search.py
This file contains the classes and logic to perform iterative deepening search to solve
a 4x4 (15-tile) sliding tile puzzle. It performs depth limited search with different depths
until it finds a solution for the puzzle. It contains different classes to handle the
nodes of the search tree, and store the possible moves to solve the initial position.
The program returns the combination of steps to solve the puzzle, the time taken by
the algorithm, and the maximum memory occupied by the nodes in the tree.

To run the program: create an instance of Search, and call the solve method passing
as a string the initial configuration of the board. Example:
    agent = Search()
    agent.solve("1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15")