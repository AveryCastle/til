'''
This file contains the Snake class which represents the snake in the game.
'''
import tkinter as tk
class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.next_direction = "Right"
    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "Up":
            new_head = (head_x, head_y - 10)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 10)
        elif self.direction == "Left":
            new_head = (head_x - 10, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 10, head_y)
        self.body.insert(0, new_head)
        self.canvas.create_rectangle(new_head[0], new_head[1], new_head[0] + 10, new_head[1] + 10, fill="white")
        self.canvas.create_rectangle(self.body[-1][0], self.body[-1][1], self.body[-1][0] + 10, self.body[-1][1] + 10, fill="black")
        self.body.pop()
    def change_direction(self, new_direction):
        if new_direction in ["Up", "Down", "Left", "Right"]:
            if new_direction != self.next_direction:
                self.next_direction = new_direction
    def eat_food(self, food):
        head_x, head_y = self.body[0]
        if (head_x, head_y) == food.position:
            self.body.append((0, 0))
            return True
        return False
    def is_collision(self):
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400 or (head_x, head_y) in self.body[1:]