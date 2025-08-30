from turtle import Turtle, Screen
from game_UI import BlocksGen, TextUIManager, Player

COLORS = ["red", "orange", "yellow", "green", "blue"]

screen = Screen()
screen.setup(560, 650)
screen.bgcolor("black")
screen.title("Breakout!")
screen.tracer(0)

blocks = BlocksGen()
text = TextUIManager()
paddle = Player()

screen.listen()
screen.onkeypress(paddle.move_right, "Right")
screen.onkeypress(paddle.move_left, "Left")

blocks.create_rows(COLORS, start_x=235, start_y=280)
text.scoreboard(-270, 295)

playing = True

while playing:
    screen.update()

screen.exitonclick()