# Implementation of Maze Solving Algorithms (Tree Traversals)

import sys

# Class Node will keep track of state, parent node, and action
# Path cost is not kept track of, because we can calculate that at the end (after finding solution)
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# Class StackFrontier (Uses 'stacking' last in first out method. (Depth-First-Search))
class StackFrontier():

    # Initially creating a frontier represented by an empty list (as of now...)
    def __init__(self):
        self.frontier = []
    
    # Function for adding a node to the END of the list
    def add(self, node):
        self.frontier.append(node)

    # Funtion to check if the frontier contains a particular state
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    # Empty function that checks if the frontier is empty
    def empty(self):

        # Length of the frontier is 0 when frontier is empty
        return len(self.frontier) == 0
    
    # Function for removing from the frontier
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:

            # Removing last item from a list ('stack')
            # Index '-1' refers to the last item in a list
            node = self.frontier[-1]

            # We update the frontier list by now including everything up until (but not including) the last node
            self.frontier = self.frontier[:-1]
            return node
        
# Class QueueFrontier inherits Class StackFrontier
# Only the functions we explicitly define again will differ from StackFrontier
# Utilizes 'queue' first in first out method (Breadth First Search)
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
       
        else:

            # In this case, we are removing the first node
            # And replacing the frontier with the list excluding the first node and starting from the second node all the way to the end of the list
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
# Class Maze handles the actual workings of a maze. Represented by a text file.
class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")
        
        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(self.walls):
                if col:
                    print("BOX", end="")
                elif (i, j) == self.start:
                    print("A", end = "")
                elif (i ,j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state

        # All possible actions
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col-1)),
            ("right", (row, col+1))
        ]

        # Ensure actions are valid
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result
    

    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        # This node represents the start state
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()

        # Initially this frontier only contains the start state
        frontier.add(start)

        # Initialize an empty explored set (because we are just starting so we haven't explored anything yet :)
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If onthing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            
            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:

                # Now I want to backtrack my way, to see which path I took to get to the goal
                # Every Node stores its parent and the action done to get to the current node
                actions = []
                cells = []

                # Follow parent nodes to find solution
                # Initial state has no parent, therefore, this loop will repeat 
                # until all the steps have been bakctracked all the way to the very first parent node. (Initial State)
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                # It is very important we reverse all the info and actions because we want to present the solution as going from 
                # the initial state to the goal. NOT the other way around.
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # All of those above code only happens if that current state was the goal.
            # If not, we mark the node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            # The logic here is that we add all the neighbors to our frontier to check. 
            # We must make sure that this 'neighbor' is not a node we already checked before
            # That is why we make sure that state is NOT IN self.explored
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)