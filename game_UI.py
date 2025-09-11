from turtle import Turtle
from collections import defaultdict
from constants import Settings

COLORS = ["red", "orange", "yellow", "green", "blue"]
FONT = ("Helvetica", 16, "normal")

class GUI(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.blocks = defaultdict(list)

    def create_rows(self, colors, start_x, start_y, row_spacing=25):
        for i, color in enumerate(colors):
            y = start_y - (i * row_spacing)  # each row lower by spacing
            self.create_blocks(color, start_x, y)

    def create_blocks(self, color, start_x, y):
        if start_x < 280:
            block = Turtle(shape="square")
            block.penup()
            block.resizemode("user")
            block.shapesize(0.75, 3.5, 0)
            block.color(color)
            block.goto(start_x+40, y)
            self.blocks[color].append(block)
            self.create_blocks(color, start_x+80, y)

    def draw_border(self, x1, y1, x2, y2):
        self.hideturtle()
        self.speed(0)
        self.pensize(2)
        self.pencolor('#787A91')
        self.penup()
        self.goto(x1, y1)
        self.pendown()
        self.goto(x2, y1)
        self.goto(x2, y2)
        self.goto(x1, y2)
        self.goto(x1, y1)

class TextUIManager(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color('white')

    def scoreboard(self, x, y):
        self.goto(x, y)
        self.write(
            arg="SCORE: ",
            move=False,
            align='left',
            font=FONT
        )

class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.resizemode("user")
        self.shapesize(
            Settings.PADDLE_SHAPESIZE_H,
            Settings.PADDLE_SHAPESIZE_W
        )
        self.color("#916BBF")
        self.setpos(0, Settings.PADDLE_Y_POS)

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.resizemode("user")
        self.shapesize(
            Settings.BALL_SHAPESIZE_H,
            Settings.BALL_SHAPESIZE_W
        )
        self.color("white")

        self.x_move = 0
        self.y_move = 0
        self.move_speed = 0.05
        self.in_play = False

    def set_velocity(self, x, y):
        self.x_move = x
        self.y_move = y

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_x(self):
        self.x_move *= -1

    def bounce_y(self):
        self.y_move *= -1

    def reset_position(self, x, y):
        self.goto(x, y)
        self.x_move = 0
        self.y_move = 0
        self.in_play = False