from turtle import Turtle
import os

import json

ALIGNMENT = "center"
FONT = ("Courier", 24, "bold")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_scores = self.load_high_scores()
        self.current_mode = "Classic"
        self.high_score = self.high_scores.get(self.current_mode, 0)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_scoreboard()

    def load_high_scores(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(script_dir, "data.txt")
            if os.path.exists(data_path):
                with open(data_path, "r") as data:
                    content = data.read()
                    # Try parsing as JSON
                    try:
                        result = json.loads(content)
                        if isinstance(result, dict):
                            return result
                        else:
                            # It's valid JSON but not a dict (likely the old int high score)
                            return {"Classic": int(result), "Obstacle": 0}
                    except json.JSONDecodeError:
                        # Fallback for legacy single integer format (if not valid JSON for some reason)
                        return {"Classic": int(content), "Obstacle": 0}
            return {"Classic": 0, "Obstacle": 0}
        except:
            return {"Classic": 0, "Obstacle": 0}

    def save_high_score(self):
        try:
            self.high_scores[self.current_mode] = self.high_score
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(script_dir, "data.txt")
            with open(data_path, "w") as data:
                json.dump(self.high_scores, data)
        except:
            pass

    def set_mode(self, mode_name):
        self.current_mode = mode_name
        self.high_score = self.high_scores.get(mode_name, 0)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def increase_score(self, amount=1):
        self.score += amount
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            self.goto(0, -40)
            self.write("NEW HIGH SCORE!", align=ALIGNMENT, font=("Courier", 20, "bold"))

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.goto(0, 260)  # Reset position to top
        self.update_scoreboard()