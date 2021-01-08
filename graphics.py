import tkinter as tk
from tictactoe import TicTacToe
WIDTH =400
HEIGHT = WIDTH
OFFSET = WIDTH/25
game = TicTacToe()
def draw_xox_table(canvas,w,h,offset):
    canvas.create_line(w/3,offset,w/3,h-offset,width=2)
    canvas.create_line(2*w/3,offset,2*w/3,h-offset,width=2)
    canvas.create_line(offset,h/3,w-offset,h/3,width=2)
    canvas.create_line(offset,2*h/3,w-offset,2*h/3,width=2)
    canvas.configure(bg='gray')
def draw_next(canvas,x_pos,y_pos,w,h):
        if (game.one_round(x_pos,y_pos)):
            draw_cross(canvas,x_pos,y_pos,w,h)
        else:
            draw_circle(canvas,x_pos,y_pos,w,h)    
        game.print_state()


def draw_circle(canvas,x_pos,y_pos,w,h):
    # to put o in the center
    x_offset = w/12
    y_offset = h/12
    rectangle_width = w/3
    rectangle_height = h/3
    x_start = x_pos * rectangle_width + x_offset
    x_end = x_pos * rectangle_width + 3 * x_offset   
    y_start = y_pos * rectangle_height + y_offset
    y_end = y_pos * rectangle_height + 3 * y_offset 
    canvas.create_oval(x_start,y_start,x_end,y_end)
    
def draw_cross(canvas,x_pos,y_pos,w,h):
    # to put o in the center
    x_offset = w/12
    y_offset = h/12
    rectangle_width = w/3
    rectangle_height = h/3
    x_start = x_pos * rectangle_width + x_offset
    x_end = x_pos * rectangle_width + 3 * x_offset   
    y_start = y_pos * rectangle_height + y_offset
    y_end = y_pos * rectangle_height + 3 * y_offset 
    canvas.create_line(x_start,y_start,x_end,y_end,width=2)
    canvas.create_line(x_end,y_start,x_start,y_end,width=2)

def clicked_position(x,y,w,h):
    rectangle_width = w/3
    rectangle_height = h/3
    return  int(x/rectangle_width), int(y/rectangle_height)

def callback(event):
    print ("clicked at", event.x, event.y)
    x_pos,y_pos = clicked_position(event.x,event.y,WIDTH,HEIGHT)
    if(game.legal(x_pos,y_pos)):
        draw_next(canvas,x_pos,y_pos,WIDTH,HEIGHT)

root = tk.Tk()
canvas = tk.Canvas(root,width=WIDTH,height=HEIGHT)
canvas.update()
draw_xox_table(canvas,WIDTH,HEIGHT,OFFSET)
canvas.bind("<Button-1>", callback)
canvas.pack()


root.mainloop()

