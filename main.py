from turtle import Turtle, Screen
from game_UI import BlocksGen, TextUIManager

COLORS = ["red", "orange", "yellow", "green", "blue"]


screen = Screen()
screen.setup(560, 650)
screen.bgcolor("black")
screen.title("Breakout!")
screen.tracer(0)

blocks = BlocksGen()
text = TextUIManager()

blocks.create_rows(COLORS, start_x=235, start_y=280)
text.scoreboard(-270, 295)

screen.update()

screen.exitonclick()