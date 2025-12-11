from turtle import Turtle

STARTING_POSITIONS = [(0,0), (-20,0), (-40,0)]
MOVE_DISTANCE = 20

class Snake:
    def __init__(self):
        self.body_color = "white"
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)
        self.head = self.segments[0]
        self._update_head_visual()
        self.can_turn = True

    def set_color(self, color):
        self.body_color = color
        for seg in self.segments:
            seg.color(color)
        # Keep head distinct? Maybe just slightly darker/lighter?
        # For now, uniform color is fine or we can update head separately.
        self._update_head_visual()

    def add_segment(self, position):
        # Revert to "square" for classic look as requested.
        new_segment = Turtle("square")
        new_segment.color(self.body_color)
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def _update_head_visual(self):
        # Make head distinct but keep classic square shape
        head = self.segments[0]
        head.color("#bdc3c7") # Light grey, subtle difference
        # No size change to keep grid alignment perfect
        # head.shapesize(stretch_wid=1.2, stretch_len=1.2)

    def hide(self):
        for seg in self.segments:
            seg.goto(1000, 1000)
            seg.hideturtle()
        self.segments.clear()

    def reset(self):
        self.hide()
        self.create_snake()
        self.head = self.segments[0]
        self.can_turn = True

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        
        self.head.forward(MOVE_DISTANCE)
        self.can_turn = True

    def up(self):
        if self.can_turn and self.head.heading() != 270:
            self.head.setheading(90)
            self.can_turn = False

    def down(self):
        if self.can_turn and self.head.heading() != 90:
            self.head.setheading(270)
            self.can_turn = False

    def left(self):
        if self.can_turn and self.head.heading() != 0:
            self.head.setheading(180)
            self.can_turn = False

    def right(self):
        if self.can_turn and self.head.heading() != 180:
            self.head.setheading(0)
            self.can_turn = False

    def extend(self):
        self.add_segment(self.segments[-1].position())
