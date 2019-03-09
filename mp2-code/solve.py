# -*- coding: utf-8 -*-
import queue
import copy
import numpy as np

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
   
    # raise NotImplementedError
# -*- coding: utf-8 -*-
import queue
import copy
import numpy as np

BIG_NUM = 10000


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
    # raise NotImplementedError
    # precompute p_dict(tile dictionary)
    # precompute c_dict(choice dictionary)
    # precompute d_dict(dot dictionary)
    """ 
    p_dict(pentomino dictionary): {P_index : (P_index,O,(x,y) | O is 0,1,2,3(no flip, rot90 0 1 2 3 times)   4,5,6,7(with flip))} -- map pent index to all possible configuration(orientation) of that pent.
        --constraints that requrie all pentominoes to be placed once
	c_dict (choice dictionary): { (P_index,O,(x,y)):((x1,y1),...,(x5,y5))       } ---- map all “choices”(configuration of arbitrary pent) to dots it covers AND P_index
        --variable and value for all possible config of pent
    d_dict (dot dictionary): { (x,y) : (P_index,O,(x,y)) that covers this position       } ----map all dots to possible configuration of pents that cover that particular dot. 
        --constraints that require all dots on the board to be covered
    """
    # for sets, use a.add(10) to add a element 10
    # a & b for intersection. a.remove(b) will throw error if no match
                    #a is dict a.pop(b,None) will not throw error. None is returned if no match
    
    """
    idea:
         enumerate all possible orientation of each pentomino. 
             for each orientation, check on all (x,y) on the board
             if there is one available upper left corner,
             c_dict mapping(choice to all covered and index)
             update p_dict mapping(each c_dict update, back edge)
             dot_dict mapping(each c_dict update, map back edge)
    """
    threshold = np.count_nonzero(pents[0])
    c_dict = {} # variable
    p_dict = {} # constraint
    dot_dict = {} # constraint
    for x in range(len(board)):
        for y in range(len(board[0])):
            dot_dict[(x,y)] = []
    for i in range(len(pents)):
        p_dict[i]= []
    board_copy = copy.deepcopy(board)
    for P_index in range(len(pents)):
        # enumerate pents
        for O in range(8):
            #enumerate orient.
            # 0 1 2 3 (no flip rot O times)
            # 4 5 6 7 (flip 0 rot O%4 times)
            cur_pent = copy.deepcopy(pents[P_index])
            if O > 3:
                # flip along x-axis
                unflipped = np.copy(cur_pent)
                cur_pent = np.flip(cur_pent,1)
                # if flipped is the same as unflipped, continue
                if False not in np.equal(unflipped,cur_pent):
                    continue

            before_rot = np.copy(cur_pent)
            cur_pent = np.rot90(cur_pent, (O%4))
            repeat_flag = 0
            if (O%4!=0):
                for each_O in range(0,O%4):
                    temp_rot = np.rot90(before_rot,each_O)
                    if (temp_rot.shape == cur_pent.shape):
                        if False not in np.equal(temp_rot,cur_pent):
                            repeat_flag = 1
                            break
            # another edge case, flipped version shares similarity wth unflipped?
            if (O>3):
                # there is a flip, so flip it back and check with all previous shapes
                flip_back = np.flip(cur_pent,1)
                for flip_rot in range(4):
                    flip_back_rot = np.rot90(flip_back,flip_rot)
                    if (flip_back_rot.shape == cur_pent.shape):
                        if False not in np.equal(flip_back_rot,cur_pent):
                            repeat_flag = 1
                            break
            if (repeat_flag == 1):
                continue

