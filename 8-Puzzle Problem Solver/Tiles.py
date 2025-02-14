"""
-----------------------
8-Puzzle Problem Solver
-----------------------
This program solves the 8-puzzle problem using different search algorithms, such as:
- Breadth-First Search (BFS)
- Iterative Deepening Depth-First Search (IDDFS)
- Greedy Best-First Search (GBFS)
- A* Search

The program:
1. Takes the initial state as input.
2. Validates if the puzzle is solvable.
3. Runs all algorithms to solve the puzzle.
4. Prints the path to the solution, the number of nodes explored.

Dependencies:
- sys (for command-line arguments)
- heapq (for priority queue in GBFS and A*)
- collections (for deque in BFS)

Usage:
Run the script with the initial state as command-line arguments:
    python Tieles.py "1 2 3 4 5 6 7 8 0"
"""

import sys
import heapq
from collections import deque


class Node:
    """
    Represents a single node in the search tree.

    Attributes:
        state (list): The current state of the puzzle (as a 3x3 matrix).
        parent (Node): The parent node in the tree.
        action (str): The action taken to reach this node (e.g., 'UP', 'DOWN').
        path_cost (int): The cost of the path from the root to this node.
        depth (int): The depth of this node in the search tree.
    """

    def __init__(self, state, parent=None, action=None, path_cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth

    def path(self):
        """
        Generates the path from the root to the current node.

        Returns:
            list: A list of (state, action) pairs.
        """
        node, path_back = self, []
        while node:
            path_back.append((node.state, node.action))
            node = node.parent
        return list(reversed(path_back))

    def __lt__(self, other):
        """
        Comparator for priority queue (used in heapq).
        Nodes are compared based on their path cost.
        """
        return self.path_cost < other.path_cost


class EightPuzzleProblem:
    """
    Represents the 8-puzzle problem.

    Attributes:
        initial (list): The initial state of the puzzle.
        goal (list): The goal state of the puzzle.

    Methods:
        actions(state): Returns the possible actions from a given state.
        result(state, action): Returns the new state after applying an action.
        action_cost(s, action, s_prime): Returns the cost of an action.
        expand(node): Expands a node and returns child nodes.
        is_goal(state): Checks if a given state is the goal state.
        heuristic_out_of_row_and_column(state): Calculates heuristic value.
    """

    def __init__(self, initial, goal="0 1 2 3 4 5 6 7 8"):
        self.initial = self.to_matrix(initial)
        self.goal = self.to_matrix(goal)

    def to_matrix(self, state_str):
        """
        Converts a string representing the state of the puzzle into a 3x3 matrix (list of lists).

        Args:
            state_str (str): The state as a space-separated string.

        Returns:
            list: A 3x3 matrix representing the state.
        """
        state_list = state_str.split()
        return [state_list[i:i + 3] for i in range(0, 9, 3)]

    def to_string(self, matrix):
        """
        Converts the 3x3 matrix back to a string.

        Args:
            matrix (list): The state as a 3x3 matrix.

        Returns:
            str: The state as a space-separated string.
        """
        return ' '.join(sum(matrix, []))

    def actions(self, state):
        """
        Returns a list of possible actions (UP, DOWN, LEFT, RIGHT) for the current state.
        The '0' represents the empty space.

        Args:
            state (list): The current state as a 3x3 matrix.

        Returns:
            list: A list of possible actions.
        """
        row, col = [(i, row.index("0")) for i, row in enumerate(state) if "0" in row][0]
        possible_actions = []
        if col > 0:
            possible_actions.append("LEFT")
        if col < 2:
            possible_actions.append("RIGHT")
        if row > 0:
            possible_actions.append("UP")
        if row < 2:
            possible_actions.append("DOWN")
        return possible_actions

    def result(self, state, action):
        """
        Returns the new state after applying an action to the current state.

        Args:
            state (list): The current state as a 3x3 matrix.
            action (str): The action to apply ('UP', 'DOWN', 'LEFT', 'RIGHT').

        Returns:
            list: The new state as a 3x3 matrix.
        """
        row, col = [(i, row.index("0")) for i, row in enumerate(state) if "0" in row][0]
        new_state = [r[:] for r in state]
        if action == "UP":
            new_row, new_col = row - 1, col
        elif action == "DOWN":
            new_row, new_col = row + 1, col
        elif action == "LEFT":
            new_row, new_col = row, col - 1
        elif action == "RIGHT":
            new_row, new_col = row, col + 1
        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
        return new_state

    def action_cost(self, s, action, s_prime):
        """
        Returns the cost of an action. For the 8-puzzle, the cost is always 1.

        Args:
            s (list): Current state.
            action (str): Action taken.
            s_prime (list): New state after applying the action.

        Returns:
            int: Cost of the action.
        """
        return 1

    def expand(self, node):
        """
        Expands the current node and generates all possible child nodes.

        Args:
            node (Node): The current node.

        Yields:
            Node: The child nodes.
        """
        s = node.state
        for action in self.actions(s):
            s_prime = self.result(s, action)
            cost = node.path_cost + self.action_cost(s, action, s_prime)
            yield Node(state=s_prime, parent=node, action=action, path_cost=cost, depth=node.depth + 1)

    def is_goal(self, state):
        """
        Checks if the current state is the goal state.

        Args:
            state (list): The state to check.

        Returns:
            bool: True if the state is the goal state, False otherwise.
        """
        return state == self.goal

    def heuristic_out_of_row_and_column(self, state):
        """
        Heuristic: Counts how many tiles are out of their correct row or column.

        Args:
            state (list): The current state as a 3x3 matrix.

        Returns:
            int: The heuristic value.
        """
        out_of_row = 0
        out_of_column = 0
        for row in range(3):
            for col in range(3):
                tile = state[row][col]
                if tile != '0':
                    goal_row, goal_col = [(i, r.index(tile)) for i, r in enumerate(self.goal) if tile in r][0]
                    if row != goal_row:
                        out_of_row += 1
                    if col != goal_col:
                        out_of_column += 1
        return out_of_row + out_of_column




#_____________________________________________________________________________________
# The following search algorithms implement different methods for solving the 8-puzzle
#_____________________________________________________________________________________
def breadth_first_search(problem):
    """
    Performs breadth-first search (BFS) to find the solution.

    Args:
        problem (EightPuzzleProblem): The 8-puzzle problem instance.

    Returns:
        tuple: A tuple containing the path to the solution and the number of nodes explored.
    """
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node.path(), 0

    frontier = deque([node])  # FIFO queue for BFS
    reached = {problem.to_string(node.state)}
    explored_nodes = 0

    while frontier:
        node = frontier.popleft()  # Explore the node at the front of the queue
        explored_nodes += 1
        for child in problem.expand(node):
            child_state_str = problem.to_string(child.state)
            if problem.is_goal(child.state):
                return child.path(), explored_nodes
            if child_state_str not in reached:
                reached.add(child_state_str)
                frontier.append(child)
    return "failure", explored_nodes


def iterative_deepening_search(problem):
    """
    Performs iterative deepening depth-first search (IDDFS) to find the solution.

    Args:
        problem (EightPuzzleProblem): The 8-puzzle problem instance.

    Returns:
        tuple: A tuple containing the path to the solution and the number of nodes explored.
    """
    def depth_limited_search(node, depth_limit):
        """
        Helper function for depth-limited search.

        Args:
            node (Node): The current node.
            depth_limit (int): The maximum depth to explore.

        Returns:
            tuple: A tuple containing the result ("cutoff", "failure", or path) and the number of nodes explored.
        """
        if problem.is_goal(node.state):
            return node.path(), 0
        if node.depth >= depth_limit:
            return "cutoff", 1

        explored_nodes = 1
        cutoff_occurred = False

        for child in problem.expand(node):
            if not is_cycle(child):  # Avoid cycles in the search tree
                result, nodes = depth_limited_search(child, depth_limit)
                explored_nodes += nodes
                if result == "cutoff":
                    cutoff_occurred = True
                elif result != "failure":
                    return result, explored_nodes

        return ("cutoff" if cutoff_occurred else "failure"), explored_nodes

    depth = 0
    while True:
        result, explored_nodes = depth_limited_search(Node(problem.initial), depth)
        if result != "cutoff":
            return result, explored_nodes
        depth += 1


def greedy_best_first_search(problem, heuristic):
    """
    Performs greedy best-first search (GBFS) using a given heuristic.

    Args:
        problem (EightPuzzleProblem): The 8-puzzle problem instance.
        heuristic (function): The heuristic function to estimate the cost.

    Returns:
        tuple: A tuple containing the path to the solution and the number of nodes explored.
    """
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node.path(), 0

    frontier = []
    heapq.heappush(frontier, (heuristic(node.state), node))  # Priority queue sorted by heuristic
    reached = {problem.to_string(node.state)}
    explored_nodes = 0

    while frontier:
        _, node = heapq.heappop(frontier)  # Get the node with the lowest heuristic value
        explored_nodes += 1
        if problem.is_goal(node.state):
            return node.path(), explored_nodes
        for child in problem.expand(node):
            child_state_str = problem.to_string(child.state)
            if child_state_str not in reached:
                reached.add(child_state_str)
                heapq.heappush(frontier, (heuristic(child.state), child))
    return "failure", explored_nodes


def a_star_search(problem, heuristic):
    """
    Performs A* search using a given heuristic.

    Args:
        problem (EightPuzzleProblem): The 8-puzzle problem instance.
        heuristic (function): The heuristic function to estimate the cost.

    Returns:
        tuple: A tuple containing the path to the solution and the number of nodes explored.
    """
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node.path(), 0

    frontier = []
    heapq.heappush(frontier, (heuristic(node.state) + node.path_cost, node))  # Priority queue sorted by f(n) = g(n) + h(n)
    reached = {problem.to_string(node.state): node.path_cost}
    explored_nodes = 0

    while frontier:
        _, node = heapq.heappop(frontier)
        explored_nodes += 1
        if problem.is_goal(node.state):
            return node.path(), explored_nodes
        for child in problem.expand(node):
            f_cost = child.path_cost + heuristic(child.state)
            child_state_str = problem.to_string(child.state)
            if child_state_str not in reached or f_cost < reached[child_state_str]:
                reached[child_state_str] = f_cost
                heapq.heappush(frontier, (f_cost, child))
    return "failure", explored_nodes


def run_all_algorithms(problem):
    """
    Runs all search algorithms on the given problem and prints the results.

    Args:
        problem (EightPuzzleProblem): The 8-puzzle problem instance.
    """
    algorithms = [
        ("BFS", breadth_first_search),
        ("IDDFS", iterative_deepening_search),
        ("GBFS", lambda prob: greedy_best_first_search(prob, prob.heuristic_out_of_row_and_column)),
        ("A*", lambda prob: a_star_search(prob, prob.heuristic_out_of_row_and_column)),
    ]

    for name, func in algorithms:
        path, nodes_explored = func(problem)
        print(f"\nAlgorithm: {name}")
        print(f"Nodes explored: {nodes_explored}")

        if path != "failure":
            move_sequence = []
            previous_state = None

            for state, action in path:
                if previous_state is not None:
                    moved_tile = None
                    for r in range(3):
                        for c in range(3):
                            if state[r][c] != previous_state[r][c] and state[r][c] != '0':
                                moved_tile = state[r][c]
                                break
                        if moved_tile:
                            break
                    if moved_tile:
                        move_sequence.append(str(moved_tile))

                previous_state = state

            print(f"Path to solution: {' -> '.join(move_sequence)}")
        else:
            print("Solution not found.")


def is_cycle(node):
    """
    Checks if the current node is part of a cycle in the search tree.

    Args:
        node (Node): The current node.

    Returns:
        bool: True if a cycle is detected, False otherwise.
    """
    current_state = node.state
    parent = node.parent
    while parent is not None:
        if parent.state == current_state:
            return True
        parent = parent.parent
    return False


def is_solvable(state):
    """
    Checks if a given puzzle state is solvable based on the number of inversions.

    Args:
        state (str): The state as a space-separated string.

    Returns:
        bool: True if the puzzle is solvable, False otherwise.
    """
    state = [int(x) for x in state.split() if x != '0']
    inversions = sum(1 for i in range(len(state)) for j in range(i + 1, len(state)) if state[i] > state[j])
    return inversions % 2 == 0


if __name__ == "__main__":
    initial_state = ' '.join(sys.argv[1:])
    if len(initial_state.split()) != 9 or not all(x.isdigit() for x in initial_state.split()):
        print("Invalid input. Please enter 9 digits separated by spaces.")
        sys.exit(1)

    if not is_solvable(initial_state):
        print("No solution exists for the given initial state.")
        sys.exit(1)

    problem = EightPuzzleProblem(initial_state)
    run_all_algorithms(problem)
