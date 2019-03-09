# -*- coding: utf-8 -*-
import copy
import numpy as np
import queue
BIG_NUM = 10000

def is_qualified(board_block, pentominos,point, rows, cols):
    # check if it is out of bound
    x,y = pentominos.shape
    if((point[0]+x) > rows or (point[1]+y) > cols):
        return False
    S = np.sum(board_block*pentominos)
    if(S >= BIG_NUM): # some other pentominos already occupy that spot
        return False
    # check no zeros was coverd
    before, = pentominos[np.where(pentominos == 0)].shape
    temp = board_block*pentominos
    after, = temp[np.where(temp == 0)].shape
    if before != after:
        return False
    return True


# forward_check(board, board_block,point)
# input: board: just board     
#        pentominos: just pentominos
#        point: the position to place the pentominos
# output: if there are n-1 ones where n = pentominos size was enclosed, return false, else return true
#
def forward_check(board, pentominos,point):
    q = queue.LifoQueue()
    n, = pentominos[np.where(pentominos != 0)].shape
    temp_board = copy.deepcopy(board)
    block_h,block_w = pentominos.shape
    temp_board[point[0]:point[0]+block_h][point[1]:point[1]+block_w] += BIG_NUM*pentominos
    visited = np.ones_like(board, dtype = bool)
    visited[np.where(temp_board == 1)] = False
    ##print(x)
    # print(visited)
    point = np.argwhere(visited == False)
    while(point.shape[0] != 0): # check different group of 1
        starting_point = point[0]
        q.put(starting_point)
        count = 0
        while(not q.empty()): # dfs in that group
            flag = 0
            temp = q.get()
            while(visited[temp[0]][temp[1]] == True):
                if(q.empty()):
                    flag = 1
                    break
                temp = q.get()
            cur = temp
            visited[cur[0]][cur[1]] = True
            if(flag == 0):
                count += 1
            #push neighbor
            if((cur[0] -1)>=0 and visited[cur[0] -1][cur[1]] != True):
                q.put((cur[0]-1, cur[1]))
            if((cur[0] +1)< h and visited[cur[0] + 1][cur[1]] != True):
                q.put((cur[0]+1, cur[1]))
            if((cur[1] -1)>=0 and visited[cur[0]][cur[1]-1] != True):
                q.put((cur[0], cur[1] -1))
            if((cur[1] +1)< w and visited[cur[0]][cur[1]+1] != True):
                q.put((cur[0], cur[1] +1))
        if(count <= n-1):
            return False
        point = np.argwhere(visited == False)
    # print(retval)
    return True

            

def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You can assume there will always be a solution.
    """
    # expand the pents
    raise NotImplementedError
