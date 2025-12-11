from turtle import Screen, Turtle
import time
import os
import random
from snake import Snake
from food import Food, BonusFood
from scoreboard import Scoreboard
from modes import ClassicMode, ObstacleMode

# Sound support
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

class Game:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=680, height=720)
        self.screen.bgcolor("black") # Start with black menu
        self.screen.title("Snake — Classic")
        self.screen.tracer(0)

        self.width = 680
        self.height = 720
        
        self.modes = {
            "Classic": ClassicMode(self.width, self.height),
            "Obstacle": ObstacleMode(self.width, self.height)
        }
        self.current_mode_name = "Classic"
        self.mode = self.modes[self.current_mode_name]

        self.snake = Snake()
        self.food = Food()
        self.bonus_food = BonusFood()
        self.scoreboard = Scoreboard()
        
        self.effect_pen = Turtle()
        self.effect_pen.hideturtle()
        self.effect_pen.penup()
        
        self.is_running = False
        self.is_paused = False
        self.is_game_over = False
        
        self.base_speed = 100
        self.speed_step = 4
        self.min_speed = 30
        self.speed_level = 0
        self.tick_ms = 20
        self.tick_accumulator = 0
        
        self.slow_motion_active = False
        
        # Level System
        self.level = 1
        self.foods_eaten = 0
        self.last_level_score = 0
        self.colors = ["white", "#3498db", "#e74c3c", "#9b59b6", "#f1c40f", "#2ecc71"] # White, Blue, Red, Purple, Yellow, Green
        
        # Particles
        self.particles = []
        
        # Sound
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(script_dir, "munch-sound-effect.mp3")
        if SOUND_AVAILABLE and os.path.exists(sound_path):
            self.munch_sound = pygame.mixer.Sound(sound_path)
        else:
            self.munch_sound = None

        self._bind_keys()
        
        self.menu_pen = Turtle()
        self.menu_pen.hideturtle()
        self.menu_pen.penup()
        
        self.hide_game_objects()
        self.show_menu()
        self.screen.onscreenclick(self.handle_click)

    def hide_game_objects(self):
        self.snake.hide() 
        self.food.goto(1000, 1000)
        self.bonus_food.hide()
        self.scoreboard.clear()
        if hasattr(self.mode, 'clear'):
            self.mode.clear()
        self.effect_pen.clear()
        # Clear particles
        for p in self.particles:
            p["t"].hideturtle()
            p["t"].clear()
        self.particles.clear()

    def _bind_keys(self):
        self.screen.listen()
        self.screen.onkey(self.snake.up, "Up")
        self.screen.onkey(self.snake.down, "Down")
        self.screen.onkey(self.snake.left, "Left")
        self.screen.onkey(self.snake.right, "Right")
        self.screen.onkey(self.toggle_pause, "p")
        self.screen.onkey(self.start_game, "space")

    def play_sound(self):
        if self.munch_sound:
            try:
                self.munch_sound.play()
            except:
                pass

    def set_mode(self, mode_name):
        if mode_name in self.modes:
            self.current_mode_name = mode_name
            self.mode = self.modes[mode_name]
            self.scoreboard.set_mode(mode_name)
            self.show_menu()

    def show_menu(self):
        if self.is_running:
            return
            
        self.screen.bgcolor("black")
        self.hide_game_objects()
        self.menu_pen.clear()
        self.is_game_over = False
        
        self.menu_pen.goto(0, 150)
        self.menu_pen.color("#2ecc71")
        self.menu_pen.write("SNAKE", align="center", font=("Courier", 80, "bold"))
        
        self.menu_pen.goto(0, 100)
        self.menu_pen.color("white")
        self.menu_pen.write("CLASSIC EDITION", align="center", font=("Courier", 20, "normal"))
        
        # Draw Mode Buttons
        modes = ["Classic", "Obstacle"]
        start_x = -100
        for m in modes:
            if m == self.current_mode_name:
                color = "#2ecc71"
                font_type = "bold"
            else:
                color = "#7f8c8d"
                font_type = "normal"
                
            self._draw_text_button(start_x, -50, m, color, font_type)
            start_x += 200
            
        self._draw_button(0, -150, "START GAME", "#2ecc71", "black", w=240, h=60)
        
        self.screen.update()

    def _draw_text_button(self, x, y, label, color, font_type):
        self.menu_pen.goto(x, y)
        self.menu_pen.color(color)
        self.menu_pen.write(label, align="center", font=("Courier", 16, font_type))
        if font_type == "bold":
            self.menu_pen.goto(x - 40, y - 5)
            self.menu_pen.pendown()
            self.menu_pen.forward(80)
            self.menu_pen.penup()

    def _draw_button(self, x, y, label, color, text_color, w=160, h=50):
        self.menu_pen.goto(x - w/2, y - h/2)
        self.menu_pen.pencolor(color)
        self.menu_pen.fillcolor(color)
            
        self.menu_pen.begin_fill()
        for _ in range(2):
            self.menu_pen.forward(w)
            self.menu_pen.left(90)
            self.menu_pen.forward(h)
            self.menu_pen.left(90)
        self.menu_pen.end_fill()
        
        self.menu_pen.goto(x, y - 12)
        self.menu_pen.color(text_color)
        self.menu_pen.write(label, align="center", font=("Courier", 20, "bold"))

    def handle_click(self, x, y):
        if self.is_running:
            return

        if self.is_game_over:
            if -100 <= x <= 100 and -50 <= y <= 10:
                self.start_game()
            elif -100 <= x <= 100 and -130 <= y <= -70:
                self.show_menu()
            elif -100 <= x <= 100 and -210 <= y <= -150:
                self.screen.bye()
            return

        if -120 <= x <= 120 and -180 <= y <= -120:
            self.start_game()
            return

        if -150 <= x <= -50 and -60 <= y <= -30:
            self.set_mode("Classic")
        elif 50 <= x <= 150 and -60 <= y <= -30:
            self.set_mode("Obstacle")

    def start_game(self):
        if self.is_running:
            return
            
        self.menu_pen.clear()
        self.screen.bgcolor("black")
        self.is_running = True
        self.is_paused = False
        self.is_game_over = False
        
        self.snake.reset()
        self.snake.set_color("white") # Reset color
        self.scoreboard.reset()
        self.speed_level = 0
        self.slow_motion_active = False
        
        self.level = 1
        self.foods_eaten = 0
        
        self.mode.setup()
        self.food.refresh(self.mode.obstacles)
        self.bonus_food.hide()
        
        self.tick_accumulator = 0
        self.screen.ontimer(self.game_loop, self.tick_ms)

    def toggle_pause(self):
        if not self.is_running:
            return
        self.is_paused = not self.is_paused

    def get_current_delay(self):
        base_delay = max(self.min_speed, self.base_speed - self.speed_level * self.speed_step)
        
        if self.slow_motion_active:
            return base_delay + 50
            
        return base_delay

    def level_up(self):
        self.level += 1
        
        # Regenerate obstacles if in Obstacle Mode
        if self.current_mode_name == "Obstacle" and hasattr(self.mode, 'generate_obstacles'):
            self.mode.generate_obstacles(self.level, self.snake.segments)
            # Refresh food position to ensure it's not inside a new obstacle
            self.food.refresh(self.mode.obstacles)
            # If bonus food is active, we might want to check it too, or just hide it to be safe/simple
            if self.bonus_food.is_active:
                self.bonus_food.hide()

        # Visual Feedback
        color_idx = (self.level - 1) % len(self.colors)
        new_color = self.colors[color_idx]
        self.snake.set_color(new_color)
        
        # Flash Level Up
        self.effect_pen.clear()
        self.effect_pen.goto(0, 0)
        self.effect_pen.color(new_color)
        self.effect_pen.write(f"LEVEL {self.level}", align="center", font=("Courier", 40, "bold"))
        self.screen.update()
        time.sleep(0.5)
        self.effect_pen.clear()

    def shake_screen(self):
        original = self.screen.bgcolor()
        self.screen.bgcolor("#2c3e50") # Dark Blue Grey
        self.screen.update()
        time.sleep(0.05)
        self.screen.bgcolor(original)

    def create_particles(self, x, y, color):
        for _ in range(8):
            p = Turtle("square")
            p.shapesize(0.3, 0.3)
            p.penup()
            p.goto(x, y)
            p.color(color)
            p.setheading(random.randint(0, 360))
            self.particles.append({"t": p, "life": 15, "speed": random.randint(5, 12)})

    def update_particles(self):
        for p in self.particles[:]:
            p["t"].forward(p["speed"])
            p["life"] -= 1
            if p["life"] <= 0:
                p["t"].hideturtle()
                p["t"].clear()
                self.particles.remove(p)

    def game_loop(self):
        if not self.is_running:
            return

        if self.is_paused:
            self.screen.update()
            self.screen.ontimer(self.game_loop, self.tick_ms)
            return

        if self.bonus_food.is_active:
            self.bonus_food.animate()
            if self.bonus_food.check_expiration():
                pass

        # Update particles every frame
        self.update_particles()

        self.tick_accumulator += self.tick_ms
        delay = self.get_current_delay()
        
        did_move = False
        if self.tick_accumulator >= delay:
            self.snake.move()
            self.tick_accumulator -= delay
            did_move = True
            self.screen.update()

        if did_move:
            if self.snake.head.distance(self.food) < 15:
                self.play_sound()
                self.shake_screen()
                self.create_particles(self.food.xcor(), self.food.ycor(), self.food.color()[0])
                
                self.food.refresh(self.mode.obstacles)
                self.snake.extend()
                
                # Score depends on level
                points = 1 * self.level
                self.scoreboard.increase_score(points)
                
                self.foods_eaten += 1
                self.speed_level += 1
                
                # Level Up Check
                if self.foods_eaten % 5 == 0:
                    self.level_up()
                
                if self.slow_motion_active:
                    self.slow_motion_active = False
                    self.effect_pen.clear()
                
                if self.foods_eaten % 5 == 0 and not self.bonus_food.is_active:
                    self.bonus_food.spawn(self.mode.obstacles)

            if self.bonus_food.is_active and self.snake.head.distance(self.bonus_food) < 15:
                self.play_sound()
                self.bonus_food.hide()
                self.create_particles(self.bonus_food.xcor(), self.bonus_food.ycor(), "gold")
                self.scoreboard.increase_score(5 * self.level)
                self.slow_motion_active = True
                
                self.effect_pen.clear()
                self.effect_pen.goto(0, 0)
                self.effect_pen.color("#f1c40f")
                self.effect_pen.write("SLOW MOTION!", align="center", font=("Courier", 30, "bold"))
                self.screen.update()
                time.sleep(0.5)
                self.effect_pen.clear()

            for segment in self.snake.segments[1:]:
                if self.snake.head.distance(segment) < 10:
                    self.game_over()
                    return

            if self.mode.check_collision(self.snake):
                self.game_over()
                return

        self.screen.update()
        self.screen.ontimer(self.game_loop, self.tick_ms)

    def game_over(self):
        self.is_running = False
        self.is_game_over = True
        self.scoreboard.game_over()
        
        for _ in range(3):
            for seg in self.snake.segments:
                seg.hideturtle()
            self.screen.update()
            time.sleep(0.2)
            for seg in self.snake.segments:
                seg.showturtle()
            self.screen.update()
            time.sleep(0.2)
            
        self.hide_game_objects()
        
        self.menu_pen.clear()
        
        self._draw_button(0, -20, "PLAY AGAIN", "#2ecc71", "black", w=200, h=60)
        self._draw_button(0, -100, "MENU", "#3498db", "black", w=200, h=60)
        self._draw_button(0, -180, "QUIT", "#e74c3c", "black", w=200, h=60)
        self.screen.update()
