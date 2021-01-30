import zope.event
from enum import Enum 
from agents import Minimax_Agent_TicTacToe
import random
import time
import copy
class Squares(Enum):
    """Squares to fill the game state."""
    Cross = 1
    Circle = -1
    Empty = 0

class GameState:
    """ Game state that is a 3x3 tictactoe grid."""
    def __init__(self):
        self.state = [[Squares.Empty for i in range(3)]for j in range(3)]
        self._is_start_state = True
        
    # generate successor state given the action
    def set_position(self,pos,action):
        y = pos[0]
        x = pos[1]
        self.state[x][y] = action
        if (self._is_start_state):
            self._is_start_state = False
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
        y = pos[0]
        x = pos[1]
        # tile is empty
        if (self.state[x][y] == Squares.Empty):
            return True
        else:
            return False
    def print_state(self):
        for row in self.state:
            for col in row:
                print(col.value,end = " ")
            print()
    
    def is_start_state(self):
        return self._is_start_state
    
    def check_end_game(self):
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
    """TicTacToe specifies all the information including next player, winner, game state and display."""
    def __init__(self,display,player1,player2):
        self.state = GameState()
        self.turn = 0
        self.winner = ''
        self.display = display
        self.player1 = Squares.Empty
        self.player2 = Squares.Empty
        # initially empty, if there is no ai player, these will remain empty
        self.ai_1 = Squares.Empty
        self.ai_2 = Squares.Empty
        if (player1 == 'AI'):
            self.ai_1 = Squares.Cross
            self.player1 = self.ai_1
        elif(player1 == 'Human'):
            self.player1 = Squares.Cross
        if (player2 == 'AI'):
            self.ai_2 = Squares.Circle
            self.player2 = self.ai_2
        elif(player2 == 'Human'):
            self.player2 = Squares.Circle
        self.next_player = self.player1

        self.Agent = Minimax_Agent_TicTacToe(15)
        # winner line to draw a line from x1,y1 to x2,y2: (x1,y1,x2,y2)
        self.winner_line = (0,0,0,0)

    def run(self):
        while ( not self.is_ended()):
            # if ai_1's turn, play ai
            if (self.next_player == self.ai_1 != Squares.Empty):
                pos_player = self.ai_play(self.ai_1)
                print(pos_player)
                time.sleep(0.7)
                self.display.update(pos_player,self.winner_line)
            #if ai_2's turn, play ai
            elif(self.next_player == self.ai_2 != Squares.Empty):
                pos_player = self.ai_play(self.ai_2)
                print(pos_player)
                time.sleep(0.7)
                self.display.update(pos_player,self.winner_line)
            else:
                #if human player played:
                if (self.display.next_pos):
                    # if a legal move
                    if (self.state.legal(self.display.next_pos[0])):                        
                        pos_player = self.one_turn(self.display.next_pos[0])
                        self.display.update(pos_player,self.winner_line)
                    self.display.next_pos.clear()

    def one_turn(self,pos):
        '''
        Plays one turn of the current player, returns the current player
        Then calls 'check_end_game' method.
        '''
        if( not self.is_ended() ):

            current_player = self.next_player
            if (self.state.legal(pos)):
                self.turn+=1
                if(current_player == Squares.Cross):
                    self.state.set_position(pos,Squares.Cross)
                    self.next_player = Squares.Circle             
                else:
                    self.state.set_position(pos,Squares.Circle)
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

    def ai_play(self,agent):
        '''
        returns the best action of the selected agent.
        agent_index = 1 ::> max agent, i.e. should be Cross 
        agent_index = 0 ::> max agent, i.e. should be Circle 
        '''
        if (agent == Squares.Circle):
            agent_index = 0
        elif (agent == Squares.Cross):
            agent_index = 1
        return self.one_turn( self.Agent.get_best_action(self.state,0,agent_index)[1] )

    # def get_random_legal_pos(self):
    #     return random.choice(self.get_legal_actions())

    def is_ended(self):
        return (self.winner != '')

        
    