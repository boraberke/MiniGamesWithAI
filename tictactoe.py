CROSS=1
CIRCLE=2
EMPTY=0
#initialize the first player as cross
next_player = CROSS
class TicTacToe:
    def __init__(self):
        self.state = [[0 for i in range(3)]for j in range(3)]
        self.next_player = CROSS
        self.turn = 0
    '''
    return True if cross is the next player and add it to the array
    check if the state is an end state
    '''
    def one_round(self,x,y):
        if (self.legal(x,y)):
            if(self.next_player == CROSS):
                self.state[y][x] = CROSS
                self.next_player = CIRCLE
                return True
            else:
                self.state[y][x] = CIRCLE
                self.next_player = CROSS
                return False
            self.turn+=1
            print(self.turn)
    def legal(self,x,y):
        if (self.state[y][x] == 0):
            return True
        else:
            return False
    def print_state(self):
        for row in self.state:
            for col in row:
                print(col,end = " ")
            print()
        
    
    
