
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    alpha_init, beta_init = arm.getArmAngle()
    alpha_limit, beta_limit = arm.getArmLimit()
    alpha_min, alpha_max = alpha_limit
    beta_min, beta_max = beta_limit
    rows = int((alpha_max-alpha_min)/granularity + 1)
    cols = int((beta_max-beta_min)/granularity + 1)
    alpha = alpha_min
    offset = [alpha_min, beta_min]
    maze_map = [[SPACE_CHAR for y in range(cols)] for x in range(rows)] # list comprehension

    while alpha <= alpha_max:
        beta = beta_min
        while beta <= beta_max:
            arm.setArmAngle((alpha, beta))
            pos = arm.getArmPos()
            pos_dist = arm.getArmPosDist()
            end = pos[1][1]
            idx = angleToIdx([alpha,beta], offset, granularity)
            x = idx[0]
            y = idx[1]

            if (alpha == alpha_init and beta == beta_init) or (isValueInBetween([alpha,alpha+granularity], alpha_init) and isValueInBetween([beta,beta+granularity], beta_init)):
                maze_map[x][y] = START_CHAR
            elif doesArmTipTouchGoals(end, goals):
                maze_map[x][y] = OBJECTIVE_CHAR
            elif not isArmWithinWindow(pos, window):
                maze_map[x][y] = WALL_CHAR
            elif doesArmTouchObjects(pos_dist, goals, isGoal=True) and not doesArmTipTouchGoals(end, goals):
                maze_map[x][y] = WALL_CHAR
            elif doesArmTouchObjects(pos_dist, obstacles, isGoal=False):
                maze_map[x][y] = WALL_CHAR
            else:
                maze_map[x][y] = SPACE_CHAR
            beta += granularity
        alpha += granularity
    
    return Maze(maze_map, offset, granularity)
