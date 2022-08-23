#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Code by: Nidhi Vraj Sadhuvala, Aditi Soni, Srinivas Vaddi, Username - nsadhuva-adisoni-svaddi
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#


import sys
import numpy as np
import heapq as hq
import math

ROWS=5
COLS=5



def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


def get_2dArray(state):  #convert to 2d array
    data = np.array(state)
    new_state=data.reshape([5,5])
    return new_state


# move - all row successors right & left
def move1_successors(state):
    horizontal_succ={}
    #move row elements to the right by one tile
    for r in range(0, ROWS):
        new_state=get_2dArray(state)
        state= get_2dArray(state)
        for c in range (0, COLS):
            if c==0:
                new_state[r][0]=state[r][COLS-1]
            else:
                new_state[r][c]=state[r][c-1]
        
        new_state_1 = new_state.ravel()
        horizontal_succ["R"+str((r+1))+","]=new_state_1
    #move row elements to the left by one tile
    for r in range(0, ROWS):
        new_state=get_2dArray(state)
        state= get_2dArray(state)
        for c in range (0, COLS):
            if c==COLS-1:
                new_state[r][COLS-1]=state[r][0]
            else:
                new_state[r][c]=state[r][c+1]
        new_state_1 = new_state.ravel()
        horizontal_succ["L"+str((r+1))+","]=new_state_1
       
    li=[]
    for key,value in horizontal_succ.items():
        li.append((key, tuple(value)))

    return li
# move- all column successors up & down
def move2_successors(state):
    #move column elements downwards by one tile
    vertical_succ={}
    for c in range(0,COLS):
        new_state=get_2dArray(state)
        state= get_2dArray(state)
        for r in range(0,ROWS):
            if r==0:
                new_state[0][c]=state[ROWS-1][c]
            else:
                new_state[r][c]=state[r-1][c] 
        new_state_1=new_state.ravel()
        vertical_succ["D"+str((c+1))+","]=new_state_1
    #move column elements upwards by one tile
    for c in range(0,COLS):
        new_state=get_2dArray(state)
        state= get_2dArray(state)
        for r in range(0,ROWS):
            if r==ROWS-1:
                new_state[ROWS-1][c]=state[0][c]
            else:
                new_state[r][c]=state[r+1][c]
        new_state_1=new_state.ravel()
        vertical_succ["U"+str((c+1))+","]=new_state_1

    li=[]
    for key,value in vertical_succ.items():
        
        li.append((key, tuple(value)))

    return li
#move - outer circle clockwise
def move3_successors_OC(state):
    # reference for rotation taken from https://www.geeksforgeeks.org/rotate-matrix-elements/
    first_row = first_col = 0
    last_row = ROWS-1
    last_col = COLS-1
    move3_succ={}
    while (last_col - first_col)==COLS-1 and (last_row-first_row)==ROWS-1:
        state= get_2dArray(state)
        prev_state = state[first_row+1][first_col]
        # Move first row elements to the right by one tile
        for i in range(first_col, last_col+1):
            new_state = state[first_row][i]
            state[first_row][i] = prev_state
            prev_state = new_state
        first_row += 1
        # Move elements of last column down by one tile
        for i in range(first_row, last_row+1):
            new_state = state[i][last_col]
            state[i][last_col] = prev_state
            prev_state = new_state
        last_col -= 1
        # Move elements of last row to the left by one tile
        for i in range(last_col, first_col-1, -1):
            new_state = state[last_row][i]
            state[last_row][i] = prev_state
            prev_state = new_state
        last_row -= 1
        # Move elements of first column up by one tile
        for i in range(last_row, first_row-1, -1):
            new_state = state[i][first_col]
            state[i][first_col] = prev_state
            prev_state = new_state
        first_col += 1
    new_state_1=state.ravel()
    move3_succ["Oc"+","]=new_state_1
    li=[]
    
    for key,value in move3_succ.items():
        li.append((key, tuple(value)))

    return li
#move - outer circle counter clockwise
def move3_successors_OCC(state):
    first_row = first_col = 0
    last_row = ROWS-1
    last_col = COLS-1

    move3_succ={}
    while (last_col - first_col)==COLS-1 and (last_row-first_row)==ROWS-1:
        state= get_2dArray(state)
        prev_state = state[first_row+1][last_col]
 
        # Move elements of first_row to the left by one tile
        for i in range(last_col,first_col-1,-1):
            new_state = state[first_row][i]
            state[first_row][i] = prev_state
            prev_state = new_state 
        first_row += 1
        # Move elements of first_col down by one tile
        for i in range(first_row, last_row+1):
            new_state = state[i][first_col]
            state[i][first_col] = prev_state
            prev_state = new_state
        first_col += 1
        # Move elements of last_row to the right by one tile
        for i in range(first_col,last_col+1):
            new_state = state[last_row][i]
            state[last_row][i] = prev_state
            prev_state = new_state
        last_row -= 1
        # Move elements of last_col up by one tile
        for i in range(last_row, first_row-1,-1):
            new_state = state[i][last_col]
            state[i][last_col] = prev_state
            prev_state = new_state
        last_col -= 1
    
    new_state_1=state.ravel()
    move3_succ["Occ"+","]=new_state_1
    li=[]
    for key,value in move3_succ.items():
        li.append((key, tuple(value)))
    return li

