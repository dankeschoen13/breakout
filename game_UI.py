from turtle import Turtle
from collections import defaultdict

COLORS = ["red", "orange", "yellow", "green", "blue"]
FONT = ("Helvetica", 18, "normal")

class BlocksGen(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.blocks = defaultdict(list)

    def create_rows(self, colors, start_x, start_y, row_spacing=25):
        for i, color in enumerate(colors):
            y = start_y - (i * row_spacing)  # each row lower by spacing
            self.create_blocks(color, start_x, y)

    def create_blocks(self, color, start_x, y):
        if start_x > -300:
            block = Turtle(shape="square")
            block.penup()
            block.resizemode("user")
            block.shapesize(0.75, 3.5)
            block.color(color)
            block.goto(start_x, y)
            self.blocks[color].append(block)
            self.create_blocks(color, start_x-80, y)

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