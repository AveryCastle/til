'''
This file contains the Food class which represents the food in the game.
'''
import tkinter as tk
import random
class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.spawn()
    def spawn(self):
        self.canvas.delete("food")
        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        self.position = (x, y)
        self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red", tags="food")