#move - inner circle clockwise
def move4_successors_IC(state):
    first_row = first_col = 1
    last_row = ROWS-2
    last_col = COLS-2

    move4_succ={}
    while (last_col - first_col)==COLS-3 and (last_row-first_row)==ROWS-3:

        state= get_2dArray(state)
        prev_state = state[first_row+1][first_col]
        # Move elements of second row to the right by one tile
        for i in range(first_col, last_col+1):
            new_state = state[first_row][i]
            state[first_row][i] = prev_state
            prev_state = new_state
        first_row += 1
        # Move elements of second_last column down by one tile
        for i in range(first_row, last_row+1):
            new_state = state[i][last_col]
            state[i][last_col] = prev_state
            prev_state = new_state
        last_col -= 1
        # Move elements of second last row to the left by one tile
        for i in range(last_col, first_col-1, -1):
            new_state = state[last_row][i]
            state[last_row][i] = prev_state
            prev_state = new_state
        last_row -= 1
        # Move elements of second column up by one tile
        for i in range(last_row, first_row-1, -1):
            new_state = state[i][first_col]
            state[i][first_col] = prev_state
            prev_state = new_state
        first_col += 1
    
    new_state_1=state.ravel()
    move4_succ["Ic"+","]=new_state_1
    li=[]
    for key,value in move4_succ.items():
        li.append((key, tuple(value)))
    return li

#move - inner circle counter clockwise
def move4_successors_ICC(state):
    first_row = first_col = 1
    last_row = ROWS-2
    last_col = COLS-2

    move4_succ={}
    while (last_col - first_col)==COLS-3 and (last_row-first_row)==ROWS-3:

        state= get_2dArray(state)
        prev_state = state[first_row+1][last_col]
 
        # Move elements of second row to the left by one tile
        for i in range(last_col,first_col-1,-1):
            new_state = state[first_row][i]
            state[first_row][i] = prev_state
            prev_state = new_state
        first_row += 1
        # Move elements of second column down by one tile
        for i in range(first_row, last_row+1):
            new_state = state[i][first_col]
            state[i][first_col] = prev_state
            prev_state = new_state
        first_col += 1
        # Move elements of second last row to the right by one tile
        for i in range(first_col,last_col+1):
            new_state = state[last_row][i]
            state[last_row][i] = prev_state
            prev_state = new_state
        last_row -= 1
        # Move elements of second last column up by one tile
        for i in range(last_row, first_row-1,-1):
            new_state = state[i][last_col]
            state[i][last_col] = prev_state
            prev_state = new_state
        last_col -= 1
    
    new_state_1=state.ravel()
    move4_succ["Icc"+","]=new_state_1
    li=[]
    for key,value in move4_succ.items():
        li.append((key, tuple(value)))
    return li

#function that gets successors for all move, in total 24 possible successors for every state
def successors(state):
    return move1_successors(state) + move2_successors(state) + move3_successors_OC(state)+move3_successors_OCC(state)+move4_successors_IC(state)+move4_successors_ICC(state)

#calculate hamming distance - number of misplaced tiles
def heuristic_misplaced_tiles(state):
    number = 0
    for i, val in enumerate(state):
        if i+1 != val:
            number += 1

    return number
#calculate manhattan distance
def calculateManhattan(state):
    number = 0
    coordinates = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0, 4), 6: (1, 0), 7: (1, 1), 8: (1, 2), 9: (1, 3),
                 10: (1, 4), 11: (2, 0), 12: (2, 1), 13: (2, 2), 14: (2, 3), 15: (2, 4), 16: (3, 0), 17:(3,1), 18:(3,2), 19:(3,3), 20:(3,4),
                 21:(4,0), 22:(4,1), 23:(4,2), 24:(4,3), 25:(4,4)}
    for i,val in enumerate(state):
        
        row,col = int(i/ ROWS) , i% COLS
        goal_row,goal_col = coordinates[val][0], coordinates[val][1]
        number += (math.fabs(col - goal_col) + math.fabs(row - goal_row))           
    return number


    
def solve(initial_board):
    
#     """
#     1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
#     2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
#        For testing we will call this function with single argument(initial_board) and it should return 
#        the solution.
#     3. Please do not use any global variables, as it may cause the testing code to fail.
#     4. You can assume that all test cases will be solvable.
#     5. The current code just returns a dummy solution.

# taken reference from https://py.checkio.org/mission/8-puzzle/publications/sleepyone/python-3/first/?ordering=most_voted&filtering=all
    fringe=[]
    visited=[initial_board]
    
    moves=""
    cost_g_score =0
    # Implement A * search using priority queues-Heapq
    hq.heappush(fringe, (heuristic_misplaced_tiles(initial_board), (initial_board, cost_g_score, moves)))
    
    while fringe:
        _, (state, cost_g, moves) = hq.heappop(fringe)  
        
        for [curr_move,curr_state] in successors(state):
            cost_h_score=heuristic_misplaced_tiles(curr_state) #get h_score - heuristic output
            if sorted(curr_state)==list(curr_state):   #check if goal state has reached, then return moves
                return  ((moves+curr_move.replace(',','')).split(','))
            else:
                if curr_state not in visited:
                    visited.append(curr_state)
                    cost_g_score= cost_g+1 #increment g_score
                    cost_f_score = cost_g_score + cost_h_score  #evaluation function - f_score
                    hq.heappush(fringe, (cost_f_score, (curr_state, cost_g_score, moves + curr_move)))
    return ""



# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))

    
