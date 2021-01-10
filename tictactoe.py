import zope.event
from enum import Enum 
from agents import Minimax_Agent
import random
import time
import copy
class Squares(Enum):
    Cross = 1
    Circle = -1
    Empty = 0

class GameState:
    def __init__(self):
        self.state = [[Squares.Empty for i in range(3)]for j in range(3)]
        
    # generate successor state given the action
    def set_position(self,x,y,action):
        self.state[y][x] = action
    def generate_successor_state(self,agent_index,action):
        game_state = copy.deepcopy(self)
        if (agent_index == 1):
            game_state.state[action[1]][action[0]] = Squares.Cross
        else:
            game_state.state[action[1]][action[0]] = Squares.Circle
        return game_state
    def get_legal_actions(self):
        empty_squares =[]
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if (self.state[j][i] == Squares.Empty):
                    empty_squares.append((i,j))
        return empty_squares
    def legal(self,pos):
        # tile is empty
        if (self.state[pos[1]][pos[0]] == Squares.Empty):
            return True
        else:
            return False
    def print_state(self):
        for row in self.state:
            for col in row:
                print(col.value,end = " ")
            print()
    
    def check_end_game(self):
        '''
        Check win and draw conditions:
        Cross Wins: three of the squares are marked with cross in a horizontal,vertical or diagonal row
        Circle Wins: three of the squares are marked with cross in a horizontal,vertical or diagonal row
        Draw: number of turns are 9 and no winners
        '''
        state = self
        #check vertical and horizontal
        for i in range(len(self.state)):
            # check vertically
            if (self.state[0][i] == self.state[1][i] == self.state[2][i] != Squares.Empty):
                winner = self.state[0][i]
                winner_line = (i,0,i,2)
                return winner,winner_line
            # check horizontally
            if (self.state[i][0] == self.state[i][1] == self.state[i][2] != Squares.Empty):
                winner  = self.state[i][0]
                winner_line = (0,i,2,i)
                return winner,winner_line

        
        # check diagonals
        if (self.state[0][0] == self.state[1][1] == self.state[2][2] != Squares.Empty):
            winner = self.state[0][0]
            winner_line = (0,0,2,2)
            return winner,winner_line
        if (self.state[2][0] == self.state[1][1] == self.state[0][2] != Squares.Empty):
            winner = self.state[2][0]
            winner_line = (2,0,0,2)
            return winner,winner_line


        # check draw
        for row in self.state:
            for col in row:
                if (col == Squares.Empty):
                    return '',(0,0,0,0)
        winner = Squares.Empty
        winner_line = (0,0,0,0)
        return winner,winner_line
        
           

class TicTacToe:

    def __init__(self,display,next_player):
        self.state = GameState()
        self.next_player = next_player
        self.turn = 0
        self.winner = ''
        self.display = display
        self.AI = Squares.Cross
        self.Agent = Minimax_Agent(1500)
        # winner line to draw a line from x1,y1 to x2,y2: (x1,y1,x2,y2)
        self.winner_line = (0,0,0,0)

    def run(self):
        while ( not self.is_ended()):
            # if AI's turn, play ai
            if (self.next_player == self.AI):
                pos_player = self.ai_play()
                self.display.update(pos_player,self.winner_line)
                print(pos_player)
            else:
                #if human player played:
                if self.display.next_pos:
                    pos_player = self.one_turn(self.display.next_pos[0])
                    self.display.update(pos_player,self.winner_line)
                    self.display.next_pos.clear()

    def one_turn(self,pos):
        '''
        Plays one turn of the current player, returns the current player
        Then calls 'check_end_game' method.
        '''
        if( not self.is_ended() ):
            x = pos[0]
            y = pos[1]
            current_player = self.next_player
            if (self.state.legal(pos)):
                self.turn+=1
                if(current_player == Squares.Cross):
                    self.state.set_position(x,y,Squares.Cross)
                    self.next_player = Squares.Circle             
                else:
                    self.state.set_position(x,y,Squares.Circle)
                    self.next_player = Squares.Cross
                self.winner,self.winner_line = self.state.check_end_game()  
                self.state.print_state()
                return (pos,current_player)
            # if not a legal move, return empty
            else:
                return ''
        # if game is over, return empty
        else:
            return ''

    def ai_play(self):
        return self.one_turn( self.Agent.get_best_action(self.state,0,1)[1] )

    # def get_random_legal_pos(self):
    #     return random.choice(self.get_legal_actions())

    def is_ended(self):
        return (self.winner != '')

        
    
    
