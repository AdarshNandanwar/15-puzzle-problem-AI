#!/usr/bin/env python3
import time
import numpy
from heapq import * # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************


#                 YOUR CODE SHOULD GO HERE.

#                 WRITE YOUR CODE IN AN EASY TO READ MANNER.

#                 YOU MAY USE SEVERAL CLASSES AND FUNCTIONS 


#                 MODIFY THE BODY OF THE FUNCTION FindMinimumPath()


def get_zero_position(state):
    for position in range(16):
        if state[position] == '0':
            return position
    return -1

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

def heuristic(state):
    return heuristic_manhattan_distance(state)
    # return max(heuristic_manhattan_distance(state), heuristic_misplaced_tiles(state))

def print_state(state):
    print(state[0]+" "+state[1]+" "+state[2]+" "+state[3])
    print(state[4]+" "+state[5]+" "+state[6]+" "+state[7])
    print(state[8]+" "+state[9]+" "+state[10]+" "+state[11])
    print(state[12]+" "+state[13]+" "+state[14]+" "+state[15])


def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    
    ### Your Code for FindMinimumPath function
    ### Write your program in an easy to read manner. You may use several classes and functions.
    ### Your function names should indicate what they are doing
    
    
    # # For heuristic function
    # correct_position = dict()
    # for row in range(4):
    #     for column in range(4):
    #         correct_position[goalState[row][column]] = [row, column]



    initial_state_string = ""
    for row in range(4):
        for column in range(4):
            initial_state_string += str(initialState[row][column])
    goal_state_string = ""
    for row in range(4):
        for column in range(4):
            goal_state_string += str(goalState[row][column])

    # A* Algorithm

    h_value = heuristic(initial_state_string)

    # state_data = { state_string : [minimum_cost, lastmove, zero_position]}
    state_data = dict()
    state_data[initial_state_string] = [h_value, -1, get_zero_position(initial_state_string)]

    # heap element format : [[f(n), g(n)], state]
    #                     : [[path_cost_till_now + heuristic_cost, path_cost_till_now], state]
    heap = []
    heappush(heap, [[0+h_value, 0], initial_state_string])

    direction = [0, -1, 0, 1, 0]

    while len(heap) > 0:

        current_node = heappop(heap)
        current_total_cost = current_node[0][0]
        current_path_cost = current_node[0][1]
        current_state = current_node[1]

        if current_state == goal_state_string:

            # CONSTRUCTION OF THE OPTIMAL PATH

            while current_state != initial_state_string:

                current_state_data = state_data[current_state]

                cur_zero_position = current_state_data[2]
                cur_zero_row = int(cur_zero_position/4)
                cur_zero_column = cur_zero_position%4

                last_move = current_state_data[1]
                if last_move == 0:
                    minPath.append('Down')
                    cur_zero_column += 1
                elif last_move == 1:
                    minPath.append('Left')
                    cur_zero_row += 1
                elif last_move == 2:
                    minPath.append('Up')
                    cur_zero_column -= 1
                elif last_move == 3:
                    minPath.append('Right')
                    cur_zero_row -= 1

                next_zero_position = 4*cur_zero_row+cur_zero_column
                first = min(cur_zero_position, next_zero_position)
                second = max(cur_zero_position, next_zero_position)
                current_state = current_state[:first] + current_state[second] + current_state[first+1:second] + current_state[first] + current_state[second+1:]

            minPath.reverse()
            return minPath, nodesGenerated

        # SKIPPING THE NODES WITH HIGHER COST
        if current_state in state_data and state_data.get(current_state)[0] < current_total_cost:
            continue

        cur_zero_position = state_data[current_state][2]
        cur_zero_row = int(cur_zero_position/4)
        cur_zero_column = cur_zero_position%4

        for move in range(4):

            # next zero coordinates
            next_zero_row = cur_zero_row + direction[move]
            next_zero_column = cur_zero_column + direction[move+1]

            if 0 <= next_zero_row and next_zero_row < 4 and 0 <= next_zero_column and next_zero_column < 4:
                next_zero_position = 4*next_zero_row+next_zero_column

                # next_state is current_state with positions cur_zero_position and next_zero_position swapped

                first = min(cur_zero_position, next_zero_position)
                second = max(cur_zero_position, next_zero_position)
                next_state = current_state[:first] + current_state[second] + current_state[first+1:second] + current_state[first] + current_state[second+1:]

                h_value = heuristic(next_state)

                if next_state not in state_data or (next_state in state_data and state_data.get(next_state)[0] > current_path_cost+1+h_value):
                    nodesGenerated += 1
                    state_data[next_state] = [current_path_cost+1+h_value, move, get_zero_position(next_state)]
                    heappush(heap, [[current_path_cost+1+h_value, current_path_cost+1], next_state])
    

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
