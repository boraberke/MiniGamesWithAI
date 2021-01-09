import zope.event
from enum import Enum 
import random
import time
class Squares(Enum):
    Cross = 1
    Circle = 2
    Empty = 0

class TicTacToe:

    def __init__(self,display,next_player):
        self.state = [[Squares.Empty for i in range(3)]for j in range(3)]
        self.next_player = next_player
        self.turn = 0
        self.winner = ''
        self.display = display
        self.AI = Squares.Circle
        # winner line to draw a line from x1,y1 to x2,y2: (x1,y1,x2,y2)
        self.winner_line = (0,0,0,0)

    def run(self):
        while ( not self.is_ended()):
            # if AI's turn, play ai
            if (self.next_player == self.AI):
                pos_player = self.ai_play()
                time.sleep(0.5)
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
            if (self.legal(pos)):
                self.turn+=1
                if(current_player == Squares.Cross):
                    self.state[y][x] = Squares.Cross
                    self.next_player = Squares.Circle             
                else:
                    self.state[y][x] = Squares.Circle
                    self.next_player = Squares.Cross
                self.check_end_game(current_player)  
                return (pos,current_player)
            # if not a legal move, return empty
            else:
                return ''
        # if game is over, return empty
        else:
            return ''

    def ai_play(self):
        return self.one_turn( self.get_random_legal_pos() )

    def get_random_legal_pos(self):
        empty_squares =[]
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if (self.state[j][i] == Squares.Empty):
                    empty_squares.append((i,j))
        return random.choice(empty_squares)
        

    def check_end_game(self,current_player):
        '''
        Check win and draw conditions:
        Cross Wins: three of the squares are marked with cross in a horizontal,vertical or diagonal row
        Circle Wins: three of the squares are marked with cross in a horizontal,vertical or diagonal row
        Draw: number of turns are 9 and no winners
        '''  
        #check vertical and horizontal
        for i in range(len(self.state)):
            # check vertically
            if (self.state[0][i] == self.state[1][i] == self.state[2][i] != Squares.Empty):
                self.winner = self.state[0][i]
                self.winner_line = (i,0,i,2)
                return
            # check horizontally
            if (self.state[i][0] == self.state[i][1] == self.state[i][2] != Squares.Empty):
                self.winner = self.state[i][0]
                self.winner_line = (0,i,2,i)
                return

        
        # check diagonals
        if (self.state[0][0] == self.state[1][1] == self.state[2][2] != Squares.Empty):
            self.winner = self.state[0][0]
            self.winner_line = (0,0,2,2)
            return
        if (self.state[2][0] == self.state[1][1] == self.state[0][2] != Squares.Empty):
            self.winner = self.state[2][0]
            self.winner_line = (2,0,0,2)
            return

        # check draw
        if (self.turn == 9):
            self.winner = 'draw'
            return

    def is_ended(self):
        return (self.winner != '')

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
        print(f"Game Status: {self.winner}")
        
    
    