# threshold is number of 1's in cur_pent
            width=len(cur_pent[0])
            height=len(cur_pent)
            for x in range(len(board)):
                for y in range(len(board[0])):
                    # check if (x,y) would make pents outside of the board
                    if (x+height> len(board)\
                        or y+width>len(board[0])):
                        continue
                    # check if this (x,y) would result in overlap
                    # check first before update
                    # if board has zero, one more condition, check the second '4'
                    invalid_flag = 0
                    for i in range(height):
                        for j in range(width):
                            if (cur_pent[i][j] != 0 and board_copy[x+i][y+j] != 1):
                                # overlap or covering some
                                invalid_flag = 1
                    if (invalid_flag == 1):
                        continue

                    # check if placing on xy would result in unreachable cases.
                    invalid_flag = 0
                    for localx in range(height):
                        for localy in range(width):
                            # check flood fill
                            if cur_pent[localx][localy] != 0:
                                continue
                            if False == floodfill(cur_pent,(x,y),np.copy(board_copy),threshold):
                                invalid_flag = 1
                    if invalid_flag == 1:
                        continue
                    '''
                    Until this point, we don't have a valid placement(choice)
                    Now we can map p_dict index to choice. and map back(c dict)
                    And go into each non-zero position, map dot_dict to choice and back
                    '''
                    cur_choice = (P_index,O,(x,y))
                    # c dict and pdict
                    # not necessary. can get info from first item
                    # will mess up later calculation
                    # if (c_dict.get(cur_choice) is None):
                    #     c_dict[cur_choice]=[P_index]
                    # else:
                    #     c_dict[cur_choice].append(P_index)
                    # p dict map back
                    p_dict[P_index].append(cur_choice)
                    # c dict(not None) and dot dict(could be). 
                    c_dict[cur_choice] = []
                    for i in range(height):
                        for j in range(width):
                            if (cur_pent[i][j]!=0):
                                # c dict update
                                cur_x = i+x # local offset i, upper left x
                                cur_y = j+y # similar
                                c_dict[cur_choice].append((cur_x,cur_y))
                                # dot dict map back
                                if (dot_dict.get((cur_x,cur_y)) is None):
                                    dot_dict[(cur_x,cur_y)] = [cur_choice]
                                else :
                                    dot_dict[(cur_x,cur_y)].append(cur_choice)
    # get rid of all the dots with zero 
    dots_to_delete = []
    for each_dot in dot_dict:
        if len(dot_dict[each_dot])==0:
            dots_to_delete.append(each_dot)
    for each_dot in dots_to_delete:
        dot_dict.pop(each_dot)
    # precomputation done.
    # now the problem is CSP
    # print("precomputation done")
    (_,solution) = solve_csp(c_dict,p_dict,dot_dict,[],pents,board)
    return solution

