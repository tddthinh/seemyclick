import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=100, bg='lightgray')
canvas.pack(pady=10)

# 1. Create a shape (e.g., a circle) *before* the rectangle
canvas.create_oval(50, 20, 150, 80, fill='blue', tags="behind")

# 2. Create the rectangle with NO fill color
# The interior will be transparent, showing the blue circle underneath
canvas.create_rectangle(70, 40, 130, 60, outline='red', width=3, fill='', tags="transparent_rect") 

root.mainloop()