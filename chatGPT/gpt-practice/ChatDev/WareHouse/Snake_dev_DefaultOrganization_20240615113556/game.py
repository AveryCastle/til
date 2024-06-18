'''
This file contains the Game class which manages the game logic and GUI.
'''
import tkinter as tk
from snake import Snake
from food import Food
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Practice")
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="black")
        self.canvas.pack()
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.canvas.bind_all("<KeyPress>", self.on_key_press)
        self.update()
    def on_key_press(self, event):
        self.snake.change_direction(event.keysym)
    def update(self):
        if self.snake.is_collision():
            self.game_over()
        else:
            self.snake.move()
            if self.snake.eat_food(self.food):
                self.food.spawn()
            self.canvas.after(100, self.update)
    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=("Arial", 20), anchor="center")