from turtle import Turtle, Screen
from game_UI import GUI, TextUIManager, Player, Ball
from game_logic import Logic
from constants import Config

COLORS = ["red", "orange", "yellow", "green", "blue"]

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
paddle = Player()
logic = Logic(gui.blocks, paddle, ball, text)

screen.listen()
screen.onkeypress(logic.press_left, "Left")
screen.onkeyrelease(logic.release_left, "Left")
screen.onkeypress(logic.press_right, "Right")
screen.onkeyrelease(logic.release_right, "Right")

text.scoreboard(-270, 310)
gui.create_rows(
    Config.Game.BLOCKS_COLORS, # create rows of blocks for each colors
    start_x=-280,
    start_y=280
)
gui.draw_border(*Config.Game.BORDER_DIMENSIONS)

# def check_ball_collision(_ball: Ball, _blocks):
#     for color, block_list in _blocks.items():
#         for block in block_list[:]:  # copy to safely remove
#             if _ball.distance(block) < 30:
#                 # Get bounding box of block
#                 block_left = block.xcor() - 5
#                 block_right = block.xcor() + 5
#                 block_top = block.ycor() + 10
#                 block_bottom = block.ycor() - 10
#
#                 # Ball position
#                 ball_x, ball_y = _ball.xcor(), _ball.ycor()
#
#                 # Distances to block edges
#                 dx_left = abs(ball_x - block_left)
#                 dx_right = abs(ball_x - block_right)
#                 dy_top = abs(ball_y - block_top)
#                 dy_bottom = abs(ball_y - block_bottom)
#
#                 # Decide bounce axis
#                 if min(dx_left, dx_right) < min(dy_top, dy_bottom):
#                     _ball.x_move *= -1  # hit side → reverse horizontal
#                 else:
#                     _ball.y_move *= -1  # hit top/bottom → reverse vertical
#
#                 # Remove block
#                 block.hideturtle()
#                 _blocks[color].remove(block)
#
#                 return


def game_loop():
    logic.paddle_move()
    if logic.game_started:
        ball.move()
        # Bounce on walls
        if abs(ball.xcor()) > 265:
            ball.bounce_x()

        if ball.ycor() > 275:
            ball.bounce_y()

        # Paddle collision
        logic.check_paddle_collision()

    # Block collisions
    # check_ball_collision(ball, gui.blocks)

    # Refresh screen
    screen.update()

    # Schedule next frame
    screen.ontimer(game_loop, int(ball.move_speed * 1000))

game_loop()
screen.mainloop()