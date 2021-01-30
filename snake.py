from enum import Enum 
import random
import queue
from pynput import keyboard
import time
from featureExtractors import SnakeSimpleExtractor as features
from collections import deque 

class Squares(Enum):
    """Squares to fill the game state."""
    Wall = '#'
    Snake = '@'
    Empty = ' '
    Food = '*'
    

class GameState:
    def __init__(self,width,height,snake_length,snake_facing):
        self.width = width
        self.height = height
        self.walls = []
        self.food = None
        self.state = self._state_with_borders()
        self.snake_facing = snake_facing
        self.snake_positions = self._initialize_snake_pos(snake_length)
        self.is_end = False
        
        self.add_random_food()
        self.score = 0
        self.empty_positions_to_update = deque()
    
    
    def next_state(self,action):
        '''
        returns a copy of the next state. Used for approximate q-learning.
        '''
        import copy
        state = copy.deepcopy(self)
        state.apply_action(action)
        state.move_snake()
        return state

    def get_walls(self):
        return self.walls

    def get_food(self):
        return self.food

    def get_snake(self):
        return self.snake_positions

    def get_snake_head(self):
        return self.snake_positions[-1]

    def add_random_food(self):
        empty_squares = self.get_empty_positions()
        pos = random.choice(empty_squares)
        self.update_state(pos,Squares.Food)
        self.food = pos
    def _initialize_snake_pos(self,snake_length):
        snake_positions = queue.deque()
        center_x,center_y = self._get_center_pos()
        # depending on where the snake is facing, enlarge the snake in the opposite way
        for i in range(snake_length):
            if (self.snake_facing == 'NORTH'):
                pos = (center_x,center_y+i) 
            elif(self.snake_facing == 'SOUTH'):
                pos =  (center_x,center_y-i) 
            elif(self.snake_facing == 'EAST'):
                pos = (center_x-i,center_y) 
            elif(self.snake_facing == 'WEST'):
                pos = (center_x+i,center_y) 
            # check if the position is a legal position (i.e. not a wall)
            if(self.is_legal_to_initialize(pos)):
                snake_positions.appendleft(pos)
                self.state[pos[1]][pos[0]] = Squares.Snake
            else:
                raise Exception('Illegal position of snake: {}'.format(pos))
        return snake_positions

    def _get_center_pos(self):
        return (self.width//2,self.height//2)
        
    def _state_with_borders(self):
        state = [[Squares.Empty for i in range(self.width)] for i in range(self.height)]
        for i in range(self.width):
            state[0][i] = Squares.Wall
            state[self.height-1][i] = Squares.Wall
            self.walls.extend( ((i,0),(i,self.height-1)) )
        for j in range(self.height):
            state[j][0] = Squares.Wall
            state[j][self.width-1] = Squares.Wall
            self.walls.extend( ((0,j),(self.width-1,j)) )
        return state

    def print_state(self):
        for row in self.state:
            for pos in row:
                print(pos.value,end=" ")
            print()

    def get_empty_positions(self):
        '''
        return squares that are empty.
        '''
        empty_positions = []
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                if (self.state[y][x] == Squares.Empty):
                    empty_positions.append((x,y))
        return empty_positions

    def is_legal_to_initialize(self,pos):
        '''
        checks if the tile is empty to place snake at initialization of the game.
        '''
        x,y = pos
        # tile is empty
        if (self.state[y][x] != Squares.Wall and self.state[y][x] != Squares.Snake):
            return True
        else:
            return False

    def get_legal_actions(self):
        if self.snake_facing == 'NORTH' or self.snake_facing == 'SOUTH':
            return [None,'WEST','EAST']
        else:
            return [None,'NORTH','SOUTH']
    
    def get_adjacent_positions(self):
        '''
        returns adjacent positions that snake can move.
        '''
        actions = self.get_legal_actions()
        positions = []
        move_pos = self.get_legal_move_positions()
        for action in actions:
            if action == None:
                if move_pos.get(self.snake_facing):
                    positions.append(move_pos.get(self.snake_facing))
            else:
                positions.append(move_pos.get(action))
        return positions

    def get_legal_move_positions(self):
        '''
        return action,move position pairs as a dict.
        '''
        x,y = self.get_snake_head()
        move_pos = {
            'NORTH': (x,y-1),
            'SOUTH': (x,y+1),
            'EAST': (x+1,y),
            'WEST': (x-1,y),
        }
        # check if the position is legal
        legal_move_pos = dict()
        for action,pos in move_pos.items():
            if self.is_legal_position(pos):
                legal_move_pos[action] = pos
        return legal_move_pos

    def is_legal_position(self,pos):
        if (pos[0] >= 0 and pos[1] >= 0 and pos[0]<self.width and pos[1]<self.height):
            return True
        else:
            return False
        
    def is_legal_action(self,action):
        if (self.snake_facing =='NORTH' or self.snake_facing =='SOUTH'):
            if (action=='WEST' or action =='EAST'):
                return True
        else:
            if (action=='NORTH' or action=='SOUTH'):
                return True
        return False

    def is_ended(self):
        return self.is_end
    
    def apply_action(self, action):
        '''
        Change the direction that snake is facing.
        '''
        if(self.is_legal_action(action)):
            self.snake_facing = action
    def next_snake_pos(self,head_pos):
        x = head_pos[0]
        y = head_pos[1]
        if (self.snake_facing == 'NORTH'):
            return (x,y-1) 
        elif(self.snake_facing == 'SOUTH'):
            return (x,y+1) 
        elif(self.snake_facing == 'EAST'):
            return (x+1,y) 
        elif(self.snake_facing == 'WEST'):
            return (x-1,y) 
    
    def get_reward(self):
        if self.check_end_game():
            return -100
        else:
            return self.reward
    def move_snake(self):
        '''
        move the snake and update the game state
        '''
        # get the head of the snake
        head = self.get_snake_head()
        next_pos = self.next_snake_pos(head)
        #move to the new location
        self.snake_positions.append(next_pos)
        # if there is a food in the next position, we let snake to grow by not shrinking from tail
        if (not self.is_food(next_pos)):
            #remove the tail
            tail = self.snake_positions.popleft()
            self.update_state(tail,Squares.Empty)
            self.empty_positions_to_update.append(tail)
            # change reward to 0 if no food is eaten
            self.reward = 0
        else:
            # set reward to 5 for food
            self.reward = 5
            self.add_random_food()
            self.score += 5
        # update the state if it is a legal move
        if (self.is_legal_to_initialize(next_pos)):
            self.update_state(next_pos,Squares.Snake)
    
    def check_end_game(self):
        '''
        check the following two conditions:
            snake eat itself: there are duplicates in the deque
            snake hits to wall: head of the snake hits to a wall
        '''
        # get the head of the snake
        head = self.get_snake_head()
        if (self.get_pos(head) == Squares.Wall):
            self.is_end = True
        else:
            count = 0
            for pos in self.snake_positions:
                if (pos == head):
                    count=count+1
            if (count==2):
                self.is_end = True
        return self.is_end

    def get_pos(self,pos):
        return self.state[pos[1]][pos[0]]

    def is_food(self,pos):
        if (self.state[pos[1]][pos[0]] == Squares.Food):
            return True
        else:
            return False

    def update_state(self,pos,square_type):
        self.state[pos[1]][pos[0]] = square_type
        
        

class SnakeGame():
    def __init__(self,display):
        self.state = GameState(11,11,3,'NORTH')
        self.player = 'Human'
        self.actionQueue = queue.Queue()
        self.listener = None
        self.display = display
        self.display.initialize(self.state)
        self.sleep_time = 0.2
        self.last_change_at = 0

    
    def check_keystrokes(self):
        if self.listener == None:
            self.listener = keyboard.Listener(on_press = self.add_actions)
            self.listener.start()
    
    def add_actions(self,key):
        try: 
            key = key.char
        except:
            key = key.name
        if (key == 'w'):
            self.actionQueue.put('NORTH')
        elif (key == 'a'):
            self.actionQueue.put('WEST')
        elif (key == 's'):
            self.actionQueue.put('SOUTH')
        elif (key == 'd'):
            self.actionQueue.put('EAST')

    
    def run(self):
        self.check_keystrokes()
        while (not self.state.is_ended()):
            if (not self.actionQueue.empty()):
                action = self.actionQueue.get()
                self.state.apply_action(action)
                print(features.get_features(self.state,action))
            else:
                print(features.get_features(self.state,None))
            self.state.move_snake()
            self.display.update(self.state)
            self.state.check_end_game()
            time.sleep(self.sleep_time)
            self.update_sleep_time()
            

    def update_sleep_time(self):
        if ( self.state.score % 15 == 0 and self.last_change_at != self.state.score and self.sleep_time >= 0.1):
            self.sleep_time-=0.02
            self.last_change_at = self.state.score    
            




if __name__ == "__main__":
    from graphics import SnakeTkinterDisplay,SnakeBasicDisplay
    from threading import Thread
    display = SnakeTkinterDisplay()
    snake = SnakeGame(display)
    control_thread = Thread(target=snake.run, daemon=True)
    control_thread.start()
    display.run_mainloop()

    # display2 = SnakeBasicDisplay()
    # snake = SnakeGame(display2)
    # snake.run()



