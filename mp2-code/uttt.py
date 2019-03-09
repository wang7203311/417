from time import sleep
from math import inf
from random import randint
import random
import math
class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.actor = -5000
        self.cur_unblock = 500
        self.cur_greater = 10



        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30
        self.debug = 0
        self.expandedNodes=0
        self.currPlayer=True
        self.cur_index = 4
        
        
        # for own vs pre
        self.opp_ready_win_index = []
        self.last_step = (-1,-1)
        self.own_is_max = True
        self.play_vs_own = False


    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        # for MaxPlayer
        # if(self.debug > 0):
        #     # self.printGameBoard()
            # print(isMax)
        if (isMax):
            # print(corner_taken)
            """
            first rule: if a local board forms 3 in a row, score is winnerMaxUtility and return
            second: if first one doesn't work, each open two-in-a-row increases utility by 500. blocked two-in-a-row
                increments utility by 100
            Third: for each corner taken, increment utility by 30.
            """
            score=0
            two_in_a_row_open = 0 # keeping track of max open twos
            two_in_a_row_block = 0 # keeping track of min open twos blocked 
            corner_taken = 0 # number of corners taken by maxPlayer
            # first rule
            for local_board_index in self.globalIdx:
                # for each local board, create local variable keeping track of wins and open twos and closed twos. 
                # "X" give weight 1. "_" give weight 0. "O" give weight -10                 
                # if weight for a row or col or diag is 3, that's a win; -30, lose; -18, blocked two-in-a-row;
                #                               2 open two-in-a-row
                i =[ [self.board[local_row + local_board_index[0]][local_col \
                    + local_board_index[1]] for local_col in range(3) ] for local_row in range(3) ]
                # i is local board 3by3 list of lists? IDK
                # print(i)
                # print("xxxxxxxxxxxxx")
                # self.debug = 0
                for row in i:
                    row_weight = 0 # reset for each row.
                    for row_elem in row:
                        if (row_elem == self.maxPlayer):
                            row_weight +=1
                        if (row_elem == self.minPlayer):
                            row_weight -= 10
                        else:
                            row_weight +=0
                    # for each row, identify the nature of the row .
                    if row_weight == 3:
                        return self.winnerMaxUtility
                    if row_weight == 2: # 1 + 1 + 0
                        two_in_a_row_open +=1
                    if row_weight == -20+1: # -10 + -10 + 1
                        two_in_a_row_block +=1
                for col in range(3):
                    col_weight = 0 # reset for each row.
                    for col_elem in [i[row_index][col] for row_index in range(3)]: # get i[0,1,2][col]
                        if (col_elem == self.maxPlayer):
                            col_weight +=1
                        if (col_elem == self.minPlayer):
                            col_weight -= 10
                        else:
                            col_weight +=0
                    # for each col, identify the nature of the col.
                    if col_weight == 3:
                        return self.winnerMaxUtility
                    if col_weight == 2: # 1 + 1 + 0
                        two_in_a_row_open +=1
                    if col_weight == -19: # -10 + -10 + 1
                        two_in_a_row_block +=1
                #check diagonal.
                weight = 0
                for diag_index in range(3):
                    if (i[diag_index][diag_index] == self.maxPlayer):
                        weight +=1
                    if (i[diag_index][diag_index] == self.minPlayer):
                        weight -= 10
                    else :
                        weight += 0
                if weight == 3:
                    return self.winnerMaxUtility
                if weight == 2:
                    two_in_a_row_open +=1
                if weight == -19: 
                    two_in_a_row_block +=1
                #check the other diagonal
                weight = 0
                for diag_index in range(3):
                    if (i[2-diag_index][diag_index] == self.maxPlayer):
                        weight +=1
                    if (i[2-diag_index][diag_index] == self.minPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 3:
                    return self.winnerMaxUtility
                if weight == 2:
                    two_in_a_row_open +=1
                if weight == -19: 
                    two_in_a_row_block +=1
                #check for coners. 4 cornors. hardcode the thing
                if (i[0][0] == self.maxPlayer):
                    corner_taken +=1
                if i[0][2] == self.maxPlayer:
                    corner_taken +=1
                if i[2][0] == self.maxPlayer:
                    corner_taken +=1
                if i[2][2] == self.maxPlayer:
                    corner_taken +=1
            
            # tally score here if it comes to that. 
            # print(corner_taken)
            if (two_in_a_row_open != 0 or two_in_a_row_block != 0):
                # second rule apply
                score = two_in_a_row_open * self.twoInARowMaxUtility + two_in_a_row_block * self.preventThreeInARowMaxUtility
                # if(self.debug > 0):
                #     print(score)
                # return score
            else : 
                # third rule apply
                score = corner_taken * self.cornerMaxUtility
                # if(self.debug > 0):
                #     print(score)
                # return score
            # if(self.debug > 0):
            #     self.printGameBoard()
            #     print(score)
            return score

        #for MinPlay
        else:
            # print("here")
            """
            first rule: if a local board forms 3 in a row, score is minutility
            second: if first one doesn't work, each open two-in-a-row decrease  utility by 100. blocked two-in-a-row
                decrease utility by 500
            Third: for each corner taken, decrease utility by 30.
        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30
            """
            score=0
            two_in_a_row_open = 0 # keeping track of max open twos
            two_in_a_row_block = 0 # keeping track of min open twos blocked 
            corner_taken = 0 # number of corners taken by maxPlayer
            # first rule
            for local_board_index in self.globalIdx:
                # for each local board, create local variable keeping track of wins and open twos and closed twos. 
                # "X" give weight 1. "_" give weight 0. "O" give weight -10                 
                # if weight for a row or col or diag is 3, that's a win; -30, lose; -18, blocked two-in-a-row;
                #                               2 open two-in-a-row
                i =[ [self.board[local_row + local_board_index[0]]\
                    [local_col + local_board_index[1]] for local_col in range(3) ] for local_row in range(3) ]
                # i is local board 3by3 list of lists? IDK

                for row in i:
                    row_weight = 0 # reset for each row.
                    for row_elem in row:
                        if (row_elem == self.minPlayer):
                            row_weight +=1
                        if (row_elem == self.maxPlayer):
                            row_weight -= 10
                        else:
                            row_weight +=0
                    # for each row, identify the nature of the row .
                    if row_weight == 3: # 1 1 1
                        return self.winnerMinUtility
                    if row_weight == 2: # 1 + 1 + 0
                        two_in_a_row_open +=1
                    if row_weight == -19: # -10 + -10 + 1
                        two_in_a_row_block +=1
                for col in range(3):
                    col_weight = 0 # reset for each row.
                    for col_elem in [i[row_index][col] for row_index in range(3)]: # get i[0,1,2][col]
                        if (col_elem == self.minPlayer):
                            col_weight +=1
                        if (col_elem == self.maxPlayer):
                            col_weight -= 10
                        else:
                            col_weight +=0
                    # for each row, identify the nature of the row .
                    if col_weight == 3:
                        return self.winnerMinUtility
                    if col_weight == 2: # 1 + 1 + 0
                        two_in_a_row_open +=1
                    if col_weight == -19: # -10 + -10 + 1
                        two_in_a_row_block +=1
                #check diagonal.
                weight = 0
                for diag_index in range(3):
                    if (i[diag_index][diag_index] == self.minPlayer):
                        weight +=1
                    if (i[diag_index][diag_index] == self.maxPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 3:
                    return self.winnerMinUtility
                if weight == 2:
                    two_in_a_row_open +=1
                if weight == -19: 
                    two_in_a_row_block +=1
                #check the other diagonal
                weight = 0
                for diag_index in range(3):
                    if (i[2-diag_index][diag_index] == self.minPlayer):
                        weight +=1
                    if (i[2-diag_index][diag_index] == self.maxPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 3:
                    return self.winnerMinUtility
                if weight == 2:
                    two_in_a_row_open +=1
                if weight == -19: 
                    two_in_a_row_block +=1
                #check for coners. 4 cornors. hardcode the thing
                if (i[0][0] == self.minPlayer):
                    corner_taken +=1
                if i[0][2] == self.minPlayer:
                    corner_taken +=1
                if i[2][0] == self.minPlayer:
                    corner_taken +=1
                if i[2][2] == self.minPlayer:
                    corner_taken +=1
            # tally score here if it comes to that. 
            
            if (two_in_a_row_open != 0 or two_in_a_row_block != 0):
                # second rule apply
                score = two_in_a_row_open * self.twoInARowMinUtility + two_in_a_row_block * self.preventThreeInARowMinUtility
                # if(self.debug > 0):
                #     print(" 2")
            else : 
                # third rule apply
                score = corner_taken * self.cornerMinUtility
                # if(self.debug > 0):
                #     print(" 3")
            # print(self.debug)
            # if(self.debug > 0):
            #     self.printGameBoard()
            #     print(score)
            return score

    def check_opp_win(self):
        temp = []
        if(self.own_is_max):
            for local_board_index in self.globalIdx:
                i =[ [self.board[local_row + local_board_index[0]]\
                    [local_col + local_board_index[1]] for local_col in range(3) ] for local_row in range(3) ]
                flag = 0
                for row in i:
                    row_weight = 0 # reset for each row.
                    for row_elem in row:
                        if (row_elem == self.minPlayer):
                            row_weight +=1
                        if (row_elem == self.maxPlayer):
                            row_weight -= 10
                        else:
                            row_weight +=0
                    # for each row, identify the nature of the row .
                    if row_weight == 2: # 1 + 1 + 0
                        temp.append(local_board_index)
                        flag = 1
                        break
                if(flag == 1):
                    continue
                for col in range(3):
                    col_weight = 0 # reset for each row.
                    for col_elem in [i[row_index][col] for row_index in range(3)]: # get i[0,1,2][col]
                        if (col_elem == self.minPlayer):
                            col_weight +=1
                        if (col_elem == self.maxPlayer):
                            col_weight -= 10
                        else:
                            col_weight +=0
                    # for each row, identify the nature of the row .
                    if col_weight == 2: # 1 + 1 + 0
                        temp.append(local_board_index)
                        flag = 1
                        break
                if(flag == 1):
                    continue
                #check diagonal.
                weight = 0
                for diag_index in range(3):
                    if (i[diag_index][diag_index] == self.minPlayer):
                        weight +=1
                    if (i[diag_index][diag_index] == self.maxPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 2:
                    temp.append(local_board_index)
                    flag = 1
                if(flag == 1):
                    continue
                #check the other diagonal
                weight = 0
                for diag_index in range(3):
                    if (i[2-diag_index][diag_index] == self.minPlayer):
                        weight +=1
                    if (i[2-diag_index][diag_index] == self.maxPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 2:
                    temp.append(local_board_index)
                    flag = 1
                if(flag == 1):
                    continue 
        else:
            for local_board_index in self.globalIdx:
                i =[ [self.board[local_row + local_board_index[0]]\
                    [local_col + local_board_index[1]] for local_col in range(3) ] for local_row in range(3) ]
                flag = 0
                for row in i:
                    row_weight = 0 # reset for each row.
                    for row_elem in row:
                        if (row_elem == self.maxPlayer):
                            row_weight +=1
                        if (row_elem == self.minPlayer):
                            row_weight -= 10
                        else:
                            row_weight +=0
                    # for each row, identify the nature of the row .
                    if row_weight == 2: # 1 + 1 + 0
                        temp.append(local_board_index)
                        flag = 1
                        break
                if(flag == 1):
                    continue
                for col in range(3):
                    col_weight = 0 # reset for each row.
                    for col_elem in [i[row_index][col] for row_index in range(3)]: # get i[0,1,2][col]
                        if (col_elem == self.maxPlayer):
                            col_weight +=1
                        if (col_elem == self.minPlayer):
                            col_weight -= 10
                        else:
                            col_weight +=0
                    # for each row, identify the nature of the row .
                    if col_weight == 2: # 1 + 1 + 0
                        temp.append(local_board_index)
                        flag = 1
                        break
                if(flag == 1):
                    continue
                #check diagonal.
                weight = 0
                for diag_index in range(3):
                    if (i[diag_index][diag_index] == self.maxPlayer):
                        weight +=1
                    if (i[diag_index][diag_index] == self.minPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 2:
                    temp.append(local_board_index)
                    flag = 1
                if(flag == 1):
                    continue
                #check the other diagonal
                weight = 0
                for diag_index in range(3):
                    if (i[2-diag_index][diag_index] == self.maxPlayer):
                        weight +=1
                    if (i[2-diag_index][diag_index] == self.minPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 2:
                    temp.append(local_board_index)
                    flag = 1
                if(flag == 1):
                    continue 
            self.opp_ready_win_index = temp
        return

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        """
            rule 1: win +10000, lost -10000, 打假赛 -5000
            rule 2: unblocked 2-in-1-row: +500(current index)
                                          +250(else)
                    block-opp: 100
            rule 3: own agent > opp agent in current local board + 10
                    corner + 20
        """
        #YOUR CODE HERE
        score=0
        if(isMax):
            #first rule
            result = self.checkWinner()
            if(result == 1):
                return self.winnerMaxUtility
            elif(result == -1):
                return self.winnerMinUtility
            last_index = self.last_step
            idx = 3*last_index[0] + last_index[1]
            if(idx in self.opp_ready_win_index):
                return self.actor
            #rule 2:
            two_in_a_row_open = 0 # keeping track of max open twos
            two_in_a_row_block = 0 # keeping track of min open twos blocked 
            corner_taken = 0
            for local_board_index in self.globalIdx:
                i =[ [self.board[local_row + local_board_index[0]][local_col \
                    + local_board_index[1]] for local_col in range(3) ] for local_row in range(3) ]
                max_p = 0
                min_p = 0
                greater = 0
                for row in i:
                    row_weight = 0 # reset for each row.
                    for row_elem in row:
                        if (row_elem == self.maxPlayer):
                            row_weight +=1
                            max_p += 1
                        if (row_elem == self.minPlayer):
                            row_weight -= 10
                            min_p += 1
                        else:
                            row_weight +=0
                    # for each row, identify the nature of the row .
                    if row_weight == 2: # 1 + 1 + 0
                        if(local_board_index == self.cur_index):
                            two_in_a_row_open +=1
                        else:
                            two_in_a_row_open +=0.5
                    if row_weight == -20+1: # -10 + -10 + 1
                        two_in_a_row_block +=1
                if(local_board_index == self.cur_index):
                    if(max_p > min_p):
                        greater = 1
                for col in range(3):
                    col_weight = 0 # reset for each row.
                    for col_elem in [i[row_index][col] for row_index in range(3)]: # get i[0,1,2][col]
                        if (col_elem == self.maxPlayer):
                            col_weight +=1
                        if (col_elem == self.minPlayer):
                            col_weight -= 10
                        else:
                            col_weight +=0
                    # for each col, identify the nature of the col.
                    if col_weight == 2: # 1 + 1 + 0
                        if(local_board_index == self.cur_index):
                            two_in_a_row_open +=1
                        else:
                            two_in_a_row_open +=0.5
                    if col_weight == -19: # -10 + -10 + 1
                        two_in_a_row_block +=1
                #check diagonal.
                weight = 0
                for diag_index in range(3):
                    if (i[diag_index][diag_index] == self.maxPlayer):
                        weight +=1
                    if (i[diag_index][diag_index] == self.minPlayer):
                        weight -= 10
                    else :
                        weight += 0
                if weight == 2:
                    if(local_board_index == self.cur_index):
                        two_in_a_row_open +=1
                    else:
                        two_in_a_row_open +=0.5
                if weight == -19: 
                    two_in_a_row_block +=1
                #check the other diagonal
                weight = 0
                for diag_index in range(3):
                    if (i[2-diag_index][diag_index] == self.maxPlayer):
                        weight +=1
                    if (i[2-diag_index][diag_index] == self.minPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 2:
                    if(local_board_index == self.cur_index):
                        two_in_a_row_open +=1
                    else:
                        two_in_a_row_open +=0.5
                if weight == -19: 
                    two_in_a_row_block +=1
                #check for coners. 4 cornors. hardcode the thing
                if (i[0][0] == self.maxPlayer):
                    corner_taken +=1
                if i[0][2] == self.maxPlayer:
                    corner_taken +=1
                if i[2][0] == self.maxPlayer:
                    corner_taken +=1
                if i[2][2] == self.maxPlayer:
                    corner_taken +=1
            
            # tally score here if it comes to that. 
            # print(corner_taken)
            if (two_in_a_row_open != 0 or two_in_a_row_block != 0):
                # second rule apply
                score = two_in_a_row_open * self.twoInARowMaxUtility + two_in_a_row_block * self.preventThreeInARowMaxUtility
                # if(self.debug > 0):
                #     print(score)
                return score
            else : 
                # third rule apply
                score = corner_taken * self.cornerMaxUtility + greater * self.cur_greater
                # if(self.debug > 0):
                #     print(score)
                return score

        else:
            #first rule
            result = self.checkWinner()
            if(result == -1):
                return self.winnerMinUtility
            elif(result == 1):
                return self.winnerMaxUtility
            last_index = self.last_step
            idx = 3*last_index[0] + last_index[1]
            if(idx in self.opp_ready_win_index):
                return -1*self.actor
            #rule 2:
            two_in_a_row_open = 0 # keeping track of max open twos
            two_in_a_row_block = 0 # keeping track of min open twos blocked 
            corner_taken = 0
            for local_board_index in self.globalIdx:
                i =[ [self.board[local_row + local_board_index[0]][local_col \
                    + local_board_index[1]] for local_col in range(3) ] for local_row in range(3) ]
                max_p = 0
                min_p = 0
                greater = 0
                for row in i:
                    row_weight = 0 # reset for each row.
                    for row_elem in row:
                        if (row_elem == self.maxPlayer):
                            row_weight +=1
                            max_p += 1
                        if (row_elem == self.minPlayer):
                            row_weight -= 10
                            min_p += 1
                        else:
                            row_weight +=0
                    # for each row, identify the nature of the row .
                    if row_weight == 2: # 1 + 1 + 0
                        if(local_board_index == self.cur_index):
                            two_in_a_row_open +=1
                        else:
                            two_in_a_row_open +=0.5
                    if row_weight == -20+1: # -10 + -10 + 1
                        two_in_a_row_block +=1
                if(local_board_index == self.cur_index):
                    if(max_p > min_p):
                        greater = 1
                for col in range(3):
                    col_weight = 0 # reset for each row.
                    for col_elem in [i[row_index][col] for row_index in range(3)]: # get i[0,1,2][col]
                        if (col_elem == self.maxPlayer):
                            col_weight +=1
                        if (col_elem == self.minPlayer):
                            col_weight -= 10
                        else:
                            col_weight +=0
                    # for each col, identify the nature of the col.
                    if col_weight == 2: # 1 + 1 + 0
                        if(local_board_index == self.cur_index):
                            two_in_a_row_open +=1
                        else:
                            two_in_a_row_open +=0.5
                    if col_weight == -19: # -10 + -10 + 1
                        two_in_a_row_block +=1
                #check diagonal.
                weight = 0
                for diag_index in range(3):
                    if (i[diag_index][diag_index] == self.maxPlayer):
                        weight +=1
                    if (i[diag_index][diag_index] == self.minPlayer):
                        weight -= 10
                    else :
                        weight += 0
                if weight == 2:
                    if(local_board_index == self.cur_index):
                        two_in_a_row_open +=1
                    else:
                        two_in_a_row_open +=0.5
                if weight == -19: 
                    two_in_a_row_block +=1
                #check the other diagonal
                weight = 0
                for diag_index in range(3):
                    if (i[2-diag_index][diag_index] == self.maxPlayer):
                        weight +=1
                    if (i[2-diag_index][diag_index] == self.minPlayer):
                        weight -= 10
                    else :
                        weight +=0
                if weight == 2:
                    if(local_board_index == self.cur_index):
                        two_in_a_row_open +=1
                    else:
                        two_in_a_row_open +=0.5
                if weight == -19: 
                    two_in_a_row_block +=1
                #check for coners. 4 cornors. hardcode the thing
                if (i[0][0] == self.maxPlayer):
                    corner_taken +=1
                if i[0][2] == self.maxPlayer:
                    corner_taken +=1
                if i[2][0] == self.maxPlayer:
                    corner_taken +=1
                if i[2][2] == self.maxPlayer:
                    corner_taken +=1
            
            # tally score here if it comes to that. 
            # print(corner_taken)
            if (two_in_a_row_open != 0 or two_in_a_row_block != 0):
                # second rule apply
                score = two_in_a_row_open * self.twoInARowMinUtility + two_in_a_row_block * self.preventThreeInARowMinUtility
                return score
            else : 
                # third rule apply
                score = corner_taken * self.cornerMinUtility + greater * self.cur_greater* -1
                return score


        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        # loop over all possible positions. If there is an empty space, return True.
        for i in self.board:
            for j in i:
                if j=='_':
                    return True
        # return false when all position possible are occupied by X or O
        return False 

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        """ 
        The idea is that first loop over each row for every local board. 
        if there is a case where three elements are equal, if it is either X or O
            return immediately the corresponding thing. 
            Else, keep going
        if all rows are exhausted, check all columns, do the same thing. 
        then check all the diagonals. do the same thing. 
        at the very last, return 0.
        """
      
        for each_local_start in self.globalIdx:
            local_board =[ [self.board[each_local_start[0]+local_row]\
                                [each_local_start[1]+local_col] for local_col in range(3)]\
                                for local_row in range(3) ]
            # check each row
            for local_row in local_board:
                if (len(set(local_row)) == 1):
                    # there is a three in a row
                    if local_row[0] == self.maxPlayer:
                        # maxPlayer wins
                        return 1
                    if local_row[0] == self.minPlayer:
                        return -1
            # check each col
            # variable NOT inherited from above
            col_array = [[local_board[local_row][local_col] for local_row in range(3)]\
                        for local_col in range(3)]
            for local_col in col_array:
                if (len(set(local_col)) == 1):
                    # there is a three in a col
                    if local_col[0] == self.maxPlayer:
                        return 1
                    if local_col[0] == self.minPlayer:
                        return -1
            # check each diag
            # variable NOT inherited from above
            diag_array=[]
            diag_array.append( [local_board[diag_row][diag_row] for diag_row in range(3)] )
            diag_array.append( [local_board[len(local_board)-1-diag_row][diag_row] for diag_row in range(3)] )
            for diag in diag_array:
                if (len(set(diag)) == 1):
                    # there is a three in a col
                    if diag[0] == self.maxPlayer:
                        return 1
                    if diag[0] == self.minPlayer:
                        return -1
        # if program is here, there is no winner
        return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        # self.
        #YOUR CODE HERE
        if(depth <= 0):
            if(not self.play_vs_own): # not play with own agent
                # print("here")
                return self.evaluatePredifined(not isMax)
            else:
                if(self.own_is_max == (not isMax)):   # evaluate own agent
                    # print("here")
                    return self.evaluateDesigned(not isMax)
                else:
                    # if(self.debug == 1):
                    # print("here")
                    return self.evaluatePredifined(not isMax)
            # print("depth is 3: ",self.evaluatePredifined(not isMax))
        local_board_index = self.globalIdx[currBoardIdx]
        l_row = local_board_index[0]
        l_col = local_board_index[1] # local col
        if(isMax):
            max_util = -10000000000
            # local_board_index = self.globalIdx[currBoardIdx]
            for row in range(0, 3):
                for col in range(0, 3):
                    if (self.board[row+l_row][col+l_col] == '_'):
                        self.board[row+l_row][col+l_col] = self.maxPlayer
                        self.expandedNodes += 1
                        util = self.alphabeta(depth - 1, 3*row+col,alpha,beta,not isMax)
                        max_util = max(max_util, util)
                        alpha = max(alpha,max_util)
                        self.board[row+l_row][col+l_col] = '_'
                        if(beta <= alpha):
                            break
            return max_util

        else:
            min_util = 10000000000
            # local_board_index = self.globalIdx[currBoardIdx]
            for row in range(0, 3):
                for col in range(0, 3):
                    if (self.board[row+l_row][col+l_col] == '_'):
                        self.board[row+l_row][col+l_col] = self.minPlayer
                        self.expandedNodes += 1
                        util = self.alphabeta(depth - 1,3*row+col,alpha,beta ,not isMax)
                        min_util = min(min_util, util)
                        beta = min(beta,min_util)
                        self.board[row+l_row][col+l_col] = '_'
                        if(beta <= alpha):
                            break
            return min_util


    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        """ 
        idea: recursive function. 
        make a copy of the current board
        if (depth <= 0) : return the evaluation of the board
        if (isMax): for each possible place on the board,place one on local
                                copy , recurse.
                        after return, revert the board with the local copy
        if (isMin): for each possible place, place on local copy, recurse
                        after recurse return, revert the board with local copy
        """
        # evaluate base case first to save space
        if(depth <= 0):
            # print("depth is 3: ",self.evaluatePredifined(not isMax))
            return self.evaluatePredifined(not isMax)
        local_board_index = self.globalIdx[currBoardIdx]
        l_row = local_board_index[0]
        l_col = local_board_index[1] # local col
        if(isMax):
            max_util = -10000000000
            # local_board_index = self.globalIdx[currBoardIdx]
            for row in range(0, 3):
                for col in range(0, 3):
                    if (self.board[row+l_row][col+l_col] == '_'):
                        self.board[row+l_row][col+l_col] = self.maxPlayer
                        self.expandedNodes += 1
                        # if(self.checkWinner() == 1 and self.debug == 1):
                        #     self.printGameBoard()
                        #     print(depth)
                        #     self.board[row+l_row][col+l_col] = '_'
                        #     return self.winnerMaxUtility
                        util = self.minimax(depth - 1, 3*row+col, not isMax)
                        # if(self.debug > 0):
                        #     print(max_util)
                        #     self.printGameBoard()
                        
                        max_util = max(max_util, util)
                        self.board[row+l_row][col+l_col] = '_'
            return max_util

        else:
            min_util = 10000000000
            # local_board_index = self.globalIdx[currBoardIdx]
            for row in range(0, 3):
                for col in range(0, 3):
                    if (self.board[row+l_row][col+l_col] == '_'):
                        self.board[row+l_row][col+l_col] = self.minPlayer
                        self.expandedNodes += 1
                        util = self.minimax(depth - 1, 3*row+col, not isMax)
                        min_util = min(min_util, util)
                        self.board[row+l_row][col+l_col] = '_'
            return min_util


    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        expandedNodes = []
        self.cur_index = self.startBoardIdx
        self.currPlayer = maxFirst
        # self.play_vs_own = True
        # maxFirst, both minimax
        # if (maxFirst and isMinimaxDefensive and isMinimaxDefensive)
        # flag = 0
        while (self.checkMovesLeft()):
        # for i in range(1):
            local_board_index = self.globalIdx[self.cur_index]
            l_row = local_board_index[0]
            l_col = local_board_index[1] 
            alpha = -1000000000000
            beta = 10000000000000
            depth = self.maxDepth
            # if(i == 7):
            #     self.debug = 1
                # print(self.currPlayer)
            if(self.currPlayer): # max player and max is offensive
                best_val = -1000000000000
                best_move = (-1,-1)
                best_index = -1
                # if(isMinimaxOffensive):   # use minimax
                result = self.checkWinner()
                # print(vertex)
                if(result != 0):
                    return gameBoards, bestMove, expandedNodes, bestValue, result
                for row in range(3):
                    for col in range(3):
                        if self.board[row+l_row][col+l_col] == '_':
                            # temp_move = (vertex[0] + row, vertex[1] + col)
                            flag = 0
                            # self.debug = 1
                            self.board[row+l_row][col+l_col] = self.maxPlayer
                            self.expandedNodes += 1
                            if(self.checkWinner() == 1):
                                best_move = (row+l_row, col+l_col)
                                bestMove.append(best_move)
                                bestValue.append(self.winnerMaxUtility)
                                gameBoards.append(self.board)
                                expandedNodes.append(self.expandedNodes)
                                return gameBoards, bestMove, expandedNodes, bestValue, 1
                            if(isMinimaxOffensive):   # use minimax
                                temp_val = self.minimax(depth - 1, 3*row+col, not self.currPlayer)
                            else:
                                flag = 1
                                temp_val = self.alphabeta(depth-1, 3*row+col,alpha,beta,not self.currPlayer)
                            self.board[row+l_row][col+l_col] = '_'
                            # self.debug = 0
                            if(temp_val > best_val):
                                best_move = (row+l_row, col+l_col)
                                best_index = row*3+col
                            best_val = max(temp_val,best_val)
                            if(flag == 1):
                                alpha = max(alpha,best_val)
                                if(beta <= alpha):
                                    break
                # print(best_val)
                self.cur_index = best_index
                bestMove.append(best_move)
                bestValue.append(best_val)
                gameBoards.append(self.board)
                self.board[best_move[0]][best_move[1]] = self.maxPlayer
                expandedNodes.append(self.expandedNodes)
                self.expandedNodes = 0
                self.currPlayer = not self.currPlayer
            else: # min player and max is defensive
                best_val = 1000000000000
                best_move = (-1,-1)
                best_index = -1
                # if(isMinimaxOffensive):   # use minimax
                result = self.checkWinner()
                # print(vertex)
                self.debug = 1
                if(result != 0):
                    return gameBoards, bestMove, expandedNodes, bestValue, result
                for row in range(3):
                    for col in range(3):
                        if self.board[row+l_row][col+l_col] == '_':
                            # temp_move = (vertex[0] + row, vertex[1] + col)
                            self.board[row+l_row][col+l_col] = self.minPlayer
                            flag = 0
                            self.expandedNodes += 1
                            if(self.checkWinner() == -1):
                                best_move = (row+l_row, col+l_col)
                                bestMove.append(best_move)
                                bestValue.append(self.winnerMinUtility)
                                gameBoards.append(self.board)
                                expandedNodes.append(self.expandedNodes)
                                return gameBoards, bestMove, expandedNodes, bestValue, -1   
                            if(isMinimaxDefensive):   # use minimax
                                temp_val = self.minimax(depth - 1, 3*row+col, not self.currPlayer)
                            else:
                                flag = 1
                                temp_val = self.alphabeta(depth-1, 3*row+col,alpha,beta,not self.currPlayer)
                            self.debug = 0
                            if(temp_val < best_val):
                                best_move = (row+l_row, col+l_col)
                                best_index = row*3+col
                            self.board[row+l_row][col+l_col] = '_'
                            best_val = min(temp_val,best_val)
                            if(flag == 1):
                                beta = min(beta,best_val)
                                if(beta <= alpha):
                                    break
                # print(best_val)
                self.cur_index = best_index
                bestMove.append(best_move)
                bestValue.append(best_val)
                gameBoards.append(self.board)
                self.board[best_move[0]][best_move[1]] = self.minPlayer
                expandedNodes.append(self.expandedNodes)
                self.expandedNodes = 0
                self.currPlayer = not self.currPlayer
        return gameBoards, bestMove, expandedNodes, bestValue, 0

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
       
        winnner : 1 for predefined and -1 for our own agent
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes = []
        winner=0
        start =randint(0,8)
        self.startBoardIdx = start
        temp = random.random()
        # print(temp)
        if(temp > 0.5):
            self.own_is_max = True
        else:
            self.own_is_max = False
        depth = self.maxDepth
        self.cur_index = self.startBoardIdx
        self.play_vs_own = True
        #determin which player go first
        temp = random.random()
        # print(temp)
        if(temp > 0.5):
            self.currPlayer = True
        else:
            self.currPlayer = False
        # maxFirst, both minimax
        # if (maxFirst and isMinimaxDefensive and isMinimaxDefensive)
        # flag = 0
        while (self.checkMovesLeft()):
        # for i in range(16):
        #     if(i == 7):
        #         self.debug = 1
            # print(self.cur_index)
            local_board_index = self.globalIdx[self.cur_index]
            l_row = local_board_index[0]
            l_col = local_board_index[1] 
            alpha = -1000000000000
            beta = 10000000000000
            if(self.currPlayer): # max player and max is offensive
                best_val = -1000000000000
                best_move = (-1,-1)
                best_index = -1
                # if(isMinimaxOffensive):   # use minimax
                result = self.checkWinner()
                # print(vertex)
                for row in range(3):
                    for col in range(3):
                        if self.board[row+l_row][col+l_col] == '_':
                            # temp_move = (vertex[0] + row, vertex[1] + col)
                            self.last_step = (row,col)
                            self.board[row+l_row][col+l_col] = self.maxPlayer
                            self.expandedNodes += 1
                            if(self.checkWinner() == 1):
                                best_move = (row+l_row, col+l_col)
                                bestMove.append(best_move)
                                bestValue.append(self.winnerMaxUtility)
                                expandedNodes.append(self.expandedNodes)
                                gameBoards.append(self.board)
                                if(self.own_is_max):                     #own agent win, set winner to -1
                                    return gameBoards, bestMove, expandedNodes,-1
                                else:                                    #predifined agent win, set winner to 1
                                    return gameBoards, bestMove, expandedNodes,1
                            temp_val = self.alphabeta(depth-1, 3*row+col,alpha,beta,not self.currPlayer)
                            self.board[row+l_row][col+l_col] = '_'
                            if(temp_val > best_val):
                                best_move = (row+l_row, col+l_col)
                                best_index = row*3+col
                            best_val = max(temp_val,best_val)
                            alpha = max(alpha,best_val)
                            if(beta <= alpha):
                                break
                # print(best_val)
                self.cur_index = best_index
                bestMove.append(best_move)
                gameBoards.append(self.board)
                self.board[best_move[0]][best_move[1]] = self.maxPlayer
                self.check_opp_win()
                expandedNodes.append(self.expandedNodes)
                # print(self.opp_ready_win_index)
                self.expandedNodes = 0
                self.currPlayer = not self.currPlayer
            else: # min player and max is defensive
                best_val = 1000000000000
                best_move = (-1,-1)
                best_index = -1
                # if(isMinimaxOffensive):   # use minimax
                result = self.checkWinner()
                # print(vertex)
                for row in range(3):
                    for col in range(3):
                        if self.board[row+l_row][col+l_col] == '_':
                            # temp_move = (vertex[0] + row, vertex[1] + col)
                            self.board[row+l_row][col+l_col] = self.minPlayer
                            self.last_step = (row,col)
                            self.expandedNodes += 1
                            if(self.checkWinner() == -1):
                                best_move = (row+l_row, col+l_col)
                                bestMove.append(best_move)
                                bestValue.append(self.winnerMinUtility)
                                expandedNodes.append(self.expandedNodes)
                                gameBoards.append(self.board)
                                if(self.own_is_max):                     #own agent win, set winner to -1
                                    return gameBoards, bestMove, expandedNodes,1
                                else:                                    #predifined agent win, set winner to 1
                                    return gameBoards, bestMove, expandedNodes,-1        
                            temp_val = self.alphabeta(depth-1, 3*row+col,alpha,beta,not self.currPlayer)
                            if(temp_val < best_val):
                                best_move = (row+l_row, col+l_col)
                                best_index = row*3+col
                            self.board[row+l_row][col+l_col] = '_'
                            best_val = min(temp_val,best_val)
                            beta = min(beta,best_val)
                            if(beta <= alpha):
                                break
                # print(best_val)
                self.cur_index = best_index
                bestMove.append(best_move)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.board[best_move[0]][best_move[1]] = self.minPlayer
                self.check_opp_win()
                self.expandedNodes = 0
                self.currPlayer = not self.currPlayer
        return gameBoards, bestMove, 0


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        flag = 0
        self.play_vs_own = True
        self.own_is_max = True
        print("our AI is Maxagent")
        print("Maxplayer go first? 1 for yes, 0 for no")
        max_first = input()
        max_first = int(max_first)
        if(max_first == 1):
            self.currPlayer = True
        else:
            self.currPlayer = False
        if(self.own_is_max != max_first):
            flag = 1
        depth = self.maxDepth
        self.cur_index = self.startBoardIdx
        while (self.checkMovesLeft()):
            local_board_index = self.globalIdx[self.cur_index]
            l_row = local_board_index[0]
            l_col = local_board_index[1] 
            alpha = -1000000000000
            beta = 10000000000000
            if(self.currPlayer): # max player and max is offensive
                best_val = -1000000000000
                best_move = (-1,-1)
                best_index = -1
                # if(isMinimaxOffensive):   # use minimax
                # print(vertex)
                for row in range(3):
                    for col in range(3):
                        if self.board[row+l_row][col+l_col] == '_':
                            # temp_move = (vertex[0] + row, vertex[1] + col)
                            self.last_step = (row,col)
                            self.board[row+l_row][col+l_col] = self.maxPlayer
                            self.expandedNodes += 1
                            if(self.checkWinner() == 1):
                                best_move = (row+l_row, col+l_col)
                                bestMove.append(best_move)
                                gameBoards.append(self.board)
                                                                 #predifined agent win, set winner to 1
                                return gameBoards, bestMove, 1
                            temp_val = self.alphabeta(depth-1, 3*row+col,alpha,beta,not self.currPlayer)
                            self.board[row+l_row][col+l_col] = '_'
                            if(temp_val > best_val):
                                best_move = (row+l_row, col+l_col)
                                best_index = row*3+col
                            best_val = max(temp_val,best_val)
                            alpha = max(alpha,best_val)
                            if(beta <= alpha):
                                break
                # print(best_val)
                self.cur_index = best_index
                bestMove.append(best_move)
                gameBoards.append(self.board)
                self.board[best_move[0]][best_move[1]] = self.maxPlayer
                self.check_opp_win()
                # print(self.opp_ready_win_index)
                self.currPlayer = not self.currPlayer
            else: # min player and max is defensive
                self.printGameBoard()
                if(flag == 1):
                    print("select a place in the board:")
                    print("eg: 0 2 means 0th raw, 2th colum in the global board")
                    x,y = input().split()
                    x = int(x)
                    y = int(y)
                    temp_r = x/3
                    temp_c = y/3
                    temp_id = 3*x+y
                    pivot = self.globalIdx[self.cur_index]
                    while(x < 0 or x > 8 or y <0 or y > 8):
                        print("invalid place")
                        print("select a place in the board:")
                        print("eg: 0 2 means 0th raw, 2th colum in the global board")
                        x,y = input().split()
                        x = int(x)
                        y = int(y)
                        temp_r = x/3
                        temp_c = y/3
                        temp_id = 3*x+y
                        pivot = self.globalIdx[self.cur_index]
                    flag = 0
                    self.board[x][y] = self.minPlayer
                    tempx = x %3
                    tempy = y % 3
                    self.cur_index = 3*tempx+tempy
                    self.currPlayer = not self.currPlayer
                    continue
                else:
                    print("select a place in the local board:",self.globalIdx[self.cur_index])
                    print("eg: 0 2 means 0th raw, 2th colum in the local board")
                    x,y = input().split()
                    x = int(x)
                    y = int(y)
                    temp_id = 3*x+y
                    pivot = self.globalIdx[self.cur_index]
                    while(temp_id < 0 or temp_id > 8):
                        print("invalid place")
                        print("select a place in the local board:",self.globalIdx[self.cur_index])
                        print("eg: 0 2 means 0th raw, 2th colum in the local board")
                        x,y = input().split()
                        x = int(x)
                        y = int(y)
                        temp_id = 3*x+y
                    self.board[pivot[0] + x][pivot[1] + y] = self.minPlayer
                    result = self.checkWinner()
                    if result == -1:
                        return gameBoards, bestMove, -1
                    self.cur_index = temp_id
                    self.currPlayer = not self.currPlayer
                    continue                  
        return gameBoards, bestMove, 0

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    uttt.printGameBoard()
    # gameBoards, bestMove, winner = uttt.playGameYourAgent()
    # gameBoards, bestMove, winner = uttt.playGameHuman()
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