def solve_csp(c_dict,p_dict,dot_dict,path,pents,board):
    '''
    CSP problem recursion.
    variables (and values): c_dict
    constraints : dot_dict,p_dict(reference)
    result: path
    return boolean(solved or not) and path
    heuristics: LRV to choose the pentomino with least remaining legal move
    LCA: choose the configuration of the pentomino that would prune the least 
            number of choices. 
    note: set should be used when counting.
    '''
    # base case: all assignments have been made, all constraints satisfied.
    if (len(p_dict.keys()) == 0 and len(dot_dict.keys()) == 0):
        # solution!
        # print('solution?L??')
        # reconstruct path according to question prompt.
        result_path = []
        for cur_c in path:
            O = cur_c[1]
            P = cur_c[0]
            x_r = cur_c[2][0]
            y_r = cur_c[2][1]
            cur_pent = np.copy(pents[P])
            if (O > 3):
                cur_pent = np.flip(cur_pent,1)
            cur_pent = np.rot90(cur_pent,O % 4)
            result_path.append((cur_pent,(x_r,y_r)))
        return (True,result_path)
    elif len(c_dict) == 0 and (len(p_dict)!=0 or len(dot_dict)!=0):
        # no solution found.
        # print('not a solution')
        # print(path[-1])
        sol_board = np.zeros(board.shape)
        if (len(path)!=0):
            for each_pent in path:
                pent_of_choice= pents[each_pent[0]]
                pent_of_choice = np.where(pent_of_choice != 0,1,0)
                orientation = each_pent[1]
                if (orientation > 3):
                    pent_of_choice = np.flip( pent_of_choice,1)
                pent_of_choice = np.rot90(pent_of_choice,orientation%4)
                # add the pent to the board
                this_x = each_pent[2][0]
                this_y = each_pent[2][1]
                this_height = len(pent_of_choice)
                this_width = len(pent_of_choice[0])
                sol_board[this_x:this_x+ this_height,this_y:this_y+this_width] += pent_of_choice
        # print(sol_board)
        # print('path length',len(path))
        return (False,[])
    
    # apply LRV: finding the P_index whose available moves are the least.
    # sort P according to its remaining legal move. Which is the size of mapped choice.
    def find_least_remaining_value(pent_in):
        # find how many available configurations are there for a specific type of pent
        # idea: get list of configs mapped to by p_dict, using set AND to eliminate impossible mapping
                # then return length
        config_available = p_dict[pent_in]
        config_valid = set(config_available) & set(c_dict.keys())
        remaining_value = len(config_valid)
        return remaining_value
    def lrv(pent_in):
        # find how many available configurations are there for a specific type of pent
        # idea: get list of configs mapped to by p_dict, using set AND to eliminate impossible mapping
                # then return length
        config_available = p_dict[pent_in]
        config_valid = set(config_available) & set(c_dict.keys())
        remaining_value = len(config_valid)
        return remaining_value
    P_LRV = sorted(p_dict.keys(),key=find_least_remaining_value\
        ,reverse =False)  # increasing order
    for cur_P in P_LRV:
        # forward checking sort of?
        if len(set(p_dict[cur_P]) & set(c_dict.keys())  )==0:
            # there is no choice left. this path is wrong
            continue
        # apply LCA: least constraining assignment. 
        '''
        for each configuration of P, it would remove other P config.
        then it removes all the overlapping dots. get this value and sort.
        '''
        # lca_helper_lambda = lambda choice: len(set(p_dict[choice[0]] +[x for sublist in \
        #     list(map(  lambda a:dot_dict[a],\
        #         c_dict[choice])) \
        #             for x in sublist]) & \
        #         set(c_dict.keys()))
        def least_constraining_assignemnt(choice):
            '''
            Given a configuration, the constraint imposed by this configuration can be found by
            the number of choices eliminated if this one is chosen. 
            There are two types of choices eliminated. 
                1. satified
                2. overlap
            For satisfied, it means all choices with the same pentomino should be eliminated.
            For overlap, it means all the other configurations covering one of the dots covered by this choice should be eliminated. 
            choose the value that rules out the fewest value of the remaining variables.
            Return: total number of VARIABLES eliminated. 
            '''
            satified_choice = p_dict[choice[0]]
            
            covered_dot = c_dict[choice]
            overlap = []
            for each_dot in covered_dot:
                mapped_to_dot = dot_dict[each_dot]
                overlap.extend(mapped_to_dot)
            overall = set(overlap + satified_choice) & set(c_dict.keys()) # eliminate ghost mapping
            return len(overall)
        def lj(choice):
            '''
            Given a configuration, the constraint imposed by this configuration can be found by
            the number of choices eliminated if this one is chosen. 
            There are two types of choices eliminated. 
                1. satified
                2. overlap
            For satisfied, it means all choices with the same pentomino should be eliminated.
            For overlap, it means all the other configurations covering one of the dots covered by this choice should be eliminated. 
            choose the value that rules out the fewest value of the remaining variables.
            Return: total number of VARIABLES eliminated. 
            '''
            satified_choice = p_dict[choice[0]]
            
            covered_dot = c_dict[choice]
            overlap = []
            for each_dot in covered_dot:
                mapped_to_dot = dot_dict[each_dot]
                overlap.extend(mapped_to_dot)
            overall = set(overlap + satified_choice) & set(c_dict.keys()) # eliminate ghost mapping
            return len(overall)


        c_LCA = sorted( list(set(p_dict[cur_P]) & set(c_dict.keys())),key = least_constraining_assignemnt\
             ,reverse = False)
        for cur_c in c_LCA:
            # path.append((cur_c[0],cur_c[2]))



            # reconstruct the fucking tile. 
            path.append(cur_c) # debugging version . Line above is correct
            



            # now a choice has been made. 
            # print out the board with choices made.
            # print_board(path,board,pents)
            lijian = 1+1

            # save to path according to (p1,(x,y)) . overlap: 
                                # loop over each element of dot_dict[for each c_dict[cur_c]], if present in c_dict, discard into temp
                                #loop over each element of p_dict[cur_c[0]], if present, discard into temp. (order matters here.)
                                # then discard p_dict[cur_c[0]] and discard dot_dict 
            # print('current choice is ',cur_c)
            temp_discard_choices = []
            # dot_dict
            covered =c_dict[cur_c]
            # print('this line ')
            # discard choices due to satisfied constrants (dots)
            for covered_dot in covered:
                for each_satified in dot_dict[covered_dot]:
                    attempt_discard = c_dict.pop(each_satified,None)
                    if attempt_discard is not None:
                        # something is discarded from choice array
                        # put key value pair to temp storage
                        temp_discard_choices.append((each_satified,attempt_discard))
            # discard choices due to used pent
            for used_pent in p_dict[cur_c[0]]:
                attempt_discard = c_dict.pop(used_pent,None)
                if (attempt_discard is not None):
                    temp_discard_choices.append((used_pent,attempt_discard))
            # discard term in p_dict and dot_dict(key value pair)
            temp_discard_pent=(cur_c[0],p_dict.pop(cur_c[0]))
            temp_discard_dots= [(disc_key,dot_dict.pop(disc_key)) for disc_key in covered]

            # even more inference. 
            #prune away more choices unavilable due to new block. use floodfill.
            # furthur prune choices if 
            
            # now inferences. check all dots, see if they still have valid mapping.
            bad_flag = 0
            for _each_dot in dot_dict.keys():
                if len( set(dot_dict[_each_dot]) & set(c_dict.keys())    ) == 0:
                    # restore and return
                    # print('which dot',_each_dot)
                    pass
                    path.pop()
                    p_dict[temp_discard_pent[0]] = temp_discard_pent[1]
                    # restore dot_dict, by looping over each tuple in temp
                    for each_discarded_dot in temp_discard_dots:
                        dot_dict[each_discarded_dot[0]] = each_discarded_dot[1]
                    # restore c_dict, in both cases, there is no repetition
                    for each_discarded_choice in temp_discard_choices:
                        c_dict[each_discarded_choice[0]]=each_discarded_choice[1]

                    # print_board(path,board,pents)
                    # print('after undo')
                    bad_flag = 1
                    break
            if (bad_flag == 1):
                break
            

            # now recursion preparation is ready?
            board_copy = np.copy(board) # consists of 1 for uncovered,  0 for unavailable
            # reconstruct the pent ,add to board, check floodfill
            O = cur_c[1]
            P = cur_c[0]
            x_r = cur_c[2][0]
            y_r = cur_c[2][1]
            cur_pent = np.copy(pents[P])
            if (O > 3):
                cur_pent = np.flip(cur_pent,1)
            cur_pent = np.rot90(cur_pent,O % 4) # numbered by index
            width_r = len(cur_pent[0])
            height_r = len(cur_pent)
            board_copy[x_r:x_r + height_r,y_r:y_r+width_r] += cur_pent
            threshold = np.count_nonzero(cur_pent)
            badbad = 0
            if False == check_for_division(threshold,board_copy):
                path.pop()
                p_dict[temp_discard_pent[0]] = temp_discard_pent[1]
                # restore dot_dict, by looping over each tuple in temp
                for each_discarded_dot in temp_discard_dots:
                    dot_dict[each_discarded_dot[0]] = each_discarded_dot[1]
                # restore c_dict, in both cases, there is no repetition
                for each_discarded_choice in temp_discard_choices:
                    c_dict[each_discarded_choice[0]]=each_discarded_choice[1]
                badbad = 1
            if (badbad == 1):
                break




            (is_sol,path_solution) = solve_csp(c_dict,p_dict,dot_dict,path,pents,board_copy)
            if (is_sol):
                return (is_sol,path_solution)
            else: 
                # backtrack here. 
                # print("invalid choice here is",cur_c)
                # print("backtracking here")
                # restore path, dot_dict, p_dict, c_dict
                path.pop()
                p_dict[temp_discard_pent[0]] = temp_discard_pent[1]
                # restore dot_dict, by looping over each tuple in temp
                for each_discarded_dot in temp_discard_dots:
                    dot_dict[each_discarded_dot[0]] = each_discarded_dot[1]
                # restore c_dict, in both cases, there is no repetition
                for each_discarded_choice in temp_discard_choices:
                    c_dict[each_discarded_choice[0]]=each_discarded_choice[1]
    return (False,[]) # still no solution after trying everything?




