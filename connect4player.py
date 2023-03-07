"""
This Connect Four player uses the minimax algorithm to find the optimal disc
placement according to the number of plies designated by difficulty_level.
********************************************************************************
********    This Connect4 player uses alpha-beta pruning, and can be    ********
********    can be turned on/off by changing the self.ab attribute to   ********
********                            to False.                           ******** 
********************************************************************************
"""
__author__ = "Seung Park"
__license__ = "University of Puget Sound"
__date__ = "February 20, 2023"

################################################################
######### IMPORTS
################################################################
import math
import numpy as np

class ComputerPlayer:
    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.id = id
        self.difficulty = difficulty_level
        self.ab = True

    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current chooses the optimal column to drop their
        disc according to the number of plies inputted.
        """
        
        # Rotate the tuple rack
        theRack = np.array([*rack])

        # run the minimax algorithm to retrieve the optimal column
        column= self.minimax(theRack, self.id, self.difficulty, -math.inf, math.inf, self.ab)[0]
        if theRack[column][-1] == 0:
            return column
           
    '''
    Minimax() takes itself, a Connect 4 Board, player, scores, difficulty,
    alpha, and beta as arguments. This function performs the minimax algorithm
    to find the best placement for the next disc. This function returns where
    to place the disc
    '''
    def minimax(self, rack, player, difficulty, alpha, beta, ab):
        
        # if the number of plies run out, either of the players win, or there
        # is a tie
        if difficulty == 0:
            return None, self.evaluateScore(rack, player)
        
        openLocations = self.findOpenColumn(rack)
        
        # AI
        if player == 2:
            value = -math.inf
            column = 0
            
            # check all valid playing locations for each column & get new score
            for col in openLocations:
                row = self.findNextOpenRow(rack, col)
                rackCopy = rack.copy()
                rackCopy[col][row] = 2
                newScore = self.minimax(rackCopy, 1, difficulty-1, alpha, beta, ab)[1]
                
                # if newScore is greater than the current score, then update
                if newScore > value:
                    value = newScore
                    column = col
                
                # if alpha-beta pruning is enabled
                if(ab):
                    alpha = max(alpha, value)
                    
                    # stop further searching
                    if alpha >= beta:
                        break
                
            return column, value
        
        # Human
        else:
            value = math.inf
            column = 0
            # check all valid playing locations for each column & get new score
            for col in openLocations:
                row = self.findNextOpenRow(rack, col)
                rackCopy = rack.copy()
                rackCopy[col][row] = 1
                newScore = self.minimax(rackCopy, 2, difficulty-1, alpha, beta, ab)[1]
                
                # if newScore is greater than the current score, then update
                if newScore < value:
                    value = newScore
                    column = col
                
                # if alpha-beta pruning is enabled
                if(ab):
                    beta = min(beta, value)
                    
                    # stop further searching
                    if alpha >= beta:
                        break
                
            return column, value

    '''
    This function takes a Connect 4 rack as input and returns the columns that
    are open for players to drop their discs
    '''
    def findOpenColumn(self, rack):
        height = len(rack)
        width = len(rack[0])
        validColumns = []
        
        for j in range(height):
            if rack[j][width-1] == 0:
                
                # append the indices of the columns that are still open
                validColumns.append(j)  
        return validColumns

    '''
    This function takes a Connect 4 rack and column as input and returns the
    next open row
    '''
    def findNextOpenRow(self, rack, column):
        width = len(rack[0])
        for row in range(width):
            if rack[column][row] == 0:
                return row
        
    '''
    This function takes a connect 4 rack, the column the piece is placed in, and
    the player as arguments & inspects every "quartet" that can be contained 
    within the rack and calculates the score of each player by these rules:
        - Point value is positive if it favors the AI, and negative if it favors its 
            opponent.
        - If it contains at least one disc of each color, it cannot be used to win. 
            It is worth 0.
        - If it contains 4 discs of the same color, it is worth ±∞ (since one player 
            has won).  
        - If it contains 3 discs of the same color (and 1 empty) it is worth ±100.
        - If it contains 2 discs of the same color (and 2 empties) it is worth ±10.
        - If it contains 1 disc (and 3 empties) it is worth ±1.
    '''
    def evaluateScore(self, rack, player):
        
        # gets the number of rows
        width = len(rack)
        # gets the number of columns
        height = len(rack[0])
        
        # keeps track of how many same-colored discs are found
        score = 0
        
        # # Horizontal Quartets
        for i in range(height-1):
            for j in range(width-4):
                quartet = []
                for k in range(j, j+3):
                    quartet.append(rack[i][k])
                score += self.checkQuartet(quartet, player)
        
        # Vertical Quartets
        for i in range(height-4):
            for j in range(width-1):
                quartet = []
                for k in range(i, i+3):
                    quartet.append(rack[k][j])
                score += self.checkQuartet(quartet, player)
        
        # Diagonal (Up-Right) Quartets
        arr = [[] for i in range(width + height - 1)]
        for i in range(height):
            for j in range(width):
                arr[i+j].append(rack[j][i])
        
        for i in range(3, len(arr)-3):
            for j in range(len(arr[i])-3):
                quartet = []
                for k in range(j, j+4):
                    quartet.append(arr[i][k])
                score += self.checkQuartet(quartet, player)

        # Diagonal (Down-Right) Quartets
        arr = [[] for i in range(width + height)]

        ind = 0
        for i in reversed(range(width+1)):
            arr[ind] = np.diag(rack, k=i)
            ind += 1
        w = width+1
        for i in range(1, height-1):
            arr[w] = np.diag(rack, k=-i)
            w += 1        

        for i in range(3, len(arr)-3):
            for j in range(len(arr[i])-3):
                quartet = []
                for k in range(j, j+4):
                    quartet.append(arr[i][k])
                score += self.checkQuartet(quartet, player)
        
        return score

    '''
    This function takes a quartet and the player and checks a quartet whether it 
    contains 4, 3, 2, 1, or 0 discs of that player:
        - Point value is positive if it favors the AI, and negative if it favors its 
            opponent.
        - If it contains at least one disc of each color, it cannot be used to win. 
            It is worth 0.
        - If it contains 4 discs of the same color, it is worth ±∞ (since one player 
            has won).  
        - If it contains 3 discs of the same color (and 1 empty) it is worth ±100.
        - If it contains 2 discs of the same color (and 2 empties) it is worth ±10.
        - If it contains 1 disc (and 3 empties) it is worth ±1.
    '''
    def checkQuartet(self, quartet, player):
        score = 0
        
        # human player
        if player == 1:
            if quartet.count(player) == 4:
                score = -math.inf
            elif quartet.count(player) == 3 and quartet.count(0) == 1:
                score -= 100
            elif quartet.count(player) == 2 and quartet.count(0) == 2:
                score -= 10
            elif quartet.count(player) == 1 and quartet.count(0) == 3:
                score -= 1
        # computer player
        else:
            if quartet.count(player) == 4:
                score = math.inf
            elif quartet.count(player) == 3 and quartet.count(0) == 1:
                score += 100
            elif quartet.count(player) == 2 and quartet.count(0) == 2:
                score += 10
            elif quartet.count(player) == 1 and quartet.count(0) == 3:
                score += 1
        
        return score