from turtle import Turtle
import random

class GameMode:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []

    def setup(self):
        """Setup the stage (walls, obstacles)."""
        pass

    def check_collision(self, snake):
        """Check for collisions specific to the mode."""
        pass

    def clear(self):
        """Clear obstacles."""
        for obs in self.obstacles:
            obs.hideturtle()
            obs.clear()
            obs.goto(1000, 1000)
        self.obstacles.clear()
        
    def _add_obstacle(self, x, y, color="#8B4513"):
        obs = Turtle("square")
        obs.penup()
        obs.color(color) # Allow custom color
        obs.goto(x, y)
        self.obstacles.append(obs)
        
    def _create_wall_segment(self, c1, c2, c3, horizontal=True, color="#8B4513"):
        if horizontal:
            for x in range(c1, c2, 20):
                self._add_obstacle(x, c3, color)
        else:
            for y in range(c2, c3, 20):
                self._add_obstacle(c1, y, color)

class ClassicMode(GameMode):
    def setup(self):
        self.clear()
        # "Classic Walls" - Long, uniform grey walls at the edges
        # Edges are at +/- 340 (Screen 680). Walls at +/- 340 (Overlapping edge).
        # Length: Block most of the edge (540px), leaving ~70px open at corners.
        # Grid Alignment: Must be multiples of 20.
        # Range: -260 to 280 (exclusive) gives -260...260 (inclusive).
        
        wall_color = "#7f8c8d" # Concrete Grey
        
        # Top Edge (y=340)
        self._create_wall_segment(-260, 280, 340, True, wall_color)
        
        # Bottom Edge (y=-340)
        self._create_wall_segment(-260, 280, -340, True, wall_color)
        
        # Left Edge (x=-320)
        self._create_wall_segment(-320, -260, 280, False, wall_color) # x=-320, y from -260 to 280
        
        # Right Edge (x=320)
        self._create_wall_segment(320, -260, 280, False, wall_color) # x=320, y from -260 to 280

    def check_collision(self, snake):
        head = snake.head
        
        # Check obstacle collision first
        for obs in self.obstacles:
            if head.distance(obs) < 20:
                return True
        
        # Wrap around logic (teleport)
        limit_x = 330 # Window edge
        limit_y = 330
        
        if head.xcor() > limit_x:
            head.setx(-limit_x)
        elif head.xcor() < -limit_x:
            head.setx(limit_x)
            
        if head.ycor() > limit_y:
            head.sety(-limit_y)
        elif head.ycor() < -limit_y:
            head.sety(limit_y)
            
        return False

class ObstacleMode(GameMode):
    def setup(self):
        # Initial setup uses level 1 layout
        self.generate_obstacles(1, [])

    def generate_obstacles(self, level, snake_segments):
        self.clear()
        
        # Store segments for collision checking in _add_obstacle
        self.safe_segments = snake_segments
        
        layout_type = level % 4
        
        if layout_type == 1:
            # Level 1, 5, 9...: The Classic Box (current default)
            self._create_wall_segment(-200, -40, 200, True)
            self._create_wall_segment(40, 220, 200, True)
            self._create_wall_segment(-200, -40, -200, True)
            self._create_wall_segment(40, 220, -200, True)
            self._create_wall_segment(-200, -200, -40, False)
            self._create_wall_segment(-200, 40, 220, False)
            self._create_wall_segment(200, -200, -40, False)
            self._create_wall_segment(200, 40, 220, False)
            
        elif layout_type == 2:
            # Level 2, 6, 10...: The Cross
            # Horizontal bar
            self._create_wall_segment(-140, 160, 0, True)
            # Vertical bar
            self._create_wall_segment(0, -140, 160, False)
            
        elif layout_type == 3:
            # Level 3, 7, 11...: Four Pillars
            self._add_obstacle(-140, 140)
            self._add_obstacle(140, 140)
            self._add_obstacle(-140, -140)
            self._add_obstacle(140, -140)
            
            # Add some surrounding blocks to make them pillars
            for x in [-140, 140]:
                for y in [-140, 140]:
                    self._add_obstacle(x+20, y)
                    self._add_obstacle(x-20, y)
                    self._add_obstacle(x, y+20)
                    self._add_obstacle(x, y-20)

        else: # layout_type == 0
            # Level 4, 8, 12...: Random Scattered Blocks
            for _ in range(20):
                rx = random.randint(-14, 14) * 20
                ry = random.randint(-14, 14) * 20
                self._add_obstacle(rx, ry)
                
        # Clear safe segments after generation
        self.safe_segments = None

    def _add_obstacle(self, x, y, color="#8B4513"):
        # Check if this position collides with the snake
        if hasattr(self, 'safe_segments') and self.safe_segments:
            for seg in self.safe_segments:
                # 20 is block size, use slightly larger to be safe
                if seg.distance(x, y) < 25: 
                    return # Do not spawn obstacle here
        
        super()._add_obstacle(x, y, color)

    def check_collision(self, snake):
        head = snake.head
        # Window edge is 330
        limit = 330 
        if head.xcor() > limit or head.xcor() < -limit or head.ycor() > limit or head.ycor() < -limit:
            return True
            
        # Check obstacle collision
        for obs in self.obstacles:
            if head.distance(obs) < 20:
                return True
        return False