'''
def lca_helper(choice):
    given a configuration, return the total number of OTHER
    configurations this choice removes. 
    Two parts: overlapped(same pent) and satisfied(same dot)
    two lists might overlap. So just get all the lists and measure lenth
    of the set. 
    get_overlap_list = p_dict[choice[0]]
    # not just the length of the list of dot_dict.
    # we need to intersect the overall thing with the remaining valid c_dict keys
    # to get rid of ghost mapping
    satisfaction_list =  [x for sublist in [list(map(  lambda a:dot_dict[a],c_dict[choice[0]]))] for x in sublist]
    return len(set(get_overlap_list + satisfaction_list) & set(c_dict.keys())
'''
def print_board(path,board,pents):

    sol_board = np.zeros(board.shape)
    if (len(path)!=0):
        pent_used = 0
        for each_pent in path:
            pent_used +=1
            pent_of_choice= pents[each_pent[0]]
            pent_of_choice = np.where(pent_of_choice != 0,1,0)
            pent_of_choice *= pent_used
            orientation = each_pent[1]
            if (orientation > 3):
                pent_of_choice = np.flip( pent_of_choice,1)

            pent_of_choice = np.rot90(pent_of_choice,orientation%4)
            # add the pent to the board
            this_x = each_pent[2][0]
            this_y = each_pent[2][1]
            this_height = len(pent_of_choice)
            this_width = len(pent_of_choice[0])
            sol_board[this_x:this_x+ this_height,this_y:this_y+this_width] += pent_of_choice
        # print('\n\n')
        # print('pent used is ',pent_used)
        # print(sol_board)



