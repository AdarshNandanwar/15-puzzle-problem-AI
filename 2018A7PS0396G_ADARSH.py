#!/usr/bin/env python3
import time
import numpy
from heapq import * # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html
import math

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************


#                 YOUR CODE SHOULD GO HERE.

#                 WRITE YOUR CODE IN AN EASY TO READ MANNER.

#                 YOU MAY USE SEVERAL CLASSES AND FUNCTIONS 


#                 MODIFY THE BODY OF THE FUNCTION FindMinimumPath()


# PRINT FUNCTION FOR THE STATE STRING
def print_state(state):
    for i in range(16):
        print(state[i], end = ' ')
        if i%4 == 3: print('')

# HEURISTIC FUNCTION: MISPLACED TILES
def heuristic_misplaced_tiles(state):
    misplaced_tiles = 0
    for i in range(16):
        tile = 0
        if state[i].isdigit():
            tile = int(state[i])
        else:
            tile = ord(state[i])-ord('A')+10
        misplaced_tiles += (tile != i)
    return misplaced_tiles

# HEURISTIC FUNCTION: EUCLIDEAN DISTANCE
def heuristic_euclidean_distance(state):
    euclidean_distance = 0.0
    for i in range(16):
        tile = 0
        if state[i].isdigit():
            tile = int(state[i])
            if tile == 0:
                continue
        else:
            tile = ord(state[i])-ord('A')+10
        cur_row = int(i/4)
        cur_column = i%4
        goal_row = int(tile/4)
        goal_column = tile%4
        euclidean_distance += math.sqrt(pow(goal_row-cur_row, 2)+pow(goal_column-cur_column, 2))
    return euclidean_distance

# HEURISTIC FUNCTION: MISPLACED ROW/COLUMN
def heuristic_misplaced_row_column(state):
    misplaced_row_column = 0
    for i in range(16):
        tile = 0
        if state[i].isdigit():
            tile = int(state[i])
            if tile == 0:
                continue
        else:
            tile = ord(state[i])-ord('A')+10
        cur_row = int(i/4)
        cur_column = i%4
        goal_row = int(tile/4)
        goal_column = tile%4
        misplaced_row_column += ((cur_row != goal_row) + (cur_column != goal_column))
    return misplaced_row_column

# HEURISTIC FUNCTION: MANHATTEN DISTANCE
def heuristic_manhattan_distance(state):
    manhatten_distance = 0
    for i in range(16):
        tile = 0
        if state[i].isdigit():
            tile = int(state[i])
            if tile == 0:
                continue
        else:
            tile = ord(state[i])-ord('A')+10
        cur_row = int(i/4)
        cur_column = i%4
        goal_row = int(tile/4)
        goal_column = tile%4
        manhatten_distance += (abs(goal_row-cur_row)+abs(goal_column-cur_column))
    return manhatten_distance

# HEURISTIC FUNCTION THAT IS CALLED FROM A* ALGORITHM
def heuristic(state):
    return heuristic_manhattan_distance(state)
    # return heuristic_euclidean_distance(state)
    # return heuristic_misplaced_tiles(state)
    # return heuristic_misplaced_row_column(state)
    # return max(heuristic_manhattan_distance(state), heuristic_misplaced_tiles(state))

# FUNCTION TO GET THE INDEX OF 0 IN THE STATE STRING
def get_zero_position(state):
    for position in range(16):
        if state[position] == '0':
            return position
    return -1

