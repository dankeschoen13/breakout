import time
from turtle import Turtle, Screen
from game_UI import GUI, TextUIManager, Player, Ball

COLORS = ["red", "orange", "yellow", "green", "blue"]

screen = Screen()
screen.setup(650, 750)
screen.getcanvas().config(highlightthickness=0)
screen.bgcolor("#03001C")
screen.title("Breakout!")
screen.tracer(0)

graphics = GUI()
text = TextUIManager()
paddle = Player()
ball = Ball()

screen.listen()
screen.onkeypress(paddle.move_right, "Right")
screen.onkeypress(paddle.move_left, "Left")

text.scoreboard(-270, 310)
graphics.create_rows( # create rows of blocks for each colors
    COLORS,
    start_x=-280,
    start_y=280
)
graphics.draw_border(-280, -325, 280, 293)

playing = True

while playing:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

screen.exitonclick()