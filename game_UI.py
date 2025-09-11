from turtle import Turtle
from collections import defaultdict
from constants import Config

class GUI(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.blocks = defaultdict(list)
        self.cell_width = Config.Blocks.CELL_WIDTH
        self.half_width = Config.Blocks.CELL_WIDTH / 2

    def create_rows(self, colors, start_x, start_y, row_spacing=Config.Blocks.ROW_SPACING):
        for i, color in enumerate(colors):
            y = start_y - (i * row_spacing)  # each row lower by spacing
            self.create_blocks(color, start_x, y)

    def create_blocks(self, color, start_x, y):
        if start_x < 280:
            block = Turtle(shape="square")
            block.penup()
            block.resizemode("user")
            block.shapesize(*Config.Blocks.SHAPESIZE)
            block.color(color)
            block.goto(start_x+self.half_width, y)
            self.blocks[color].append(block)
            self.create_blocks(color, start_x+self.cell_width, y)

    def draw_border(self, x1, y1, x2, y2):
        self.hideturtle()
        self.speed(0)
        self.pensize(Config.Game.BORDER_THICKNESS)
        self.pencolor(Config.Game.BORDER_COL)
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
        self.color(Config.Game.REG_FONT_COL)

    def scoreboard(self, x, y):
        self.goto(x, y)
        self.write(
            arg=Config.Game.SCORE_TXT,
            move=False,
            align='left',
            font=Config.Game.REG_FONT
        )

class Paddle(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.resizemode("user")
        self.shapesize(*Config.Paddle.SHAPESIZE)
        self.color(Config.Paddle.COLOR)
        self.setpos(0, Config.Paddle.STARTING_POS)

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.resizemode("user")
        self.shapesize(*Config.Ball.SHAPESIZE)
        self.color(Config.Ball.COLOR)

        self.x_move = 0
        self.y_move = 0
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