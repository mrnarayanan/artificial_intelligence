# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)

import queue

class Node:
    def __init__(self, row, col, g):
        self.row = row
        self.col = col
        self.total_cost = 0
        self.h = 0 # heuristic
        self.g = g
        self.visited = []
        self.not_visited = []
    def __lt__(self, other):
        return self.total_cost < other.total_cost
    def __eq__(self, other):
        return self.total_cost == other.total_cost
    def __gt__(self, other):
        return self.total_cost > other.total_cost

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    frontier = queue.Queue()
    dots = maze.getObjectives()
    start = maze.getStart()
    visited = set()
    frontier.put([start])
    while not frontier.empty():
        current_path = frontier.get()
        row, col = current_path[-1]
        if (row,col) in visited:
            continue
        visited.add((row,col))
        if (row,col) in dots:
            return current_path
        for point in maze.getNeighbors(row,col):
            if point not in visited:
                frontier.put(current_path + [point])
    return []

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    end = maze.getObjectives()[0]
    frontier = queue.PriorityQueue()
    visited = {}
    srow, scol = start
    erow, ecol = end
    cost = abs(srow - erow) + abs(scol - ecol)
    frontier.put((cost, [(srow, scol)]))
    while not frontier.empty():
        current_path = frontier.get()[1]
        row, col = current_path[-1]
        if (row, col) in visited:
            continue
        current_cost = abs(row - erow) + abs(col - ecol) + len(current_path) - 1
        visited[(row, col)] = current_cost
        if (row, col) == (erow, ecol):
            return current_path
        for point in maze.getNeighbors(row, col):
            new_cost = abs(point[0] - erow) + abs(point[1] - ecol) + len(current_path) - 1
            if point not in visited:
                frontier.put((new_cost, current_path + [point]))
            else:
                if visited[point] > new_cost:
                    visited[point] = new_cost
                    frontier.put((new_cost, current_path + [point]))
    return []

def mst(dist, not_visited):
    weight = 0
    if len(not_visited) == 0:
        return 0
    visited = [not_visited[0]]
    while len(visited) < len(not_visited):
        mini = -1
        pos = (0, 0)
        for p1 in visited:
            for p2 in not_visited:
                if p2 not in visited:
                    temp = dist[(p1, p2)] -2
                    if mini == -1 or mini > temp:
                        mini = temp
                        pos = p2
        weight += mini 
        visited.append(pos)
    return weight

def astar_helper(maze, start, end):
    frontier = queue.PriorityQueue()
    visited = {}
    srow, scol = start
    erow, ecol = end
    cost = abs(srow - erow) + abs(scol - ecol)
    frontier.put((cost, [(srow, scol)]))
    while not frontier.empty():
        current_path = frontier.get()[1]
        row, col = current_path[-1]
        if (row, col) in visited:
            continue
        current_cost = abs(row - erow) + abs(col - ecol) + len(current_path) - 1
        visited[(row, col)] = current_cost
        if (row, col) == (erow, ecol):
            return current_path
        for point in maze.getNeighbors(row, col):
            new_cost = abs(point[0] - erow) + abs(point[1] - ecol) + len(current_path) - 1
            if point not in visited:
                frontier.put((new_cost, current_path + [point]))
            else:
                if visited[point] > new_cost:
                    visited[point] = new_cost
                    frontier.put((new_cost, current_path + [point]))
    return []

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.
        
    @param maze: The maze to execute the search on.
        
    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    dots = maze.getObjectives()
    start = maze.getStart()
    dots.insert(0, start)
    srow, scol = start 
    path = {}
    dist = {}
    visited = []
    frontier = queue.PriorityQueue()
    if len(dots) == 0:
        return []
    if len(dots) == 1:
        return astar_helper(maze, start, dots[0])
    for x in range(len(dots)):
        y = x + 1
        while y < len(dots):
            path[(dots[x], dots[y])] = astar_helper(maze, dots[x], dots[y])
            path[(dots[y], dots[x])] = path[(dots[x], dots[y])][::-1] # reverse list
            dist[(dots[x], dots[y])] = len(path[(dots[x], dots[y])])
            dist[(dots[y], dots[x])] = len(path[(dots[x], dots[y])])
            y += 1
    start_node = Node(srow, scol, 0)
    start_node.not_visited = dots.copy()
    start_node.not_visited.pop(0)
    start_node.visited.append((srow, scol))
    frontier.put(start_node)
    end_node = Node(0, 0, 0)
    while frontier.qsize() > 0:
        current_node = frontier.get()
        if len(current_node.not_visited) == 0:
            end_node = current_node
            break
        for i, n in enumerate(current_node.not_visited):
            nrow, ncol = n
            next_node = Node(nrow, ncol, 0)
            next_node.not_visited = current_node.not_visited.copy()
            next_node.visited = current_node.visited.copy()
            next_node.not_visited.remove(n)
            next_node.visited.append((nrow, ncol))
            next_node.h = mst(dist, next_node.not_visited)
            next_node.g = current_node.g + dist[((current_node.row, current_node.col), n)] - 1
            next_node.total_cost = next_node.g + next_node.h + len(next_node.not_visited)
            frontier.put(next_node)
    ret = [start]
    for i in range(len(end_node.visited) - 1):
        temp = path[(end_node.visited[i], end_node.visited[i+1])].copy()
        temp.pop(0)
        ret += temp
    return ret 

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    dots = maze.getObjectives()
    start = maze.getStart()
    dots.insert(0, start)
    srow, scol = start 
    path = {}
    dist = {}
    visited = []
    frontier = queue.PriorityQueue()
    if len(dots) == 0:
        return []
    if len(dots) == 1:
        return astar_helper(maze, start, dots[0])
    for x in range(len(dots)):
        y = x + 1
        while y < len(dots):
            path[(dots[x], dots[y])] = astar_helper(maze, dots[x], dots[y])
            path[(dots[y], dots[x])] = path[(dots[x], dots[y])][::-1] # reverse list
            dist[(dots[x], dots[y])] = len(path[(dots[x], dots[y])])
            dist[(dots[y], dots[x])] = len(path[(dots[x], dots[y])])
            y += 1
    start_node = Node(srow, scol, 0)
    start_node.not_visited = dots.copy()
    start_node.not_visited.pop(0)
    start_node.visited.append((srow, scol))
    frontier.put(start_node)
    end_node = Node(0, 0, 0)
    while frontier.qsize() > 0:
        current_node = frontier.get()
        if len(current_node.not_visited) == 0:
            end_node = current_node
            break
        for i, n in enumerate(current_node.not_visited):
            nrow, ncol = n
            next_node = Node(nrow, ncol, 0)
            next_node.not_visited = current_node.not_visited.copy()
            next_node.visited = current_node.visited.copy()
            next_node.not_visited.remove(n)
            next_node.visited.append((nrow, ncol))
            next_node.h = mst(dist, next_node.not_visited)
            next_node.g = current_node.g + dist[((current_node.row, current_node.col), n)] - 1
            next_node.total_cost = next_node.g + next_node.h + len(next_node.not_visited)
            frontier.put(next_node)
    ret = [start]
    for i in range(len(end_node.visited) - 1):
        temp = path[(end_node.visited[i], end_node.visited[i+1])].copy()
        temp.pop(0)
        ret += temp
    return ret 

def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
