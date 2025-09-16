from turtle import Turtle, Screen
from game_UI import GUI, TextUIManager, Paddle, Ball
from game_logic import Logic
from constants import Config

screen = Screen()
screen.setup(
    width=Config.Screen.WIDTH,
    height=Config.Screen.HEIGHT
)
screen.getcanvas().config(highlightthickness=0)
screen.bgcolor(Config.Screen.BG_COLOR)
screen.title(Config.Screen.TITLE)
screen.tracer(0)

gui = GUI()
text = TextUIManager()
ball = Ball()
paddle = Paddle()
logic = Logic(gui.blocks, paddle, ball, text)

screen.listen()
screen.onkeypress(logic.press_left, "Left")
screen.onkeyrelease(logic.release_left, "Left")
screen.onkeypress(logic.press_right, "Right")
screen.onkeyrelease(logic.release_right, "Right")

text.scoreboard(*Config.Game.SCORE_POS)
gui.create_rows(
    Config.Blocks.COLORS, # create rows of blocks for each colors
    start_x=-Config.Blocks.STARTING_POS,
    start_y=Config.Blocks.STARTING_POS
)
gui.draw_border(*Config.Game.BORDER_DIM)

def game_loop():
    logic.paddle_move()
    if logic.game_started:
        ball.move()
        # Bounce on walls
        if abs(ball.xcor()) > 265:
            ball.bounce_x()

        if ball.ycor() > 275:
            ball.bounce_y()

        logic.check_paddle_collision()
        logic.check_blocks_collision()

    screen.update()

    screen.ontimer(game_loop, int(1000 / Config.Screen.FPS))

game_loop()
screen.mainloop()