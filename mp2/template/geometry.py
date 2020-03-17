# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
#import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position (int,int):of the arm link, (x-coordinate, y-coordinate)
    """
    # opposite = sin(angle)*hypot
    # adjacent = cos(angle)*hypot
    rad = math.radians(angle)
    opp = int(math.sin(rad) * length)
    adj = int(math.cos(rad) * length)
    x, y = start 
    ret = (x + adj, y - opp) # subtract for y b/c (0,0) is top left
    return ret 

# Sources: 
    # http://mathworld.wolfram.com/Circle-LineIntersection.html -- from Piazza
    # https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py -- from Google search
    
def determ(x_start, x_end, y_start, y_end, x_circle, y_circle, dx, dy, dr, determinant, discriminant):
    if discriminant < 0:
        return False
    
    inter = [
        (x_circle + (determinant * dy + sgn * (-1 if dy < 0 else 1) * dx * math.sqrt(discriminant)) / dr**2,
         y_circle + (-1 * determinant * dx + sgn * abs(dy) * math.sqrt(discriminant)) / dr**2) 
         for sgn in ((1, -1) if dy < 0 else (-1, 1))
    ]

    vector = (x_end - x_start, y_end - y_start)
    x_line, y_line = vector
    x_int1 = inter[0][0] - x_start
    x_int2 = inter[1][0] - x_start
    y_int1 = inter[0][1] - y_start
    y_int2 = inter[1][1] - y_start

    if x_line != 0 and y_line != 0:
        if (0 <= x_int1/x_line <= 1 and 0 <= y_int1/y_line <= 1) or (0 <= x_int2/x_line <= 1 and 0 <= y_int2/y_line <= 1):
            return True
        else:
            return False
    elif x_line == 0 and y_line != 0:
        if (x_int1 == 0 and 0 <= y_int1/y_line <= 1) or (x_int2 == 0 and 0 <= y_int2/y_line <= 1):
            return True
        else:
            return False
    elif x_line != 0 and y_line == 0:
        if (0 <= x_int1/x_line <= 1 and y_int1 == 0) or (0 <= x_int2/x_line <= 1 and y_int2 == 0):
            return True
        else:
            return False
    elif x_line == 0 and y_line == 0:
        if (x_int1 == 0 and y_int1 == 0) or (x_int2 == 0 and y_int2 == 0):
            return True
        else:
            return False

def lci(x_start, x_end, y_start, y_end, padding, x_circle, y_circle, rad):
    (x1, y1) = (x_start - x_circle, y_start - y_circle)
    (x2, y2) = (x_end - x_circle, y_end- y_circle)
    dx = x2 - x1
    dy = y2 - y1
    dr = math.sqrt(dx**2 + dy**2)
    det = x1 * y2 - x2 * y1
    disc = (rad**2) * (dr**2) - det**2
    no_pad = determ(x_start, x_end, y_start, y_end, x_circle, y_circle, dx, dy, dr, det, disc)
    rad1 = rad + padding
    rad2 = rad - padding 
    disc1 = (rad1**2) * (dr**2) - det**2
    disc2 = (rad2**2) * (dr**2) - det**2
    pad = determ(x_start, x_end, y_start, y_end, x_circle, y_circle, dx, dy, dr, det, disc1) or determ(x_start, x_end, y_start, y_end, x_circle, y_circle, dx, dy, dr, det, disc2)
    return no_pad or pad 

def doesArmTouchObjects(armPosDist, objects, isGoal=False):
    """Determine whether the given arm links touch any obstacle or goal

        Args:
            armPosDist (list): start and end position and padding distance of all arm links [(start, end, distance)]
            objects (list): x-, y- coordinate and radius of object (obstacles or goals) [(x, y, r)]
            isGoal (bool): True if the object is a goal and False if the object is an obstacle.
                           When the object is an obstacle, consider padding distance.
                           When the object is a goal, no need to consider padding distance.
        Return:
            True if touched. False if not.
    """
    for pos in armPosDist:
        start, end, pad = pos 
        x_start, y_start = start 
        x_end, y_end = end 
        for obj in objects:
            obj_x, obj_y, obj_r = obj 
            dist1 = math.sqrt((x_start - obj_x)**2 + (y_start - obj_y)**2)
            dist2 = math.sqrt((x_end - obj_x)**2 + (y_end - obj_y)**2)
            if dist1 <= obj_r or dist2 <= obj_r:
                return True
            else:
                pad_var = 0
                if not isGoal:
                    pad_var = pad
                return lci(x_start, x_end, y_start, y_end, pad_var, obj_x, obj_y, obj_r)

def doesArmTipTouchGoals(armEnd, goals):
    """Determine whether the given arm tip touch goals

        Args:
            armEnd (tuple): the arm tip position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]. There can be more than one goal.
        Return:
            True if arm tick touches any goal. False if not.
    """
    arm_x, arm_y = armEnd
    for g in goals:
        x, y, r = g
        x_dist = arm_x - x
        y_dist = arm_y - y 
        dist = math.sqrt(x_dist**2 + y_dist**2)
        if dist <= r:
            return True

    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end positions of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False if not.
    """
    w, h = window 
    for arm in armPos:
        arm_start_x, arm_start_y = arm[0]
        arm_end_x, arm_end_y = arm[1]
        if arm_start_x < 0 or arm_start_x > w or arm_end_x < 0 or arm_end_x > w or arm_start_y < 0 or arm_start_y > h or arm_end_y < 0 or arm_end_y > h:
            return False
    return True


if __name__ == '__main__':
    computeCoordinateParameters = [((150, 190),100,20), ((150, 190),100,40), ((150, 190),100,60), ((150, 190),100,160)]
    resultComputeCoordinate = [(243, 156), (226, 126), (200, 104), (57, 156)]
    testRestuls = [computeCoordinate(start, length, angle) for start, length, angle in computeCoordinateParameters]
    assert testRestuls == resultComputeCoordinate

    testArmPosDists = [((100,100), (135, 110), 4), ((135, 110), (150, 150), 5)]
    testObstacles = [[(120, 100, 5)], [(110, 110, 20)], [(160, 160, 5)], [(130, 105, 10)]]
    resultDoesArmTouchObjects = [
        True, True, False, True, False, True, False, True,
        False, True, False, True, False, False, False, True
    ]

    testResults = []
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle))

    print("\n")
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))

    assert resultDoesArmTouchObjects == testResults

    testArmEnds = [(100, 100), (95, 95), (90, 90)]
    testGoal = [(100, 100, 10)]
    resultDoesArmTouchGoals = [True, True, False]

    testResults = [doesArmTipTouchGoals(testArmEnd, testGoal) for testArmEnd in testArmEnds]
    assert resultDoesArmTouchGoals == testResults

    testArmPoss = [((100,100), (135, 110)), ((135, 110), (150, 150))]
    testWindows = [(160, 130), (130, 170), (200, 200)]
    resultIsArmWithinWindow = [True, False, True, False, False, True]
    testResults = []
    for testArmPos in testArmPoss:
        for testWindow in testWindows:
            testResults.append(isArmWithinWindow([testArmPos], testWindow))
    assert resultIsArmWithinWindow == testResults

    print("Test passed\n")
