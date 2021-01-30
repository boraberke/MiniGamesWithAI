# graphics.py

import tkinter as tk
from tictactoe import TicTacToe
from tictactoe import Squares

class TicTacToeTable:
    """Graphics of TicTacToe"""
    def __init__(self):
        #Constants to draw 
        self.WIDTH =500
        self.HEIGHT = self.WIDTH
        self.OFFSET = self.WIDTH/25
        self.x_offset = self.WIDTH/12
        self.y_offset = self.HEIGHT/12
        self.rectangle_width = self.WIDTH/3
        self.rectangle_height = self.HEIGHT/3
        self.next_pos = []
        #screen and canvas
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,width=self.WIDTH,height=self.HEIGHT)
        self._initialize_canvas()
        
        
    def _initialize_canvas(self):
        self.canvas.update()
        self._draw_xox_table(2,'white')
        self.canvas.configure(bg='black')
        self.canvas.bind("<Button-1>", self._callback)
        self.canvas.pack()
    
    def run_mainloop(self):
        self.root.mainloop()
    def _draw_xox_table(self,line_width,line_color):
        w = self.WIDTH 
        h = self.HEIGHT
        offset = self.OFFSET
        self.canvas.create_line(w/3,offset,w/3,h-offset,width=line_width,fill=line_color)
        self.canvas.create_line(2*w/3,offset,2*w/3,h-offset,width=line_width,fill=line_color)
        self.canvas.create_line(offset,h/3,w-offset,h/3,width=line_width,fill=line_color)
        self.canvas.create_line(offset,2*h/3,w-offset,2*h/3,width=line_width,fill=line_color)

    def _draw_next(self,position,player):
            if (player == Squares.Cross):
                self._draw_cross(position)
            elif (player == Squares.Circle):
                self._draw_circle(position)

    def _draw_winner_line(self,positions):
        x_start = positions[0] * self.rectangle_width + self.rectangle_width / 2
        x_end = positions[2] * self.rectangle_width + self.rectangle_width / 2
        y_start = positions[1] * self.rectangle_height + self.rectangle_width / 2
        y_end = positions[3] * self.rectangle_height + self.rectangle_width / 2
        self.canvas.create_line(x_start,y_start,x_end,y_end,width=5,fill='red')
    
    def _draw_circle(self,position):
        self.canvas.create_oval(self.__cross_circle_positions(position),width=4,fill='red',outline='green')
        
    def _draw_cross(self,position):
        x1,y1,x2,y2 = self.__cross_circle_positions(position)
        self.canvas.create_line(x1,y1,x2,y2,width=4,fill='green')
        self.canvas.create_line(x1,y2,x2,y1,width=4,fill='green')

    def __cross_circle_positions(self,position):
        # to put cross and circles at the center of the squares
        x_pos = position[0]
        y_pos = position[1]
        x_start = x_pos * self.rectangle_width + self.x_offset
        x_end = x_pos * self.rectangle_width + 3 * self.x_offset   
        y_start = y_pos * self.rectangle_height + self.y_offset
        y_end = y_pos * self.rectangle_height + 3 * self.y_offset 
        return (x_start,y_start,x_end,y_end)

    def _clicked_position(self,x,y):
        return  (int(x/self.rectangle_width), int(y/self.rectangle_height))

    def _callback(self,event):
        # get the square which is clicked as position i.e (x,y)
        position = self._clicked_position(event.x,event.y)
        # add the position to the next_pos list
        if not self.next_pos:            
            self.next_pos.append(position)  

    def update(self,pos_player,winner_line_pos):
        self._draw_next(pos_player[0],pos_player[1])
        if (winner_line_pos != ''):
            self._draw_winner_line(winner_line_pos)

class SnakeBasicDisplay:
    '''
    allows you to play it on console, printing the state to the console.
    '''
    def initialize(self,state):
        state.print_state()
    def update(self,state):
        state.print_state()


class SnakeTkinterDisplay:
    def initialize(self,state):
        MAX_SIZE = 500
        # get number of squares in the state
        self.square_counts = (state.width,state.height)
        self.width_height_rate = self.square_counts[0]/self.square_counts[1]
        if ( self.width_height_rate > 1 ):
            self.width = MAX_SIZE
            self.height = round(MAX_SIZE / self.width_height_rate)
        elif ( self.width_height_rate < 1 ):
            self.height = MAX_SIZE
            self.width = round(MAX_SIZE * self.width_height_rate)
        else:
            self.height = MAX_SIZE
            self.width = MAX_SIZE
        self.rectangle_width = self.width // self.square_counts[0]
        self.rectangle_height = self.height // self.square_counts[1]
        self.offset = max(self.rectangle_width / 8,self.rectangle_height / 8)
        #screen and canvas
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,width=self.width,height=self.height)
        self._initialize_canvas(state)
        
        
    def _initialize_canvas(self,game_state):
        state = game_state.state
        self.canvas.update()
        for y in range(len(state)):
            for x in range(len(state[y])):
                self._draw_rect((x,y),state[y][x])
        self.canvas.configure(bg='black')
        self.canvas.pack()

    def run_mainloop(self):
        self.root.mainloop()

    def update(self,game_state):
        import copy
        from snake import Squares as s
        # draw the removed tail
        if ( not game_state.empty_positions_to_update.empty()):
            empty_pos = game_state.empty_positions_to_update.get()
            self._draw_rect(empty_pos,s.Empty)
        snake_positions = copy.deepcopy(game_state.snake_positions)
        head_pos = snake_positions.pop()
        # draw new head position
        self._draw_rect(head_pos,s.Snake)
        # draw the food position
        self._draw_rect(game_state.food_position,s.Food)

    def get_canvas_coordinates(self,coordinates):
        x = coordinates[0]
        y = coordinates[1]
        return (self.rectangle_height * x,self.rectangle_width * y)
    
    
    def _draw_rect(self,coordinates,square_type):
        coordinates = self.get_canvas_coordinates(coordinates)
        from snake import Squares as s
        square_type = square_type.value
        x1 = coordinates[0]
        y1 = coordinates[1]
        x2 = x1 + self.rectangle_width
        y2 = y1 + self.rectangle_height
        offset = self.offset
        if ( square_type == s.Snake.value ):
            self.canvas.create_rectangle(x1+offset,y1+offset,x2-offset,y2-offset,fill='white')
        elif ( square_type == s.Wall.value ):
            self.canvas.create_rectangle(x1,y1,x2,y2,fill='orange')
        elif ( square_type == s.Food.value ):
            self.canvas.create_oval(x1+offset,y1+offset,x2-offset,y2-offset,fill='red')
        else:
            self.canvas.create_rectangle(x1,y1,x2,y2,fill='black')



