from turtle import Turtle
import random
import time
import math

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("red")
        self.shapesize(stretch_wid=0.6, stretch_len=0.6)
        self.speed("fastest")
        self.obstacles_list = []
        self.refresh()

    def refresh(self, obstacles=None):
        if obstacles is not None:
            self.obstacles_list = obstacles
        
        max_attempts = 50
        for _ in range(max_attempts):
            random_x = random.randint(-280, 280)
            random_y = random.randint(-280, 280)
            random_x = (random_x // 20) * 20
            random_y = (random_y // 20) * 20
            
            collision = False
            for obs in self.obstacles_list:
                # Increased buffer to 40 to prevent food spawning too close to walls
                if abs(obs.xcor() - random_x) < 40 and abs(obs.ycor() - random_y) < 40:
                    collision = True
                    break
            
            if not collision:
                self.goto(random_x, random_y)
                return
        
        self.goto(random_x, random_y)

class BonusFood(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("gold")
        self.shapesize(stretch_wid=0.8, stretch_len=0.8)
        self.speed("fastest")
        self.is_active = False
        self.obstacles_list = []
        self.spawn_time = 0
        self.pulse_phase = 0
        self.hideturtle()
    
    def spawn(self, obstacles=None):
        if obstacles is not None:
            self.obstacles_list = obstacles
        
        max_attempts = 50
        for _ in range(max_attempts):
            random_x = random.randint(-260, 260)
            random_y = random.randint(-260, 260)
            random_x = (random_x // 20) * 20
            random_y = (random_y // 20) * 20
            
            collision = False
            for obs in self.obstacles_list:
                # Increased buffer to 40 to prevent food spawning too close to walls
                if abs(obs.xcor() - random_x) < 40 and abs(obs.ycor() - random_y) < 40:
                    collision = True
                    break
            
            if not collision:
                self.goto(random_x, random_y)
                self.showturtle()
                self.is_active = True
                self.spawn_time = time.time()
                self.pulse_phase = 0
                return
        
        self.goto(random_x, random_y)
        self.showturtle()
        self.is_active = True
        self.spawn_time = time.time()
        self.pulse_phase = 0
    
    def hide(self):
        self.hideturtle()
        self.is_active = False
    
    def animate(self):
        if not self.is_active:
            return
        
        self.pulse_phase += 0.2
        size = 0.9 + 0.3 * math.sin(self.pulse_phase)
        self.shapesize(stretch_wid=size, stretch_len=size)
        
        # Flash effect
        if int(self.pulse_phase * 2) % 2 == 0:
            self.color("#FFFF00") # Yellow
        else:
            self.color("#FFD700") # Gold
    
    def check_expiration(self):
        if not self.is_active:
            return False
        
        elapsed = time.time() - self.spawn_time
        if elapsed >= 5.0:
            self.hide()
            return True
        return False
