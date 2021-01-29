import tkinter as tk
root = tk.Tk()
canvas = tk.Canvas(root,width=500,height=500)
canvas.update()
canvas.configure(bg='black')
canvas.pack()
root.mainloop()