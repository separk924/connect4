"""
This Connect Four player just picks a random spot to play. It's pretty dumb.
"""
__author__ = "Seung Park"
__license__ = "University of Puget Sound"
__date__ = "February 20, 2023"

import random
import time
import math

class ComputerPlayer:
    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.id = id
        self.difficulty = difficulty_level

    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current just pauses for half a second (for 
        effect), and then chooses a random valid move.
        """
        
        time.sleep(0.5) # pause purely for effect--real AIs shouldn't do this
        while True:
            play = random.randrange(0, len(rack))
            if rack[play][-1] == 0: return play
            
    def minimax(self, rack, currentDepth, maxPlayer, scores):
        
        isTerminal = self.isTerminalNode(rack)
        openLocations = self.findOpen(rack)
        if currentDepth == 0 or isTerminal:
            return 
        
        if(maxPlayer):
            value = -math.inf
            
            # for columns in openLocations:
        
            return max(self.minimax(rack, currentDepth-1, False, scores))
        
        else:
            value = math.inf
            
            # for columns in openLocations:
            
            return max(self.minimax(rack, currentDepth-1, True, scores))
            
            
        
        
    '''
    This function takes a Connect 4 rack and player ID as input and returns whether
    the last move ends the game or not
    '''
    def isTerminalNode(rack, player):
        
        return False
    
    '''
    This function takes a Connect 4 rack as input and returns the columns that
    are open for players to drop their discs
    '''
    def findOpen(rack):
        height = len(rack)
        validColumns = []
        for j in len(rack[0]):
            if rack[height-1][j] == 0:
                  validColumns.append(j)  
        return validColumns
    
    
    def evaluation(rack):
        
        pass
    
    