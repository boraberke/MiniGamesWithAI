
#initialize the first player as cross
from enum import Enum 
class Squares(Enum):
    Cross = 1
    Circle = 2
    Empty = 0

class TicTacToe:

    def __init__(self):
        self.state = [[Squares.Empty for i in range(3)]for j in range(3)]
        self.next_player = Squares.Cross
        self.turn = 0
        self.gameStatus = 'play'
    '''
    Plays one turn of the current player, returns the current player
    Then calls 'check_end_game' method.
    '''
    def one_turn(self,x,y):
        current_player = self.next_player
        if (self.legal(x,y)):
            self.turn+=1
            print(self.turn)
            if(current_player == Squares.Cross):
                self.state[y][x] = Squares.Cross
                self.next_player = Squares.Circle             
            else:
                self.state[y][x] = Squares.Circle
                self.next_player = Squares.Cross
            self.check_end_game(current_player)  
        return current_player
    '''
    Check win and draw conditions:
        Cross Wins: three of the squares are marked with cross in a horizontal,vertical or diagonal row
        Circle Wins: three of the squares are marked with cross in a horizontal,vertical or diagonal row
        Draw: number of turns are 9 and no winners
    '''        
    def check_end_game(self,current_player):
        #check horizontally
        sum_of_line = 0
        for row in self.state:
            for col in row:
                # only current_player can win, if there is any other square that is not current_player, then there is no winning condition
                if(col == current_player):
                    sum_of_line += 1
                else:
                    sum_of_line = 0
                    break   
                # if sum is 3, current_player wins
                if(sum_of_line==3):
                    self.gameStatus=current_player      


                
        #check vertically
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                # empty square means no winning condition
                if(self.state[j][i] == current_player):
                    sum_of_line += 1
                else:
                    sum_of_line = 0
                    break
                # if sum is 3, current_player wins
                if(sum_of_line==3):
                    self.gameStatus=current_player


        #check for one diagonal
        for i in range(len(self.state)):
                # empty square means no winning condition
                if(self.state[i][i] == current_player):
                    sum_of_line += 1
                else:
                    sum_of_line = 0
                    break
                # if sum is 3, current_player wins
                if(sum_of_line==3):
                    self.gameStatus=current_player

        #check for the other diagonal
        for i in range(len(self.state)):
                # empty square means no winning condition
                if(self.state[i][len(self.state)-1-i] == current_player):
                    sum_of_line += 1
                else:
                    sum_of_line = 0
                    break
                # if sum is 3, current_player wins
                if(sum_of_line==3):
                    self.gameStatus=current_player

    def legal(self,x,y):
        # tile is empty
        if (self.state[y][x] == Squares.Empty):
            return True
        else:
            return False
    def print_state(self):
        for row in self.state:
            for col in row:
                print(col.value,end = " ")
            print()
        print(f"Game Status: {self.gameStatus}")
        
    
    
