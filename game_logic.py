import math
from constants import Config

class Logic:

    def __init__(self, blocks, paddle, ball, scoreboard):
        self.blocks = blocks
        self.paddle = paddle
        self.ball = ball
        self.ball.reset_position(self.paddle.xcor(), self.get_ball_start_y())
        self.score = scoreboard
        # Game Stages Flag
        self.game_started = False
        self.first_move = []
        # Movement flags
        self.is_moving_left = False
        self.is_moving_right = False
        self.paddle_step = Config.Paddle.SPEED

    # Key press trackers
    def press_left(self):
        self.game_started = True
        self.is_moving_left = True

    def release_left(self):
        self.is_moving_left = False

    def press_right(self):
        self.game_started = True
        self.is_moving_right = True

    def release_right(self):
        self.is_moving_right = False

    def paddle_move(self):
        moved = False

        if (self.is_moving_left
                and self.paddle.xcor() > -Config.Game.X_BOUNDARY):
            self.paddle.setx(self.paddle.xcor() - self.paddle_step)
            moved = True

        if (self.is_moving_right
                and self.paddle.xcor() < Config.Game.X_BOUNDARY):
            self.paddle.setx(self.paddle.xcor() + self.paddle_step)
            moved = True

        if moved and not self.ball.in_play:
            self.launch_ball()

    def get_ball_start_y(self):
        paddle_top = self.paddle.ycor() + Config.Paddle.half_height()
        return paddle_top + Config.Ball.half_height()

    def launch_ball(self):
        if self.ball.in_play:
            return  # Already launched

        self.ball.in_play = True
        paddle_half = Config.Paddle.half_width()
        speed = Config.Ball.SPEED

        ratio = (self.ball.xcor() - self.paddle.xcor()) / paddle_half

        if self.is_moving_right:
            ratio += Config.Physics.PADDLE_PUSH
        elif self.is_moving_left:
            ratio -= Config.Physics.PADDLE_PUSH

        ratio = max(-Config.Physics.MAX_RATIO,
                    min(ratio, Config.Physics.MAX_RATIO))

        self.ball.x_move = ratio * speed

        self.ball.y_move = math.sqrt(max(speed ** 2 - self.ball.x_move ** 2, 0))

    def check_paddle_collision(self):
        paddle_half = Config.Paddle.half_width()
        if (self.paddle.ycor() < self.ball.ycor() < self.get_ball_start_y()
                and self.paddle.xcor() - paddle_half < self.ball.xcor() < self.paddle.xcor() + paddle_half
                and self.ball.y_move < 0):
            self.ball.bounce_y()

            speed = math.hypot(self.ball.x_move, self.ball.y_move)

            ratio = (self.ball.xcor() - self.paddle.xcor()) / paddle_half

            if self.is_moving_right:
                ratio += Config.Physics.PADDLE_PUSH
            elif self.is_moving_left:
                ratio -= Config.Physics.PADDLE_PUSH

            ratio = max(-Config.Physics.MAX_RATIO,
                        min(ratio, Config.Physics.MAX_RATIO))

            self.ball.x_move = ratio * speed

            self.ball.y_move = math.copysign(
                math.sqrt(max(speed ** 2 - self.ball.x_move ** 2, 0)),
                self.ball.y_move
            )
        elif self.ball.ycor() < Config.Game.BORDER_DIM[1] + Config.Ball.half_height():
            self.ball.reset_position(self.paddle.xcor(), self.get_ball_start_y())
