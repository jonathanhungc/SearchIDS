import random
import math
import time
import psutil
import os
from collections import deque
import sys


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
        self.tiles = tiles

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action == 'L':
            if empty_index % self.size > 0:
                new_tiles[empty_index - 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index - 1]
        if action == 'R':
            if empty_index % self.size < (self.size - 1):
                new_tiles[empty_index + 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index + 1]
        if action == 'U':
            if empty_index - self.size >= 0:
                new_tiles[empty_index - self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index - self.size]
        if action == 'D':
            if empty_index + self.size < self.size * self.size:
                new_tiles[empty_index + self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index + self.size]
        return Board(new_tiles)


# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))


class Search:

    # Utility function to randomly generate 15-puzzle
    def generate_puzzle(self, size):
        numbers = list(range(size * size))
        random.shuffle(numbers)
        return Node(Board(numbers), None, None)

    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        children = []
        actions = ['L', 'R', 'U', 'D']  # left,right, up , down ; actions define direction of movement of empty tile
        for action in actions:
            child_state = parent_node.state.execute_action(action)
            child_node = Node(child_state, parent_node, action)
            children.append(child_node)
        return children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        while (node.parent is not None):
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path

    # Function that checks if a node is a cycle, or if a node has the same formation of tiles as a previous node
    def is_cycle(self, node):
        current_tiles = node.state.tiles
        while node.parent is not None:
            if current_tiles == node.parent.state.tiles:
                return True
            node = node.parent

        return False

    # Function that checks the depth of  node
    def depth(self, node):
        depth = 0
        while node.parent is not None:
            depth += 1
            node = node.parent

        return depth

    # This function runs iterative deepening search from the given root node and returns path, number of nodes expanded and total time taken
    def run_ids(self, root_node):
        depth = 0
        while True:
            result = self.run_dls(root_node, depth)
            if result != "cutoff":
                return result
            depth += 1

    # This function runs depth limited search based on the depth specified
    def run_dls(self, root_node, depth):
        start_time = time.time()
        frontier = deque([root_node])
        result = "failure"
        max_memory = 0
        nodes_expanded = 0

        while len(frontier) > 0:
            max_memory = max(max_memory, sys.getsizeof(frontier))
            cur_node = frontier.popleft()

            if self.goal_test(cur_node.state.tiles):
                path = self.find_path(cur_node)
                end_time = time.time()
                return path, nodes_expanded, (end_time - start_time), max_memory

            if self.depth(cur_node) >= depth:
                result = "cutoff"
            elif not self.is_cycle(cur_node):
                for child in self.get_children(cur_node):
                    nodes_expanded += 1
                    frontier.append(child)

        return result

    # Function to test the goal
    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def solve(self, input):

        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed = self.run_ids(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)


if __name__ == '__main__':
    agent = Search()
    agent.solve("1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12")

"""
Test cases
1 0 3 4 5 2 6 8 9 10 7 11 13 14 15 12 | D R D R D

1 2 3 4 5 6 8 0 9 11 7 12 13 10 14 15 | L D L D R R

1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15 | R D L D D R R

1 2 0 4 6 7 3 8 5 9 10 12 13 14 11 15 | D L L D R R D R

1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12 | R U L L D R D R D
"""