def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    
    ### Your Code for FindMinimumPath function
    ### Write your program in an easy to read manner. You may use several classes and functions.
    ### Your function names should indicate what they are doing
        
    # direction[0:4] = {down, left, up, right}
    direction = [0, -1, 0, 1, 0]

    # CONVERTING THE INITIAL AND GOAL STATES IN A FLATTENED STRING FORMAT

    initial_state_string = ""
    for row in range(4):
        for column in range(4):
            initial_state_string += str(initialState[row][column])
    goal_state_string = ""
    for row in range(4):
        for column in range(4):
            goal_state_string += str(goalState[row][column])

    # A* ALGORITHM

    minimum_cost_list = dict()
    minimum_cost_list[initial_state_string] = heuristic(initial_state_string)
    last_move = dict()

    # format for heap element : 
    # [[f(n), g(n)], state]
    # [[path_cost_till_now + heuristic_cost, path_cost_till_now], state]
    
    heap = []
    heappush(heap, [[0+heuristic(initial_state_string), 0], initial_state_string])

    while len(heap) > 0:

        current_cost_and_state = heappop(heap)
        current_total_cost = current_cost_and_state[0][0]
        current_path_cost = current_cost_and_state[0][1]
        current_state = current_cost_and_state[1]

        if current_state == goal_state_string:
            # OPTIMAL PATH TO THE GOAL STATE FOUND
            # CONSTRUCTING THE OPTIMAL PATH
            while current_state != initial_state_string:

                minPath.append(last_move[current_state])

                cur_zero_position = get_zero_position(current_state)
                cur_zero_row = int(cur_zero_position/4)
                cur_zero_column = cur_zero_position%4

                move_direction = []
                if last_move[current_state] == 'Down':
                    move_direction = [0, -1]
                elif last_move[current_state] == 'Left':
                    move_direction = [-1, 0]
                elif last_move[current_state] == 'Up':
                    move_direction = [0, 1]
                elif last_move[current_state] == 'Right':
                    move_direction = [1, 0]

                # GETTING PARENT OF THE CURRENT STATE
                next_zero_row = cur_zero_row - move_direction[0]
                next_zero_column = cur_zero_column - move_direction[1]
                next_zero_position = 4*next_zero_row+next_zero_column
                first = min(cur_zero_position, next_zero_position)
                second = max(cur_zero_position, next_zero_position)
                current_state = current_state[:first] + current_state[second] + current_state[first+1:second] + current_state[first] + current_state[second+1:]

            minPath.reverse()
            return minPath, nodesGenerated

        # IGNORING INEFFICIENT PATHS
        if current_state in minimum_cost_list and minimum_cost_list.get(current_state) < current_total_cost:
            continue

        # POSITION OF ZERO IN CURRENT STATE
        cur_zero_position = get_zero_position(current_state)
        cur_zero_row = int(cur_zero_position/4)
        cur_zero_column = cur_zero_position%4

        for move in range(4):
            # POSITION OF 0 IN THE NEXT STATE
            next_zero_row = cur_zero_row + direction[move]
            next_zero_column = cur_zero_column + direction[move+1]

            if 0 <= next_zero_row and next_zero_row < 4 and 0 <= next_zero_column and next_zero_column < 4:
                next_zero_position = 4*next_zero_row+next_zero_column

                # next state is current_state with positions cur_zero_position and next_zero_position swapped

                first = min(cur_zero_position, next_zero_position)
                second = max(cur_zero_position, next_zero_position)
                next_state = current_state[:first] + current_state[second] + current_state[first+1:second] + current_state[first] + current_state[second+1:]

                if next_state not in minimum_cost_list or (next_state in minimum_cost_list and minimum_cost_list.get(next_state) > current_path_cost+1+heuristic(next_state)):
                    nodesGenerated += 1
                    minimum_cost_list[next_state] = current_path_cost+1+heuristic(next_state)
                    if move == 0:
                        last_move[next_state] = 'Down'
                    elif move == 1:
                        last_move[next_state] = 'Left'
                    elif move == 2:
                        last_move[next_state] = 'Up'
                    elif move == 3:
                        last_move[next_state] = 'Right'
                    heappush(heap, [[minimum_cost_list[next_state], current_path_cost+1], next_state])
    
    ### Your Code ends here. minPath is a list that contains actions.
    ### For example, minPath = ['Up','Right','Down','Down','Left']
    
    return minPath, nodesGenerated



#**************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
    with open("initial_state4.txt", "r") as file: #IMP: If you change the file name, then there will be an error when
                                                        #               evaluators test your program. You will lose 2 marks.
        initialState = [[x for x in line.split()] for i,line in enumerate(file) if i<4]
    return initialState

def ShowState(state,heading=''):
    print(heading)
    for row in state:
        print(*row, sep = " ")

def main():
    initialState = ReadInitialState()
    ShowState(initialState,'Initial state:')
    goalState = [['0','1','2','3'],['4','5','6','7'],['8','9','A','B'],['C','D','E','F']]
    ShowState(goalState,'Goal state:')
    
    start = time.time()
    minimumPath, nodesGenerated = FindMinimumPath(initialState,goalState)
    timeTaken = time.time() - start
    
    if len(minimumPath)==0:
        minimumPath = ['Up','Right','Down','Down','Left']
        print('Example output:')
    else:
        print('Output:')

    print('   Minimum path cost : {0}'.format(len(minimumPath)))
    print('   Actions in minimum path : {0}'.format(minimumPath))
    print('   Nodes generated : {0}'.format(nodesGenerated))
    print('   Time taken : {0} s'.format(round(timeTaken,4)))

if __name__=='__main__':
    main()
