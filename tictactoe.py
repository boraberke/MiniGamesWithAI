
#initialize the first player as cross
from enum import Enum 
class Squares(Enum):
    Cross = 1
    Circle = 2
    Empty = 0

class TicTacToe:

    def __init__(self,next_player):
        self.state = [[Squares.Empty for i in range(3)]for j in range(3)]
        self.next_player = next_player
        self.turn = 0
        self.winner = ''
        self.winner_line = (0,0,0,0)

    def one_turn(self,pos):
        '''
        Plays one turn of the current player, returns the current player
        Then calls 'check_end_game' method.
        '''
        x = pos[0]
        y = pos[1]
        current_player = self.next_player
        if (self.legal(pos)):
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
            # check horizontally
            if (self.state[i][0] == self.state[i][1] == self.state[i][2] != Squares.Empty):
                self.winner = self.state[i][0]
                self.winner_line = (0,i,2,i)

        
        # check diagonals
        if (self.state[0][0] == self.state[1][1] == self.state[2][2] != Squares.Empty):
            self.winner = self.state[0][0]
            self.winner_line = (0,0,2,2)
        if (self.state[2][0] == self.state[1][1] == self.state[0][2] != Squares.Empty):
            self.winner = self.state[2][0]
            self.winner_line = (2,0,0,2)

        # check draw
        if (self.turn == 9):
            self.winner = 'draw'
    
    # def check_end_game(self,current_player):
    #     '''
    #     Check win and draw conditions:
    #     Cross Wins: three of the squares are marked with cross in a horizontal,vertical or diagonal row
    #     Circle Wins: three of the squares are marked with cross in a horizontal,vertical or diagonal row
    #     Draw: number of turns are 9 and no winners
    #     ''' 
    #     #check draw 
    #     if(self.turn == 9):
    #         self.gameStatus='draw'
    #         return self.gameStatus   
    #     #check horizontally
    #     sum_of_line = 0
    #     for row in self.state:
    #         for col in row:
    #             # only current_player can win, if there is any other square that is not current_player, then there is no winning condition
    #             if(col == current_player):
    #                 sum_of_line += 1
    #             else:
    #                 sum_of_line = 0
    #                 break   
    #             # if sum is 3, current_player wins
    #             if(sum_of_line==3):
    #                 self.gameStatus = current_player 
    #                 return self.gameStatus     
   
    #     #check vertically
    #     for i in range(len(self.state)):
    #         for j in range(len(self.state[i])):
    #             # empty square means no winning condition
    #             if(self.state[j][i] == current_player):
    #                 sum_of_line += 1
    #             else:
    #                 sum_of_line = 0
    #                 break
    #             # if sum is 3, current_player wins
    #             if(sum_of_line==3):
    #                 self.gameStatus=current_player
    #                 return self.gameStatus   


    #     #check for one diagonal
    #     for i in range(len(self.state)):
    #             # empty square means no winning condition
    #             if(self.state[i][i] == current_player):
    #                 sum_of_line += 1
    #             else:
    #                 sum_of_line = 0
    #                 break
    #             # if sum is 3, current_player wins
    #             if(sum_of_line==3):
    #                 self.gameStatus=current_player
    #                 return self.gameStatus   

    #     #check for the other diagonal
    #     for i in range(len(self.state)):
    #             # empty square means no winning condition
    #             if(self.state[i][len(self.state)-1-i] == current_player):
    #                 sum_of_line += 1
    #             else:
    #                 sum_of_line = 0
    #                 break
    #             # if sum is 3, current_player wins
    #             if(sum_of_line==3):
    #                 self.gameStatus=current_player
    #                 return self.gameStatus 


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
        
    
    