def floodfill(cur_pent,coor,board,threshold):
    import queue
    x = coor[0]
    y = coor[1]
    height = len(cur_pent)
    width = len(cur_pent[0])
    board[x:x+height,y:y+width] += cur_pent
    # board consists of 1 and 2 and possibly 0 .
    # 2 is occupied, 1 is empty, 0 is unavailable.
    '''
    for each 1 inside the block of cur_pent,
    go out using BFS, and only check for connected 1's. 
    if the number exceeds threshold.
    '''
    is_valid = False
    for localx in range(height):
        for localy in range(width):
            if cur_pent[localx][localy] == 0:
                if board[localx][localy] > 1 or board[localx][localy]==0: 
                    continue
                # floodfill algorithm here.
                start = (x+localx,y+localy)
                q = queue.Queue()
                q.put(start)
                processed = 0
                while(not q.empty()):
                    current = q.get()
                    processed +=1
                    if (processed >= threshold):
                        is_valid = True
                        break
                    # check neighbors. if there is a match, push.
                    # check if within range,
                    # check if 1, then push
                    # else nothing
                    # up
                    up = (current[0]-1,current[1])
                    if (up[0] >= 0):
                        if board[up[0],up[1]]==1:
                            q.put(up)

                    #down
                    down = (current[0]+1,current[1])
                    if (down[0]<len(board)):
                        if board[down[0],down[1]]==1:
                            q.put(down)

                    #left
                    left = (current[0],current[1]-1)
                    if (left[1]>=0):
                        if board[left[0],left[1]]==1:
                            q.put(left)

                    #right
                    right = (current[0],current[1]+1)
                    if (right[1]< len(board[0])):
                        if board[right[0],right[1]]==1:
                            q.put(right)

                if (processed < threshold):
                    return False
    return is_valid

                
def check_for_division(threshold,board):
    '''
    return False if remaining connected area has value not devisible 
    by threshold.
    '''
    uncovered1 = np.argwhere(board == 1)
    uncovered = []
    for each_uncovered in uncovered1:
        uncovered.append(list(each_uncovered))

    while(len(uncovered)!= 0 ):
        count_connect = 0
        start = uncovered[0]
        del uncovered[0] # delete start, and all its connected neighbors 
        q = queue.Queue()
        q.put(start)
        
        # begin expanding 
        while( not q.empty()):
            current = q.get()
            count_connect +=1
            # neighbors, if neighors in the uncovered, push and remove 
            # up
            up = [current[0]-1,current[1]]
            if (up in uncovered):
                uncovered.remove(up)
                q.put(up)

            down = [current[0]+1,current[1]]
            if (down in uncovered):
                uncovered.remove(down)
                q.put(down)

            left = [current[0],current[1]-1]
            if (left in uncovered):
                uncovered.remove(left)
                q.put(left)

            right = [current[0],current[1]+1]
            if (right in uncovered):
                uncovered.remove(right)
                q.put(right)


        # end expanding 
        if count_connect% threshold != 0:
            return False # no divisible
    return True